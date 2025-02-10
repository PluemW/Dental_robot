import cv2
import numpy as np

# Capture video from the webcam
cap = cv2.VideoCapture("/dev/video2")  # Change to video file path if needed

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply threshold to detect black line
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour (assuming it's the line)
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])  # Center X of the black line
            cy = int(M["m01"] / M["m00"])  # Center Y (optional)

            # Get frame center
            frame_center = frame.shape[1] // 2

            # Print direction based on line position
            if cx < frame_center - 50:
                direction = "Left"
            elif cx > frame_center + 50:
                direction = "Right"
            else:
                direction = "Straight"

            print(direction)

            # Draw the detected line and center point
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 3)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.line(frame, (frame_center, 0), (frame_center, frame.shape[0]), (255, 0, 0), 2)

    # Display the processed frame
    cv2.imshow("Line Tracking", frame)
    cv2.imshow("Threshold", thresh)

    # Break loop on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
