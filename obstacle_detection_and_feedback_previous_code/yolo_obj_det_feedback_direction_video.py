import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolov10n.pt')  # Use the correct YOLO model file

# Path to the input video file (replace with your video file path)
video_path = r'C:\Users\OMOLP094\Desktop\WORK_FROM_NOV_2024\obstacle_detection_swimmers_open_waters\obstacle_detection_and_feedback_previous_code\swimmer_no_obstacle_2.mp4'  
output_video_path = r'C:\Users\OMOLP094\Desktop\WORK_FROM_NOV_2024\obstacle_detection_swimmers_open_waters\obstacle_detection_and_feedback_previous_code\swimmer_no_obstacle_2_bbox.mp4'

# Open the video file
cap = cv2.VideoCapture(video_path)

# Get video properties (width, height, fps)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create VideoWriter object to save the processed video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Define a list of class names (replace with your custom class names if applicable)
class_names = model.names  # Automatically loads class names associated with the model

while cap.isOpened():
    ret, frame = cap.read()  # Read each frame from the video
    
    if not ret:
        break  # Break the loop if there are no frames left
    
    # Perform inference using the YOLO model for the current frame
    results = model(frame)  # Perform object detection on the frame
    
    # Initialize variables for the swimmer's bounding box and center
    swimmer_box = None
    swimmer_center_x = None

    # Iterate through the detections for the current frame
    for result in results:
        boxes = result.boxes  # Get all detected bounding boxes
        for box in boxes:
            # Extract bounding box coordinates and convert to integers
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Top-left (x1, y1) and bottom-right (x2, y2)
            confidence = box.conf[0]  # Extract the confidence score
            class_id = int(box.cls[0])  # Extract the class ID of the detected object

            # Draw the bounding box on the frame
            color = (0, 255, 0)  # Green for bounding box
            thickness = 2
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)  # Draw the rectangle

            # Create label with class name and confidence score
            label = f"{class_names[class_id]}: {confidence:.2f}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_thickness = 1
            text_size, _ = cv2.getTextSize(label, font, font_scale, font_thickness)  # Measure text size
            text_x, text_y = x1, y1 - 10  # Position above the bounding box

            # Draw background for the label
            cv2.rectangle(frame, (text_x, text_y - text_size[1]), (text_x + text_size[0], text_y), color, -1)

            # Overlay the label text on top of the rectangle
            cv2.putText(frame, label, (text_x, text_y - 2), font, font_scale, (0, 0, 0), font_thickness)  # Text

            # Check if the detected object is the swimmer (person)
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
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Extract coordinates of the detected object
                class_id = int(box.cls[0])  # Extract class ID

                # Skip if the object is the swimmer
                if class_names[class_id] == "person":
                    continue

                # Check if the object is ahead of the swimmer (y-axis comparison, assuming lower y means closer)
                if y1 < swimmer_box[1]:  # Object is above the swimmer (ahead)
                    obstacle_ahead = True

                    # Determine if the obstacle is to the left or right of the swimmer
                    if x1 < swimmer_center_x:
                        move_direction = "right"
                    else:
                        move_direction = "left"

                    # Draw an additional message for the obstacle
                    obstacle_label = "Obstacle ahead, change the route!"
                    cv2.putText(frame, obstacle_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    break  # Exit the loop once an obstacle ahead is detected

        if obstacle_ahead:
            print(f"Obstacle ahead! Swimmer should move to their {move_direction}.")
        else:
            print("No obstacle ahead. The swimmer can continue.")
    
    # Write the processed frame to the output video
    out.write(frame)

# Release the video capture and writer objects
cap.release()
out.release()

print(f"Processed video saved to {output_video_path}")
