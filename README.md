# Tracking System with YOLOV8

This project is a Python-based tracking system that uses YOLO for object detection and SORT for tracking. It processes video data, tracks objects (e.g., cars), and stores results in a database for further analysis.

## Features
- Object detection using the YOLO model.
- Object tracking using the SORT algorithm.
- Real-time visualization of tracking results.
- Data persistence using SQLite.
- Smoothed probability plots for tracking confidence.

## Requirements
Install dependencies using the provided `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

File Structure
1. main.py: Main script for video tracking.
2. plot_track.py: Contains visualization functions.
3. sql_queries.py: Manages database operations.
4. helper_methods.py: Includes utility functions (e.g., IoU calculation).
5. requirements.txt: Dependency list.


## How to Run
Ensure you have a video file (e.g., video.mp4) and a YOLO model (e.g., yolov8l.pt).
Execute the script:
```python
python main.py <video_source> [model_name]
```

<video_source>: Path to the input video file.

[model_name] (optional): Path to the YOLO model file. Default is yolov8l.pt.
Example
```bash
python main.py video.mp4 yolov8l.pt
```# yolov8__tracking_project
