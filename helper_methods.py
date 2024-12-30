import cv2
import os

def calculate_iou(box1, box2):
    """
    Calculate the Intersection over Union (IoU) between two bounding boxes.

    Args:
        box1 (tuple): Coordinates of the first box (x1, y1, x2, y2).
        box2 (tuple): Coordinates of the second box (x1, y1, x2, y2).

    Returns:
        float: The IoU value between the two boxes, ranging from 0 to 1. If the boxes do not overlap, returns 0.
    """
    # Calculate intersection coordinates
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # Calculate intersection area
    intersection = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)

    # Calculate individual box areas
    box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    # Calculate union area
    union = box1_area + box2_area - intersection

    # Return IoU value
    return intersection / union if union > 0 else 0

def get_video(video_name):
    """
    Open a video file and ensure it is valid for processing.

    Args:
        video_name (str): Path to the video file.

    Returns:
        cv2.VideoCapture: A video capture object if the file is valid and can be opened.
        None: If the file is invalid or cannot be processed.
    """
    # Check if the file exists
    if not os.path.exists(video_name):
        print(f"Error: File '{video_name}' does not exist.")
        return None

    # Check if the file is not empty
    if os.path.getsize(video_name) == 0:
        print(f"Error: File '{video_name}' is empty.")
        return None

    # Attempt to open the video
    video_source = cv2.VideoCapture(video_name)
    if not video_source.isOpened():
        print(f"Error: Cannot open video source '{video_name}'.")
        return None

    # Check if the video contains any frames
    ret, _ = video_source.read()
    if not ret:
        print(f"Error: Video '{video_name}' has no frames or cannot be decoded.")
        video_source.release()
        return None

    # Reset the video to the first frame
    video_source.set(cv2.CAP_PROP_POS_FRAMES, 0)

    return video_source
