# Smart Wildlife Security: Fog-Powered Video Compression for Cloud Efficiency

A cutting-edge solution to address human-wildlife conflicts in rural areas by integrating fog computing and intelligent video compression. The system efficiently captures, processes, and transmits relevant wildlife activity data to the cloud, ensuring resource optimization and enhanced rural security.

---

## Features

- **24/7 Surveillance**: Continuous video capture with intelligent frame extraction and object detection.
- **Fog Computing**: Processes data closer to the source to minimize latency and ensure timely action.
- **Smart Video Compression**: Selectively compresses and transmits relevant data to reduce cloud storage load.
- **Dynamic Data Transmission**: Adaptive algorithms to optimize resource usage and ensure efficient data flow.
- **Comprehensive Reporting**: Generates detailed reports of wildlife activities for monitoring and analysis.
- **Security Measures**: Encryption applied to ensure the safety and confidentiality of transmitted data.

---

## Technologies Used

- **YOLOv8**: For object detection and activity identification.
- **Python**: Core programming language.
- **Socket Programming**: For client-server communication.
- **Fog Computing**: Data processing near the source.
- **Encryption & Compression**: Ensures secure and efficient data transmission.

---

## System Workflow

### 1. Video Capture and Frame Extraction
1. Capture video and convert into frames.
2. Detect objects in each frame using YOLOv8.
3. Track objects and generate trimmed videos with only relevant activities.
4. Enhance security by applying encryption before transmission.

### 2. Data Transmission
1. Encrypt and compress the data.
2. Transmit compressed data to the server.
3. Decrypt and extract the data on the server for storage and analysis.
4. Generate a report summarizing key findings.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/smart-wildlife-security.git
   cd smart-wildlife-security
