import cv2
import os

# Create a directory to save the captured images if it doesn't exist
save_dir = 'captured_images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Open the video capture
pathVideo = 'imagenes/videos/LI.mp4'  # Use 0 for the default camera, or replace with the video file path

cap = cv2.VideoCapture(pathVideo)

# # Check if the video capture is opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

frame_count = 2
paused = False

while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow('Video Frame', frame)

    # Wait for a key press
    key = cv2.waitKey(80)

    # If 's' is pressed, pause the video and save the frame as an image
    if key == ord('s'):
        paused = True
        cv2.waitKey(0)
        frame_count += 1
        img_name = os.path.join(save_dir, f'CI_{frame_count}.png')
        cv2.imwrite(img_name, frame)
        print(f"Saved: {img_name}")

    # If 'c' is pressed, continue the video
    elif key == ord('c'):
        cv2.waitKey(0)
        paused = False

    # If 'q' is pressed, exit the loop
    elif key == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
