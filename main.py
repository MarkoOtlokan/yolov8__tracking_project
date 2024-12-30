import cv2
import datetime
import numpy as np
from ultralytics import YOLO
from sort import Sort
import sys
from plot_track import plot_tracking_data, plot_tracking_data_smoth
from sql_queries import setup_database, batch_insert_tracking_data
from helper_methods import calculate_iou, get_video

# Constants
CONFIDENCE_THRESHOLD_LIMIT = 0.7
BOX_COLOUR = (0, 255, 0)
BATCH_SIZE = 100

tracking_data = {}


def process_frame(frame, model, tracker, car_class_index, frame_number, data_batch, sql_connection):
    """
    Process a single video frame to detect, track, and record objects.

    Args:
        frame (np.ndarray): Video frame.
        model (YOLO): YOLO model instance.
        tracker (Sort): SORT tracker instance.
        car_class_index (int): Index of the car class in the model.
        frame_number (int): Current frame number.
        data_batch (list): Accumulated tracking data for batch insertion.
        sql_connection (sqlite3.Connection): SQLite connection.

    Returns:
        np.ndarray: Processed video frame.
    """
    result = model(frame)[0]
    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="float")
    confidences = np.array(result.boxes.conf.cpu(), dtype="float")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")

    # Filter detections for the target class and confidence threshold
    valid_indices = (classes == car_class_index) & (confidences > CONFIDENCE_THRESHOLD_LIMIT)
    bboxes = bboxes[valid_indices]
    confidences = confidences[valid_indices]

    detections = np.hstack((bboxes, confidences.reshape(-1, 1)))
    tracked_objects = tracker.update(detections)

    for obj in tracked_objects:
        x1, y1, x2, y2, obj_id = map(int, obj)
        obj_confidence = None
        max_iou = 0

        # Match tracked object with detection
        for bbox, confidence in zip(bboxes, confidences):
            iou = calculate_iou((x1, y1, x2, y2), bbox)
            if iou > max_iou and iou > 0.5:
                max_iou = iou
                obj_confidence = confidence

        if obj_confidence is not None:
            data_batch.append((frame_number, obj_id, x1, y1, x2, y2, obj_confidence))
            update_tracking_data(obj_id, frame_number, obj_confidence)
            label = f"Car ID: {obj_id} ({obj_confidence:.2f})"
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOUR, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 2, BOX_COLOUR, 2)

    # Insert batch data into the database if the batch size is met
    if len(data_batch) >= BATCH_SIZE:
        batch_insert_tracking_data(sql_connection, data_batch)
        data_batch.clear()

    return frame


def update_tracking_data(obj_id, frame_number, confidence):
    """
    Update the tracking data for visualization.

    Args:
        obj_id (int): Object ID.
        frame_number (int): Frame number.
        confidence (float): Detection confidence.
    """
    if obj_id not in tracking_data:
        tracking_data[obj_id] = ([], [])
    tracking_data[obj_id][0].append(frame_number)
    tracking_data[obj_id][1].append(confidence)


def main(video_source, model_name):
    """
    Main function for processing video, detecting, tracking, and storing data.
    """
    sql_connection = setup_database()
    data_batch = []
    video_source = get_video(video_source)

    model = YOLO(model_name)
    tracker = Sort()
    car_class_index = next(key for key, value in model.names.items() if value == "car")

    frame_number = 0

    while True:
        ret, frame = video_source.read()
        if not ret:
            print("End of video or no frames available.")
            break

        frame_number += 1
        start_time = datetime.datetime.now()

        frame = process_frame(frame, model, tracker, car_class_index, frame_number, data_batch, sql_connection)

        # Display FPS on the frame
        fps = f"FPS: {1 / (datetime.datetime.now() - start_time).total_seconds():.2f}"
        cv2.putText(frame, fps, (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        cv2.imshow("Output video", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    # Insert any remaining data
    if data_batch:
        batch_insert_tracking_data(sql_connection, data_batch)

    sql_connection.close()
    video_source.release()
    cv2.destroyAllWindows()

    # Plot tracking data
    plot_tracking_data(tracking_data)
    plot_tracking_data_smoth(tracking_data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <video_source> [model_name]")
        sys.exit(1)

    video_source = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "yolov8l.pt"

    print(f"Using model: {model_name}")
    main(video_source, model_name)
