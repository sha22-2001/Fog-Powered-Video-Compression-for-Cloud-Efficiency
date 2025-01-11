from ultralytics import YOLO
import cv2
import cvzone
import math
import time
import pygame
from datetime import datetime
import os

audio_path = "music/3.wav"
cap = cv2.VideoCapture("Videos/12.mp4")  # 12 26 9 27

model = YOLO("YOLO_Weights/yolov8x.pt")

classNames = ["person", "", "car", "", "", "Tiger", "train", "", "",
              "", "", "", "", "", "", "Tiger",
              "Tiger", "", "", "Cow", "Elephant", "Bear", "Tiger", "Leopard", "", "", ]

prev_frame_time = 0
new_frame_time = 0

# Initialize class count dictionary
class_counts = {class_name: 0 for class_name in classNames}

# Get the current date and format it as "dd-mm-yy" for the text file name
current_date_str = datetime.now().strftime("%d-%m-%y")
text_file_path = os.path.join("Analyse_Data()/detected_objects/D@ta/", f"{current_date_str}.txt")

# Create a text file to store the data
text_file = open(text_file_path, "w")

# Define the directory to save detected object images
output_directory = "Analyse_Data()/detected_objects"

# Create the directory if it doesn't exist
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

while True:
    new_frame_time = time.time()
    success, img = cap.read()
    results = model(img, stream=True)

    # Reset class counts for each frame
    for class_name in classNames:
        class_counts[class_name] = 0

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            if conf > 0.7:
                cvzone.cornerRect(img, (x1, y1, w, h))
                # Save the detected object as an image
                detected_object = img[y1:y2, x1:x2]
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                image_filename = os.path.join(output_directory, f"object_{timestamp}.jpg")
                cv2.imwrite(image_filename, detected_object)
            # Class Name
            cls = int(box.cls[0])
            print("cls:", cls)
            class_name = classNames[cls]

            if conf > 0.7:
                cvzone.putTextRect(img, f'{class_name} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            # Update class counts
            if class_name in class_counts:
                class_counts[class_name] += 1

            # Check if class name is "Tiger" or "Elephant" and confidence > 0.70
            if (class_name == "Tiger" or class_name == "Elephant") and conf > 0.70:
                pygame.mixer.init()
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play(-1)
                pygame.time.wait(100)
            else:
                pygame.mixer.init()
                pygame.mixer.music.stop()

    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    # Get the current date and format it as "day - month - year"
    current_date = datetime.now().strftime("%d/%B/%Y")

    # Get the current time and format it as "hh:mm:ss"
    current_time = datetime.now().strftime("%H:%M:%S")

    # Print class names, counts, date, and time to the text file
    for class_name, count in class_counts.items():
        if count > 0:
            data = f"{class_name} - {count} - {current_date} - {current_time}\n"
            text_file.write(data)
            print(data)

    cv2.imshow("Image", img)

    # Check for key press 'q' to exit the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Close the text file
text_file.close()

# Release resources and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
