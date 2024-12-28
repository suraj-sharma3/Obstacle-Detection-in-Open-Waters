# Testing the yolo model with video data

import os

from ultralytics import YOLO
import cv2

VIDEOS_DIR = os.path.join('.', 'videos')

video_path = os.path.join(VIDEOS_DIR, 'cracked_pipe_video.mp4')
video_path_out = '{}_out.mp4'.format(video_path)

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')

# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.5

while ret:

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()

### Improved Code

# Testing the YOLO model with video data

""" import os
from ultralytics import YOLO
import cv2

VIDEOS_DIR = os.path.join('.', 'videos')
video_path = os.path.join(VIDEOS_DIR, 'cracked_pipe_video.mp4')
video_path_out = '{}_out.mp4'.format(video_path)

# Ensure video file exists
if not os.path.exists(video_path):
    raise FileNotFoundError(f"Video file not found: {video_path}")

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

if not ret:
    raise ValueError(f"Failed to read the video file: {video_path}")

H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')

# Ensure model file exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

# Load a YOLO model
model = YOLO(model_path)

threshold = 0.5  # Confidence threshold

while ret:
    # Predict using the YOLO model
    results = model(frame, conf=threshold)[0]  # Set confidence threshold during inference

    # Draw bounding boxes
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            label = f"{model.names[int(class_id)]}: {score:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1 - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

    out.write(frame)

    # Read next frame
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows() """


# Real-time testing of the YOLO model with camera feed

""" 
import os
from ultralytics import YOLO
import cv2

# Camera index (0 is default camera, adjust if you have multiple cameras)
camera_index = 0
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    raise ValueError(f"Unable to access the camera with index {camera_index}")

# Load a YOLO model
model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

model = YOLO(model_path)
threshold = 0.5  # Confidence threshold

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame from the camera. Exiting...")
        break

    # Predict using the YOLO model
    results = model(frame, conf=threshold)[0]  # Set confidence threshold during inference

    # Draw bounding boxes
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            label = f"{model.names[int(class_id)]}: {score:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1 - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the processed frame in a window
    cv2.imshow("YOLO Detection", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() """

