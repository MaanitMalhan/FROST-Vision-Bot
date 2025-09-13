import cv2
import json
import sys

# Create the CSRT tracker
tracker = cv2.legacy.TrackerCSRT_create()

# Get video source from command-line argument or fallback to input()
if len(sys.argv) > 1:
    video_source = sys.argv[1]
else:
    try:
        video_source = input("Enter '0' to use the camera or provide the path to an MP4 file: ")
    except EOFError:
        print("No video source provided. Exiting.")
        exit()

# Open video capture
if video_source == '0':
    video = cv2.VideoCapture(0)
else:
    video = cv2.VideoCapture(video_source)

if not video.isOpened():
    print("Could not open video source")
    exit()

# Read the first frame
ok, frame = video.read()
if not ok:
    print("Cannot read video file")
    exit()

# Get label name from command-line argument or fallback to input()
if len(sys.argv) > 2:
    label_name = sys.argv[2]
else:
    try:
        label_name = input("Enter a label name for the object being tracked: ")
    except EOFError:
        print("No label name provided. Exiting.")
        exit()

# Resize the frame for display if needed
def resize_frame(frame, width=800):
    height, original_width = frame.shape[:2]
    scale = width / original_width
    new_height = int(height * scale)
    return cv2.resize(frame, (width, new_height))

# Make the OpenCV window resizable
cv2.namedWindow("Tracking", cv2.WINDOW_NORMAL)

# Let user select ROI
frame_resized = resize_frame(frame)
bbox = cv2.selectROI("Select ROI", frame_resized, False)
cv2.destroyWindow("Select ROI")

# Adjust the bounding box to match the original frame size
scale = frame.shape[1] / frame_resized.shape[1]
bbox = tuple(int(coord * scale) for coord in bbox)

# Initialize tracker with first frame and bounding box
ok = tracker.init(frame, bbox)

# Prepare JSON file for saving bounding box coordinates
output_file = "bounding_boxes.json"
bounding_boxes = {label_name: []}  # Organize by label name

frame_count = 0  # Initialize frame counter

while True:
    frame_count += 1
    ok, frame = video.read()
    if not ok:
        break

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Check if tracking failed
    if not ok:
        cv2.putText(frame, "Tracking failure. Press 'r' to reinitialize.", (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        cv2.imshow("Tracking", resize_frame(frame))

        # Wait for user input to reinitialize
        key = cv2.waitKey(0) & 0xff
        if key == ord('r'):  # Press 'r' to reinitialize
            frame_resized = resize_frame(frame)
            bbox = cv2.selectROI("Select ROI", frame_resized, False)
            cv2.destroyWindow("Select ROI")

            # Adjust the bounding box to match the original frame size
            scale = frame.shape[1] / frame_resized.shape[1]
            bbox = tuple(int(coord * scale) for coord in bbox)

            # Reinitialize tracker
            tracker = cv2.legacy.TrackerCSRT_create()
            tracker.init(frame, bbox)
        continue

    # Draw bounding box if tracking is successful
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (0, 255, 0), 3, 1)  # Thicker rectangle (thickness=3)

    # Save bounding box corner coordinates to JSON
    bounding_boxes[label_name].append({
        "frame": frame_count,
        "top_left": {"x": p1[0], "y": p1[1]},
        "bottom_right": {"x": p2[0], "y": p2[1]}
    })

    # Resize the frame for display
    frame_resized = resize_frame(frame)

    # Display result
    cv2.imshow("Tracking", frame_resized)

    # Exit if ESC is pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

# Write bounding boxes to JSON file
with open(output_file, "w") as f:
    json.dump(bounding_boxes, f, indent=4)

video.release()
cv2.destroyAllWindows()