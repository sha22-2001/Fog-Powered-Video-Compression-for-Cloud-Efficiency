from ultralytics import YOLO
import cv2
import os
import matplotlib.pyplot as plt
import torch

# Load the YOLO models (YOLOv5lu and another YOLOv8 model)
model_yolov5lu = YOLO("YOLO_Weights/yolov5lu.pt")
model_yolov8 = YOLO("YOLO_Weights/yolov8l.pt")

# Path to the folder containing images
image_folder = "image"  # Replace with the path to your image folder

classNames = ["person", "", "car", "motorbike", "", "Tiger", "train", "truck", "",
              "", "", "", "", "", "", "Tiger",
              "Tiger", "", "", "Cow", "Elephant", "Bear", "Tiger", "Leopard", "", "", ]

# Lists to store the average confidences for each model
average_confidences_yolov5lu = []
average_confidences_yolov8 = []
image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpeg")]

# Create a folder to save the graphs
os.makedirs("Graphs", exist_ok=True)

# Process each image in the folder for YOLOv5lu
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    img = cv2.imread(image_path)
    results = model_yolov5lu(img)

    total_confidence = 0
    object_count = 0

    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = box.conf[0].cpu().item()  # Move to CPU and convert to a float
            if conf > 0.7:
                total_confidence += conf
                object_count += 1

    # Calculate the average confidence for the image and store it for YOLOv5lu
    if object_count > 0:
        average_confidence = total_confidence / object_count
    else:
        average_confidence = 0

    average_confidences_yolov5lu.append(average_confidence)

# Process each image in the folder for YOLOv8
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    img = cv2.imread(image_path)
    results = model_yolov8(img)

    total_confidence = 0
    object_count = 0

    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = box.conf[0].cpu().item()  # Move to CPU and convert to a float
            if conf > 0.7:
                total_confidence += conf
                object_count += 1

    # Calculate the average confidence for the image and store it for YOLOv8
    if object_count > 0:
        average_confidence = total_confidence / object_count
    else:
        average_confidence = 0

    average_confidences_yolov8.append(average_confidence)

# Create a linear graph to display both sets of average confidences
plt.figure(figsize=(8, 6))
plt.plot(average_confidences_yolov5lu, marker='o', linestyle='-', color='b', label='YOLOv5lu')
plt.plot(average_confidences_yolov8, marker='o', linestyle='-', color='r', label='YOLOv8')
plt.xlabel("Image Number")
plt.ylabel("Average Confidence")
plt.title("Average Confidence Scores for Images")
plt.grid(True)
plt.legend()

# Save the graph with a filename indicating the number of images processedw
num_images = len(image_files)
graph_file_name = f"Graph/{num_images}-Conf.png"
plt.savefig(graph_file_name)

# Display the graph
plt.show()

# Determine which model is best based on average confidence values
best_model = "YOLOv5lu" if max(average_confidences_yolov5lu) > max(average_confidences_yolov8) else "YOLOv8"
print(f"The best model is {best_model}")
