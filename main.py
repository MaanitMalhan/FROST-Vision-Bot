import cv2
import numpy as np
import subprocess
import os
# Run libcamera-vid command to capture frames from the IMX500 camera in YUV420 format
command = "libcamera-vid -t 0 --width 640 --height 480 --framerate 30 --output - --codec yuv420"

#write_fd = os.open(command, os.O_WRONLY)

# Start the capture process with subprocess
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Set the width and height of the frame
frame_width = 640
frame_height = 480
frame_size = frame_width * frame_height * 3 // 2  # YUV420 format (Y + UV)

while True:
    # Read the raw frame data from libcamera-vid's output
    raw_frame = process.stdout.read(frame_size)

    # Check if we got the correct number of bytes
    if len(raw_frame) != frame_size:
        print(f"Error reading frame data. Expected {frame_size} bytes, but got {len(raw_frame)} bytes.")
        break

    # Convert the raw byte data (YUV420) into a numpy array
    yuv_frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((frame_height + frame_height // 2, frame_width))  # YUV420 shape

    # Convert YUV420 to RGB using OpenCV
    rgb_frame = cv2.cvtColor(yuv_frame, cv2.COLOR_YUV2BGR_I420)

    hsv = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2HSV)

    # Define range of blue color in HSV
    lower_blue = np.array([100, 45, 45])
    upper_blue = np.array([120, 250, 250])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(rgb_frame, rgb_frame, mask=mask)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding box around the detected contour(s)
    for contour in contours:
        if cv2.contourArea(contour) > 10000:  # Filter out small areas
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(rgb_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print('x:', x, 'y:', y)
            # Write the x, y coordinates to the pipe
            #os.write(write_fd, f"{x},{y}\n".encode())

    # Display the original frame with bounding boxes
    cv2.imshow('Frame', rgb_frame)
   # cv2.imshow('Mask', mask)
    cv2.imshow('Result', res)


    # Process the frame using OpenCV (e.g., converting to grayscale)
    #gray_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)

    # Display the processed frame
   # cv2.imshow('Grayscale IMX500 Stream', gray_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
process.terminate()
cv2.destroyAllWindows()
