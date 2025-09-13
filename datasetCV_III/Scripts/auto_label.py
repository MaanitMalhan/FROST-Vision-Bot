import cv2
import numpy as np
import os
import json

def nothing(x):
    pass

def create_hsv_sliders():
    # Create the HSV Sliders window
    cv2.namedWindow("HSV Sliders", cv2.WINDOW_NORMAL)
    cv2.createTrackbar("H Min", "HSV Sliders", 0, 179, nothing)
    cv2.createTrackbar("H Max", "HSV Sliders", 179, 179, nothing)
    cv2.createTrackbar("S Min", "HSV Sliders", 0, 255, nothing)
    cv2.createTrackbar("S Max", "HSV Sliders", 255, 255, nothing)
    cv2.createTrackbar("V Min", "HSV Sliders", 0, 255, nothing)
    cv2.createTrackbar("V Max", "HSV Sliders", 255, 255, nothing)

def get_hsv_ranges():
    # Get the current positions of the sliders
    h_min = cv2.getTrackbarPos("H Min", "HSV Sliders")
    h_max = cv2.getTrackbarPos("H Max", "HSV Sliders")
    s_min = cv2.getTrackbarPos("S Min", "HSV Sliders")
    s_max = cv2.getTrackbarPos("S Max", "HSV Sliders")
    v_min = cv2.getTrackbarPos("V Min", "HSV Sliders")
    v_max = cv2.getTrackbarPos("V Max", "HSV Sliders")
    return (h_min, s_min, v_min), (h_max, s_max, v_max)

def auto_label_frames(frames_folder, output_file):
    frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith('.jpg')])
    labeled_data = {}

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Create the HSV sliders
    create_hsv_sliders()

    for frame_file in frame_files:
        frame_path = os.path.join(frames_folder, frame_file)
        img = cv2.imread(frame_path)
        img_resized = cv2.resize(img, (800, 600))  # Resize for better visibility
        hsv = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)

        while True:
            # Get the HSV range from the sliders
            lower_range, upper_range = get_hsv_ranges()
            mask = cv2.inRange(hsv, np.array(lower_range), np.array(upper_range))
            result = cv2.bitwise_and(img_resized, img_resized, mask=mask)

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            boxes = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w * h > 500:  # Filter out small detections
                    boxes.append((x, y, x + w, y + h))
                    cv2.rectangle(img_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display the results
            cv2.imshow("Original", img_resized)
            cv2.imshow("Mask", mask)
            cv2.imshow("Filtered", result)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):  # Save labels
                labeled_data[frame_file] = boxes
                print(f"Saved labels for {frame_file}: {boxes}")
                break
            elif key == ord('n'):  # Skip frame
                print(f"Skipped {frame_file}")
                break
            elif key == ord('q'):  # Quit labeling
                print("Exiting labeling tool.")
                cv2.destroyAllWindows()
                with open(output_file, 'w') as f:
                    json.dump(labeled_data, f, indent=4)
                return

    cv2.destroyAllWindows()
    with open(output_file, 'w') as f:
        json.dump(labeled_data, f, indent=4)
    print(f"Labels saved to {output_file}")

if __name__ == "__main__":
    import sys
    # Get frames folder and output file from command-line arguments or fallback to input()
    if len(sys.argv) > 2:
        frames_folder = sys.argv[1]
        output_file = sys.argv[2]
    else:
        try:
            frames_folder = input("Enter the path to the folder containing frames: ")
            output_file = input("Enter the output file path for labels (e.g., labels.json): ")
        except EOFError:
            print("No input provided. Exiting.")
            exit()
    auto_label_frames(frames_folder, output_file)