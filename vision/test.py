import cv2
from ultralytics import YOLO

model = YOLO("vision/best.pt")
video_path = "/dev/video2"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    success, frame = cap.read()
    if success:
        results = model(frame)
        for result in results:
            boxes = result.boxes 
            for box in boxes:
                conf = box.conf.item()
                if conf >= 0.7:  
                    x1, y1, x2, y2 = map(int, box.xyxy[0])                      
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow("YOLO Inference", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
