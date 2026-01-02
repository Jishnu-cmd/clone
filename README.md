# Mirror Clone System using MediaPipe & OpenCV

A real-time mirror clone application that detects and segments a human subject from live video and generates a mirrored clone dynamically using computer vision and machine learning techniques.

## Features

- Real-time human segmentation using MediaPipe
- Mirror clone generation with horizontal flipping
- Live webcam input processing
- Performance optimization for consumer hardware
- Clean exit controls

## Requirements

- Python 3.8+
- Webcam
- Windows/Linux compatible

## Installation

1. Clone or download the project files
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main application:
```bash
python mirror_clone_system.py
```

- The system will automatically detect your webcam
- You'll see a split-screen view with your segmented image and mirror clone
- Press **ESC** to exit

## System Requirements

- Minimum resolution: 640×480
- Target FPS: ≥20
- CPU usage: ≤70% on mid-range systems

## Technical Details

- **Human Segmentation**: MediaPipe Selfie Segmentation
- **Mirror Transform**: OpenCV horizontal flipping
- **Real-time Processing**: Optimized for low latency
- **Background Removal**: Binary masking technique
<img width="1789" height="968" alt="image" src="https://github.com/user-attachments/assets/20b1162f-7fe8-46bd-bf94-86a07e97f8b9" />

## Troubleshooting

- **Low FPS**: Ensure good lighting conditions
- **Poor segmentation**: Position yourself clearly in frame
- **No webcam detected**: Check camera permissions and connections

## Academic Use

This project is designed for:
- Computer Vision coursework
- Final year projects
- AR/VR learning

- Interactive demonstrations
