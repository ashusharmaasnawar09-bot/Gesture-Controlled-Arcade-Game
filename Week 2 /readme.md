# Week 2: Introduction to MediaPipe

## Additional OpenCV Concepts Explored

Before transitioning completely to MediaPipe, several important computer vision concepts in OpenCV were explored.

### Webcam Video Capture

Learned how to:

* Access the system webcam using `cv2.VideoCapture()`
* Read frames continuously using `cap.read()`
* Display live video streams
* Handle keyboard events using `cv2.waitKey()`
* Release resources using `cap.release()`

### Video Recording

Implemented video recording using:

* `cv2.VideoWriter()`
* `cv2.VideoWriter_fourcc()`

Concepts learned:

* Frame width and height extraction
* Frames Per Second (FPS)
* Video codecs and compression

Common codecs studied:

* XVID
* MJPG
* MP4V
* H264

### Image Smoothing and Noise Reduction

#### Gaussian Blur

Used for smoothing images by applying a weighted average to neighboring pixels.

Concepts:

* Kernel size
* Sigma value
* Noise reduction

#### Median Blur

Used for removing salt-and-pepper noise.

Concepts:

* Median filtering
* Edge preservation

### Image Sharpening

Implemented sharpening using custom convolution kernels and `cv2.filter2D()`.

Concepts:

* Kernel matrices
* Edge enhancement
* Image depth (`ddepth`)

### Edge Detection

#### Canny Edge Detection

Used to detect object boundaries.

Concepts:

* Intensity gradients
* Low threshold
* High threshold
* Hysteresis thresholding

### Thresholding

Converted grayscale images into binary images using:

* `cv2.threshold()`

Concepts:

* Binary segmentation
* Threshold value
* Maximum pixel value

### Bitwise Operations

Learned image masking and image combination techniques using:

* `cv2.bitwise_and()`
* `cv2.bitwise_or()`
* `cv2.bitwise_not()`

Applications:

* Region extraction
* Object masking
* Image compositing

### Contour Detection

Studied object boundary detection using:

```python
contours, hierarchy = cv2.findContours()
```

Concepts:

* Contours
* Hierarchy
* Parent-child contour relationships

Contour Retrieval Modes:

* RETR_EXTERNAL
* RETR_LIST
* RETR_TREE

Contour Approximation Methods:

* CHAIN_APPROX_NONE
* CHAIN_APPROX_SIMPLE

### Shape Detection

Used:

* `cv2.arcLength()`
* `cv2.approxPolyDP()`

to identify:

* Triangle
* Rectangle
* Pentagon
* Circle

based on the number of approximated contour vertices.

### Face Detection using Haar Cascades

Implemented real-time face detection using OpenCV's pre-trained Haar Cascade classifiers.

Concepts:

* Haar Cascade XML files
* CascadeClassifier
* detectMultiScale()
* Scale Factor
* Min Neighbours

Applications:

* Face Detection
* Attendance Systems
* Real-Time Object Tracking

---

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
