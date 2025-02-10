import cv2
import os

# Define the folder to save images
save_folder = "cap"

# Create the folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)

# Open the video stream (camera index 0 for default webcam)
video_path = "/dev/video2"
cap = cv2.VideoCapture(video_path)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

img_count = 0  # Counter for image filenames

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture image.")
        break

    # Display the live video feed
    cv2.imshow("Video Feed - Press 's' to save, 'q' to quit", frame)

    # Wait for key press
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):  # Press 's' to save an image
        img_filename = os.path.join(save_folder, f"captured_image_{img_count}.jpg")
        cv2.imwrite(img_filename, frame)
        print(f"Image saved: {img_filename}")
        img_count += 1  # Increment counter

    elif key == ord("q"):  # Press 'q' to quit
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
