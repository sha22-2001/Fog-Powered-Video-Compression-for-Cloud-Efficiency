from ultralytics import YOLO
import os
import time
import matplotlib.pyplot as plt
from PIL import Image

# Load YOLO models (YOLOv5 'u' model and YOLOv8)
model_yolov5 = YOLO("YOLO_Weights/yolov5lu.pt")
model_yolov8 = YOLO("YOLO_Weights/yolov8l.pt")

# Path to the folder containing images
image_folder = "image"

# Get a list of image file names in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpeg")]

# Create lists to store inference times for YOLOv5 and YOLOv8
times_yolov5 = []
times_yolov8 = []

# Loop through the images and perform inference with both models
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)

    # Load the image
    img = Image.open(image_path)

    # Inference with YOLOv5
    start_time = time.time()
    _ = model_yolov5(img)
    end_time = time.time()
    times_yolov5.append(end_time - start_time)

    # Inference with YOLOv8
    start_time = time.time()
    _ = model_yolov8(img)
    end_time = time.time()
    times_yolov8.append(end_time - start_time)



# Generate a linear graph
plt.figure(figsize=(8, 6))
plt.plot(times_yolov5, label="YOLOv5")
plt.plot(times_yolov8, label="YOLOv8")
plt.xlabel("Image Number")
plt.ylabel("Inference Time (s)")
plt.ylim(0, 1)  # Limit the y-axis to a maximum value of 1
plt.legend()
plt.title("Inference Time Comparison")

# Save the graph with a name indicating the number of images
num_images = len(image_files)
graph_file_name = f"Graph/{num_images}.png"
plt.savefig(graph_file_name)

# Show the graph
plt.show()
