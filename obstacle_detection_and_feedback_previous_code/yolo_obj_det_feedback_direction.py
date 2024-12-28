import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolov10n.pt')  

# Path to the input image
image_path = r'C:\Users\OMOLP094\Desktop\WORK_FROM_NOV_2024\Obstacle_Detection_for_Swimmers\swimmer_open_water_no_obstacle_1.jpg'  # Input image file path
output_path = r'C:\Users\OMOLP094\Desktop\WORK_FROM_NOV_2024\Obstacle_Detection_for_Swimmers\swimmer_with_obstacles_1_bbox.jpg'  # Output image file path where the result will be saved

# Load the image
image = cv2.imread(image_path)  # Read the image from the specified file path

# Perform inference using the YOLO model
results = model(image_path)  # Perform object detection on the input image

# Define a list of class names (replace with your custom class names if applicable)
class_names = model.names  # Automatically loads class names associated with the model

# Initialize variables for the swimmer's bounding box
swimmer_box = None
swimmer_center_x = None

# Iterate through the detections (one result per image)
for result in results:
    boxes = result.boxes  # Get all detected bounding boxes in the result
    for box in boxes:
        # Extract bounding box coordinates and convert them to integers
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Top-left (x1, y1) and bottom-right (x2, y2)
        confidence = box.conf[0]  # Extract the confidence score of the detection
        class_id = int(box.cls[0])  # Extract the class ID of the detected object

        # Draw the bounding box on the image
        color = (0, 255, 0)  # Green color for the bounding box
        thickness = 2  # Thickness of the bounding box lines
        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)  # Draw the rectangle

        # Create a label with the class name and confidence score
        label = f"{class_names[class_id]}: {confidence:.2f}"  # Format the label text
        font = cv2.FONT_HERSHEY_SIMPLEX  # Specify the font for the label text
        font_scale = 0.5  # Scale of the font
        font_thickness = 1  # Thickness of the label text
        text_size, _ = cv2.getTextSize(label, font, font_scale, font_thickness)  # Measure text size
        text_x, text_y = x1, y1 - 10  # Position the label above the bounding box
        text_w, text_h = text_size  # Width and height of the text box

        # Draw a filled rectangle as the background for the label
        cv2.rectangle(image, (text_x, text_y - text_h), (text_x + text_w, text_y), color, -1)  # Background

        # Overlay the label text on top of the rectangle
        cv2.putText(image, label, (text_x, text_y - 2), font, font_scale, (0, 0, 0), font_thickness)  # Text

        # Check if the detected object is the swimmer (person)
        if class_names[class_id] == "person":
            swimmer_box = (x1, y1, x2, y2)
            swimmer_center_x = (x1 + x2) // 2  # Calculate the swimmer's center x-coordinate

# If the swimmer is detected
if swimmer_box:
    # Set a flag to check if an obstacle is ahead
    obstacle_ahead = False
    move_direction = None

    # Iterate through other detected objects to check for obstacles ahead
    for result in results:
        boxes = result.boxes  # Get all detected bounding boxes in the result
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Extract coordinates of the detected object
            class_id = int(box.cls[0])  # Extract the class ID of the detected object

            # Skip if the object is the swimmer
            if class_names[class_id] == "person":
                continue

            # Check if the object is ahead of the swimmer (y-axis comparison, assuming lower y means closer)
            if y1 < swimmer_box[1]:  # The object is above the swimmer (ahead)
                obstacle_ahead = True

                # Determine if the obstacle is to the left or right of the swimmer
                if x1 < swimmer_center_x:
                    move_direction = "right"
                else:
                    move_direction = "left"

                # Draw an additional message for the obstacle
                obstacle_label = "Obstacle ahead, change the route!"
                cv2.putText(image, obstacle_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                break  # Exit the loop once an obstacle ahead is detected

    if obstacle_ahead:
        print(f"Obstacle ahead! Swimmer should move to their {move_direction}.")
    else:
        print("No obstacle ahead. The swimmer can continue.")

# Save the output image with bounding boxes and labels
cv2.imwrite(output_path, image)  # Write the modified image to the specified file path

print(f"Output image saved to {output_path}")  # Inform the user about the saved output
