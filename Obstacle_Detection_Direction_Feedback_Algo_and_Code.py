### Algorithm

# Setup and Initialization: 
    # 1.1 Import the required libraries. 
    # 1.2 Load the YOLO model (yolov10n.pt). 
    # 1.3 Start the webcam video capture. 
    # 1.4 Retrieve the class names for the YOLO model.

# Process Video Frames:
    # While the webcam is active: 
    # 2.1 Read the current video frame. 
    # 2.2 If reading fails, terminate the loop.

# Perform Object Detection:
    # Apply the YOLO model to the frame.
    # For each detected object: 
    # 3.1 Extract the bounding box coordinates, confidence score, and class ID (https://docs.ultralytics.com/datasets/detect/coco/#dataset-yaml) 
    # 3.2 Draw bounding boxes and labels on the frame.

# Identify the Swimmer:
    # If the detected object is a "person," save the swimmer's bounding box and center x-coordinate.

# Check for Obstacles:

    # For other objects in the frame: 
    # 5.1 If an object is higher (y1 < swimmer_box[1]), mark it as an obstacle. 
    # 5.2 Determine if the obstacle is on the left or right of the swimmer.

# Display Warnings:
# If obstacles are detected, display a warning message indicating the required direction to move.

# Display and Exit:
# Show the processed frame with bounding boxes and labels.
# Exit the program if the q key is pressed.

# Cleanup:
# Release the webcam and close all windows.

### Code

# cv2: Used for handling video capture, frame processing, and displaying results.
# ultralytics: The library provides the YOLO object detection model for inference.

import cv2
from ultralytics import YOLO

import time

# A YOLO model is loaded from the file 'yolov10n.pt'. Ensure that this file is the correct trained model for your application.
model = YOLO('yolov10n.pt')  

# The VideoCapture function initializes the webcam feed. Here, 0 indicates the default camera.
cap = cv2.VideoCapture(0)

# The model.names attribute contains the list of class names the model can detect (e.g., "person", "car", etc.).
class_names = model.names  # Automatically loads class names associated with the model

# print(class_names)

# The loop reads frames from the webcam. If ret is False, the video feed failed.
while cap.isOpened():
    ret, frame = cap.read()  # Read each frame from the video
    
    if not ret:
        print("Failed to grab frame. Exiting.")
        break
    
    # The YOLO model is applied to the frame to detect objects. The result includes bounding boxes, class IDs, and confidence scores.
    results = model(frame)  # Perform object detection on the frame
    # print(type(results))
    # print(len(results))

    time.sleep(5)
    
    # Initialize variables for the swimmer's bounding box and center
    swimmer_box = None
    swimmer_center_x = None

    # For each detection:
        # Bounding Box Coordinates: (x1, y1) (top-left) and (x2, y2) (bottom-right).
        # Confidence: Probability of the detection.
        # Class ID: Represents the detected object's class.

    # Iterate through the detections for the current frame
    for result in results:
        # print(result)
        # time.sleep(5)
        boxes = result.boxes  # Get all detected bounding boxes
        for box in boxes:
            # Extract bounding box coordinates and convert to integers
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Top-left (x1, y1) and bottom-right (x2, y2)
            confidence = box.conf[0]  # Extract the confidence score
            class_id = int(box.cls[0])  # Extract the class ID of the detected object

            # Draw a bounding box around the detected object
            # - 'color' specifies the box's color in BGR format (green in this case).
            # - 'thickness' defines the width of the bounding box border.
            # - 'cv2.rectangle()' draws the box on the frame using the coordinates of the top-left (x1, y1)
            #   and bottom-right (x2, y2) corners.

            color = (0, 255, 0)  # Green for bounding box
            thickness = 2
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)  # Draw the rectangle

            # Create and position a label for the detected object
            # - 'label' combines the class name and confidence score, formatted to 2 decimal places.
            # - Font properties are defined using OpenCV's font options: 
            #   'FONT_HERSHEY_SIMPLEX' (basic sans-serif), 'font_scale' (size), and 'font_thickness' (stroke width).
            # - 'cv2.getTextSize()' calculates the size of the label text to position it accurately above the bounding box.
            # - The label's position is set slightly above the top-left corner of the bounding box (y1 - 10 pixels).

            label = f"{class_names[class_id]}: {confidence:.2f}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_thickness = 1
            
            text_size, _ = cv2.getTextSize(label, font, font_scale, font_thickness)  # Measure text size
            text_x, text_y = x1, y1 - 10  # Position above the bounding box

            # Bounding boxes are drawn around detected objects with labels showing the class name and confidence score
            cv2.rectangle(frame, (text_x, text_y - text_size[1]), (text_x + text_size[0], text_y), color, -1)

            # Overlay the label text on top of the rectangle
            cv2.putText(frame, label, (text_x, text_y - 2), font, font_scale, (0, 0, 0), font_thickness)  # Text

            # If a detected object is a "person," it is considered the swimmer. The swimmer's bounding box and center (x-coordinate) are calculated.
            if class_names[class_id] == "person":
                swimmer_box = (x1, y1, x2, y2)
                swimmer_center_x = (x1 + x2) // 2  # Calculate swimmer's center x-coordinate

    if swimmer_box:
        # Set flag to check if an obstacle is ahead
        obstacle_ahead = False
        move_direction = None

        # Iterate through other detected objects to check for obstacles ahead
        for result in results:
            boxes = result.boxes
            # print(f"Boxes : {boxes}")
            for box in boxes:
                # print(f"Boxes : {box}")
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Extract coordinates of the detected object
                class_id = int(box.cls[0])  # Extract class ID

                # Skip if the object is the swimmer
                if class_names[class_id] == "person":
                    continue

                # Obstacles are checked:
                # Vertical Position: If an object is higher (smaller y1) than the swimmer, it is ahead.
                # Horizontal Position: The obstacle is classified as "left" or "right" of the swimmer based on x1.
                if y1 < swimmer_box[1]:  # Object is above the swimmer (ahead)
                    obstacle_ahead = True

                    # Determine if the obstacle is to the left or right of the swimmer
                    if x1 < swimmer_center_x:
                        move_direction = "left"
                    else:
                        move_direction = "right"

                    # If an obstacle is ahead, a warning message is displayed on the frame and printed in the console.
                    obstacle_label = "Obstacle ahead, change the route!"
                    cv2.putText(frame, obstacle_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    break  # Exit the loop once an obstacle ahead is detected

        if obstacle_ahead:
            print(f"Obstacle ahead! Swimmer should move to their {move_direction}.")
        else:
            print("No obstacle ahead. The swimmer can continue.")
    
    # The processed frame is displayed in a window. Pressing q exits the program.
    cv2.imshow("Processed Feed", frame)
    # Wait for 1 ms between frames, and exit if 'q' is pressed
    k = cv2.waitKey(1)
    if k == ord('q'):
        print("Exiting the program.")
        break

cv2.destroyAllWindows()
cap.release()
