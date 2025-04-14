import cv2
import numpy as np

# Load image
image_path = "C:\\Users\\CoolR\\Code\\datasetCV_test\\output_folder\\frame_0026.jpg"
frame = cv2.imread(image_path)

if frame is None:
    raise ValueError("Image not found. Check the path.")

current_coordinates = {"x": None, "y": None}

# Define HSV range for white
lower_hsv = np.array([0, 0, 200])
upper_hsv = np.array([180, 30, 255])

# Convert BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
res = cv2.bitwise_and(frame, frame, mask=mask)

# Find contours
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    if cv2.contourArea(contour) > 100:  # Adjust area threshold as needed
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        current_coordinates = {"x": x, "y": y}
        break  # Use the first large contour found

# Show results
cv2.imshow("Original", frame)
cv2.imshow("Mask", mask)
cv2.imshow("Filtered", res)
cv2.waitKey(0)
cv2.destroyAllWindows()