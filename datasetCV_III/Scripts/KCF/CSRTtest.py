import cv2

# Create the CSRT tracker
tracker = cv2.legacy.TrackerCSRT_create()

# Prompt user for video source
video_source = input("Enter '0' to use the camera or provide the path to an MP4 file: ")

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

while True:
    ok, frame = video.read()
    if not ok:
        break

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Draw bounding box if tracking is successful
    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
    else:
        cv2.putText(frame, "Tracking failure", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Resize the frame for display
    frame_resized = resize_frame(frame)

    # Display result
    cv2.imshow("Tracking", frame_resized)

    # Exit if ESC is pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

video.release()
cv2.destroyAllWindows()
