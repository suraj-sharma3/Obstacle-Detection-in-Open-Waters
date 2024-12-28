import cv2
import numpy as np

def process_image(image):
    # Step 1: Preprocess the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Step 2: Water segmentation (example: detect non-water regions)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_water = np.array([90, 50, 50])  # Adjust HSV values for water
    upper_water = np.array([130, 255, 255])
    water_mask = cv2.inRange(hsv, lower_water, upper_water)
    obstacle_mask = cv2.bitwise_not(water_mask)

    # Step 3: Contour detection
    contours, _ = cv2.findContours(obstacle_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    obstacle_zones = {'left': False, 'center': False, 'right': False}

    # Define swimmer path zones (assume fixed coordinates for simplicity)
    height, width = image.shape[:2]
    left_zone = (0, int(width / 3))
    center_zone = (int(width / 3), int(2 * width / 3))
    right_zone = (int(2 * width / 3), width)

    # Step 4: Map obstacles to zones
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cx = x + w // 2  # Obstacle center x-coordinate

        if left_zone[0] <= cx < left_zone[1]:
            obstacle_zones['left'] = True
        elif center_zone[0] <= cx < center_zone[1]:
            obstacle_zones['center'] = True
        elif right_zone[0] <= cx < right_zone[1]:
            obstacle_zones['right'] = True

    return obstacle_zones

def decide_path(obstacle_zones):
    if obstacle_zones['center']:
        if not obstacle_zones['left']:
            return "Move left"
        elif not obstacle_zones['right']:
            return "Move right"
        else:
            return "Stop! No clear path"
    return "Keep going"

# Example usage
image = cv2.imread(r'C:\Users\OMOLP094\Desktop\WORK_FROM_NOV_2024\Obstacle_Detection_for_Swimmers\swimmer_open_water_no_obstacle_1.jpg')
obstacle_zones = process_image(image)
decision = decide_path(obstacle_zones)
print(decision)
