import cv2
import os
import json

# Global variables for drawing bounding boxes
drawing = False
ix, iy = -1, -1
boxes = []

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, boxes

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_img = param.copy()
            cv2.rectangle(temp_img, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow("Labeling", temp_img)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        boxes.append((ix, iy, x, y))
        cv2.rectangle(param, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.imshow("Labeling", param)

def label_frames(frames_folder, output_file):
    global boxes
    frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith('.jpg')])
    labeled_data = {}

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for frame_file in frame_files:
        frame_path = os.path.join(frames_folder, frame_file)
        img = cv2.imread(frame_path)

        # Resize the image to fit the screen
        screen_width = 1280  # Adjust as needed
        screen_height = 720  # Adjust as needed
        h, w, _ = img.shape
        scale = min(screen_width / w, screen_height / h)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

        boxes = []

        # Make the window resizable
        cv2.namedWindow("Labeling", cv2.WINDOW_NORMAL)
        cv2.imshow("Labeling", img)
        cv2.setMouseCallback("Labeling", draw_rectangle, img)

        print(f"Labeling {frame_file}. Press 's' to save, 'n' to skip, or 'q' to quit.")
        while True:
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
    frames_folder = input("Enter the path to the folder containing frames: ")
    output_file = input("Enter the output file path for labels (e.g., labels.json): ")
    label_frames(frames_folder, output_file)