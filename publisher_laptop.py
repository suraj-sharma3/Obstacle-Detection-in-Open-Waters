import cv2
from ultralytics import YOLO
import time
import paho.mqtt.client as mqtt

# MQTT Setup
BROKER = "test.mosquitto.org"  # Change this to your MQTT broker's IP
PORT = 1883
TOPIC = "swim/movement"

# Initialize MQTT client
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

# Load YOLO model
model = YOLO('yolov10n.pt')

# Start video capture
cap = cv2.VideoCapture(0)
class_names = model.names  # Load class names

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting.")
        break

    results = model(frame)
    time.sleep(5)

    swimmer_box = None
    swimmer_center_x = None
    move_direction = None

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])

            if class_names[class_id] == "person":
                swimmer_box = (x1, y1, x2, y2)
                swimmer_center_x = (x1 + x2) // 2

    if swimmer_box:
        obstacle_ahead = False
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])

                if class_names[class_id] == "person":
                    continue

                if y1 < swimmer_box[1]:  # Object is above (ahead)
                    obstacle_ahead = True
                    move_direction = "left" if x1 < swimmer_center_x else "right"
                    break

        if obstacle_ahead:
            print(f"Obstacle ahead! Move {move_direction}.")
            client.publish(TOPIC, move_direction)  # Send MQTT message

    cv2.imshow("Processed Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client.disconnect()
cv2.destroyAllWindows()
cap.release()
