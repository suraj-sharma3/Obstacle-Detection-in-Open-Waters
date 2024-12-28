from ultralytics import YOLO

# Load the pre-trained YOLOv10-N model
model = YOLO("yolov10n.pt")
results = model(r"C:\Users\OMOLP094\Desktop\WORK_FROM_NOV_2024\Obstacle_Detection_for_Swimmers\swimmer_open_water_no_obstacle_1.jpg")
# results[0].show()

# for result in results:
#     result.show()
#     print(result)

# Iterate through the detections
for result in results:
    boxes = result.boxes  # Get all detected boxes
    for box in boxes:
        # Extract bounding box coordinates
        x1, y1, x2, y2 = box.xyxy[0]  # Top-left (x1, y1) and bottom-right (x2, y2)
        confidence = box.conf[0]      # Confidence score
        class_id = box.cls[0]         # Class ID
        
        print(f"Bounding Box: {x1}, {y1}, {x2}, {y2}")
        print(f"Confidence: {confidence}")
        print(f"Class ID: {class_id}")

# Display the image with bounding boxes
results[0].plot(show=True)


