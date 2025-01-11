import cv2
from ultralytics import YOLO
import os

cap = cv2.VideoCapture("Videos/12.5.mp4")
model = YOLO("YOLO_Weights/yolov8x.pt")

# Video writer setup
output_video_path = "output_video.mp4"
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4 format
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

while True:
    success, img = cap.read()

    if not success:
        print("Error reading frame from video.")
        break

    if img is None:
        print("Error: Frame is None.")
        continue

    results = model(img, stream=True)
    objects_detected = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = round(box.conf[0].item(), 2)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            objects_detected = True  # Set flag to True if any object is detected

    if objects_detected:
        out.write(img)  # Write frame to output video only if objects are detected

    cv2.imshow("Image", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release resources
out.release()
cap.release()
cv2.destroyAllWindows()
