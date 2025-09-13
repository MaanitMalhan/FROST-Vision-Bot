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
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="Extract frames from a video file.")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("output_folder", help="Path to the output folder")
    parser.add_argument("--frame_interval", type=int, default=10, help="Interval between frames to save (default: 10)")
    args = parser.parse_args()
    extract_frames(args.video_path, args.output_folder, args.frame_interval)