import cv2
import os

def extract_frames(video_path, output_folder, frame_interval=10):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f'frame_{saved_count:04d}.jpg')
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
        
        frame_count += 1
    
    cap.release()
    print(f"Saved {saved_count} frames to {output_folder}")

if __name__ == "__main__":
    print("Example path: ./parent_folder/child_folder")
    video_path = input("Enter the path to the video file: ")
    output_folder = input("Enter the output folder path: ")
    extract_frames(video_path, output_folder)