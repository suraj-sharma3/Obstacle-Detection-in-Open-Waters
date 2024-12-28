import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolov10n.pt')  # Replace 'yolov10.pt' with the correct YOLO model file

# Path to the input image
image_path = r'C:\Users\OMOLP094\Desktop\WORK_FROM_NOV_2024\Obstacle_Detection_for_Swimmers\swimmer_with_obstacles_1.jpg'  # Input image file path
output_path = r'C:\Users\OMOLP094\Desktop\WORK_FROM_NOV_2024\Obstacle_Detection_for_Swimmers\swimmer_with_obstacles_1_bbox.jpg'  # Output image file path where the result will be saved

# Load the image
image = cv2.imread(image_path)  # Read the image from the specified file path

# Perform inference using the YOLO model
results = model(image_path)  # Perform object detection on the input image

# Define a list of class names (replace with your custom class names if applicable)
class_names = model.names  # Automatically loads class names associated with the model

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

# Save the output image with bounding boxes and labels
cv2.imwrite(output_path, image)  # Write the modified image to the specified file path

print(f"Output image saved to {output_path}")  # Inform the user about the saved output
