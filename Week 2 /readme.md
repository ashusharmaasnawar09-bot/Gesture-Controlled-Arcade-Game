# Week 2: Introduction to MediaPipe

## What is MediaPipe?

MediaPipe is Google's cross-platform framework for building real-time perception pipelines.

It provides pre-trained machine learning models for:

* Hand Tracking
* Face Detection
* Face Mesh
* Pose Estimation
* Object Detection

For this project, the focus is on MediaPipe Hands.

---

## MediaPipe Hands

MediaPipe Hands is a real-time hand tracking solution that detects and tracks hand landmarks directly from webcam frames.

The framework returns 21 landmark points for each detected hand.

These landmarks can later be used for gesture recognition.

---

## 21 Hand Landmarks

MediaPipe provides coordinates for:

* Wrist
* Thumb (4 landmarks)
* Index Finger (4 landmarks)
* Middle Finger (4 landmarks)
* Ring Finger (4 landmarks)
* Pinky Finger (4 landmarks)

Total: 21 landmarks

Each landmark contains:

* x coordinate
* y coordinate
* z coordinate

---

## Concepts Learned

### Hand Detection

Detecting hand presence in webcam frames.

### Hand Landmark Detection

Extracting all 21 landmark coordinates.

### Landmark Visualization

Drawing landmarks and hand connections on live video.

### Coordinate Extraction

Reading x, y and z values of every detected landmark.

---

## Key Functions Used

* mp.solutions.hands.Hands()
* hands.process()
* mp.solutions.drawing_utils.draw_landmarks()
* cv2.VideoCapture()
* cv2.cvtColor()

---


* Configure MediaPipe in Python.
* Detect hands in real time.
* Visualize the hand skeleton.
* Extract all 21 landmark coordinates.
* Build the foundation required for gesture recognition in later weeks.
