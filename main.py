import cv2 as cv
import numpy as np
import os

pipe_name = '/tmp/vision_pipe'

# Open the named pipe for writing
write_fd = os.open(pipe_name, os.O_WRONLY)

cap = cv.VideoCapture('./Test/video.mp4')  

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

while True:
    # Take each frame
    _, frame = cap.read()
    if frame is None:
        print("Error: Could not read frame.")
        break

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Define range of blue color in HSV
    lower_blue = np.array([100, 45, 45])
    upper_blue = np.array([120, 250, 250])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame, frame, mask=mask)

    # Find contours in the mask
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Draw bounding box around the detected contour(s)
    for contour in contours:
        if cv.contourArea(contour) > 10000:  # Filter out small areas
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print('x:', x, 'y:', y)
            # Write the x, y coordinates to the pipe
            os.write(write_fd, f"{x},{y}\n".encode())

    # Display the original frame with bounding boxes
    cv.imshow('Frame', frame)
    cv.imshow('Mask', mask)
    cv.imshow('Result', res)

    # Break the loop if 'Esc' key is pressed
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
os.close(write_fd)
