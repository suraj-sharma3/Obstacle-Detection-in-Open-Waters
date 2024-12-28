import cv2
import socket
import time
from ultralytics import YOLO

# ESP32 Access Point IP and Port
ESP32_IP = "192.168.4.1"  # Replace with the actual IP address of your ESP32 Access Point
PORT = 80  # Port for HTTP server

# Load YOLO model
model = YOLO("yolov8n.pt")  # YOLOv8 model (you can use yolov5 or other versions)

def detect_objects(frame):
    """Detect objects in a given frame using YOLO."""
    results = model(frame, conf=0.5)  # Set confidence threshold to 0.5
    # Check if any objects were detected
    return len(results[0].boxes) > 0

def send_request(command):
    """Send a command to the ESP32."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the ESP32 server
        client_socket.connect((ESP32_IP, PORT))

        # Prepare the HTTP GET request with the command
        http_request = f"GET / HTTP/1.1\r\nHost: ESP32\r\n\r\n{command}"
        client_socket.sendall(http_request.encode())

        # Receive and display the response
        response = client_socket.recv(4096)
        print("Response from ESP32:")
        print(response.decode())

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client_socket.close()

def main():
    # Open the video capture (default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Perform object detection
        object_detected = detect_objects(frame)

        if object_detected:
            print("Object detected! Sending 'vibrate' command to ESP32.")
            send_request("vibrate")
            time.sleep(2)  # Avoid spamming the ESP32 with requests

        # Display the video feed
        # cv2.imshow("Video Feed", frame)

        # Exit the loop if 'q' is pressed
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        if 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
