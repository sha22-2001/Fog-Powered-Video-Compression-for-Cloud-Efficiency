from ultralytics import YOLO
import cv2
import cvzone
import math
import time
from datetime import datetime
from collections import defaultdict
import pygame

audio_path = "music/2.wav"

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

model = YOLO("YOLO_Weights/facehand.pt")
classNames = ['Face', 'Hand']
number = 1;

def count_hands(frame):
    count = 0
    results = model(frame, stream=True)
    for r in results:
        boxes = r.boxes
        for i, box in enumerate(boxes):
            cls = int(box.cls[0])
            class_type = classNames[cls]
            conf = math.ceil((box.conf[0] * 100)) / 100

            if class_type == "Hand" and conf > 0.65:
                count += 1

    return count


while True:
    success, img = cap.read()
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)


            cls = int(box.cls[0])
            class_type = classNames[cls]
            conf = math.ceil((box.conf[0] * 100)) / 100
            timestamp = datetime.now()

            # count hands in the current frame
            hand_count = count_hands(img)
            print("Number of hands detected:", hand_count)


            if conf > 0.60:
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cls = int(box.cls[0])
                cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            if classNames[cls] == "Hand" and conf > 0.65:
                pygame.mixer.init()
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play(-1)
                pygame.time.wait(100)

            else:
                pygame.mixer.init()
                pygame.mixer.music.stop()
                entry_time = None
                exit_time = None

    # Show image
    cv2.imshow("Image", img)
    cv2.waitKey(1)






