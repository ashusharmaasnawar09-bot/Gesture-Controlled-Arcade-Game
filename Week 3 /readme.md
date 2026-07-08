# Week 3: Hand Tracking Module & Gesture Recognition

## Overview

This week focused on understanding how **MediaPipe Hands** works, creating a reusable **Hand Tracking Module**, and implementing the basic logic required for **gesture recognition**. Instead of writing all the code in a single file, the project was organized into reusable modules that can be imported into future projects.

---

## Learning Objectives

- Understand MediaPipe Hands
- Learn Object-Oriented Programming (OOP) in Python
- Build a reusable Hand Tracking Module
- Detect hand landmarks
- Extract landmark coordinates
- Detect which fingers are open or closed
- Classify simple hand gestures

---

# 1. MediaPipe Hands

MediaPipe provides several pre-trained computer vision models called **Solutions**.

```
mediapipe
│
├── solutions
│      ├── hands
│      ├── pose
│      ├── face_detection
│      ├── face_mesh
│      └── selfie_segmentation
```

Each solution performs a different task.

| Solution | Purpose |
|----------|----------|
| Hands | Detect hands |
| Pose | Detect body joints |
| Face Detection | Detect faces |
| Face Mesh | Detect detailed facial landmarks |
| Selfie Segmentation | Background segmentation |

### Initializing MediaPipe Hands

```python
mpHands = mp.solutions.hands
hands = mpHands.Hands()
```

By default, MediaPipe uses:

```python
Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
```

### Parameter Explanation

| Parameter | Description |
|------------|-------------|
| static_image_mode | False means continuous webcam/video detection |
| max_num_hands | Maximum number of hands to detect |
| min_detection_confidence | Minimum confidence required for initial detection |
| min_tracking_confidence | Minimum confidence required for tracking |

---

# 2. Hand Tracking Module

Instead of writing detection logic repeatedly, we created a reusable module called **HandTrackingModule.py**.

This module is responsible for:

- Detecting hands
- Drawing landmarks
- Extracting landmark coordinates
- Returning landmark positions

---

# 3. Program Flow

```
Start Program
      │
      ▼
Import Libraries
      │
      ▼
Create handDetector Class
      │
      ▼
Open Webcam
      │
      ▼
Read Frame
      │
      ▼
Detect Hands
      │
      ▼
Extract Landmarks
      │
      ▼
Display Image
      │
      ▼
Repeat
```

---

# 4. Understanding Classes

```python
class handDetector():
```

A class is a blueprint used to create objects.

Later we create an object using:

```python
detector = handDetector()
```

This object can access every function inside the class.

---

# 5. Constructor (__init__)

```python
def __init__(self,
             mode=False,
             maxHands=2,
             detectionCon=0.5,
             trackCon=0.5):
```

`__init__()` is a constructor.

It is automatically executed whenever an object is created.

Its purpose is to initialize the object's variables.

```python
self.mode = mode
self.maxHands = maxHands
self.detectionCon = detectionCon
self.trackCon = trackCon
```

---

# 6. Understanding `self`

`self` refers to the current object.

For example,

```python
detector = handDetector()
```

Here every `self` points to `detector`.

So,

```python
self.mode
```

actually means

```python
detector.mode
```

Each object has its own copy of these variables.

---

# 7. Creating the MediaPipe Detector

```python
self.mpHands = mp.solutions.hands

self.hands = self.mpHands.Hands(
    self.mode,
    self.maxHands,
    self.detectionCon,
    self.trackCon
)

self.mpDraw = mp.solutions.drawing_utils
```

This initializes the MediaPipe Hands model and the drawing utilities.

---

# 8. Detecting Hands

```python
def findHands(self, img, draw=True):
```

### Step 1

Convert the image from **BGR** to **RGB**.

```python
imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

MediaPipe expects RGB images.

---

### Step 2

Process the image.

```python
self.results = self.hands.process(imgRGB)
```

MediaPipe detects all visible hands and predicts their landmarks.

---

### Step 3

Check if a hand exists.

```python
if self.results.multi_hand_landmarks:
```

---

### Step 4

Loop through every detected hand.

```python
for handLms in self.results.multi_hand_landmarks:
```

---

### Step 5

Draw landmarks.

```python
self.mpDraw.draw_landmarks(
    img,
    handLms,
    self.mpHands.HAND_CONNECTIONS
)
```

This draws all **21 landmarks** and their connections.

---

# 9. Finding Landmark Positions

```python
def findPosition(self, img, handNo=0, draw=True):
```

This function extracts all 21 landmark coordinates.

```python
for id, lm in enumerate(myHand.landmark):
```

Each landmark contains:

- Landmark ID
- x coordinate
- y coordinate
- z coordinate

MediaPipe returns normalized coordinates between **0 and 1**.

To convert them into pixel coordinates:

```python
h, w, c = img.shape

cx = int(lm.x * w)
cy = int(lm.y * h)
```

The coordinates are stored as:

```python
lmList.append([id, cx, cy])
```

Example:

```
[
 [0,320,410],
 [1,326,392],
 ...
]
```

---

# 10. Using the Module

The module can be imported into any project.

```python
import HandTrackingModule as htm
```

Create the detector:

```python
detector = htm.handDetector()
```

Detect hands:

```python
img = detector.findHands(img)
```

Extract landmarks:

```python
lmList = detector.findPosition(img)
```

This keeps the project modular and reusable.

---

# 11. Gesture Recognition

MediaPipe only tells us **where the landmarks are**.

It does not identify gestures.

Gesture recognition is implemented by comparing landmark positions.

---

# 12. Detecting Which Fingers Are Up

```python
def fingers_up(lm_list):
```

Returns a list of five values.

```
[Thumb, Index, Middle, Ring, Pinky]
```

where

```
1 = Finger Up
0 = Finger Folded
```

Example:

```
[1,1,0,0,1]
```

means

- Thumb → Up
- Index → Up
- Middle → Down
- Ring → Down
- Pinky → Up

---

# 13. Fingertip Landmark IDs

MediaPipe assigns fixed IDs.

```python
tips = [4, 8, 12, 16, 20]
```

| Finger | Landmark ID |
|----------|------------|
| Thumb | 4 |
| Index | 8 |
| Middle | 12 |
| Ring | 16 |
| Pinky | 20 |

---

# 14. Thumb Detection

The thumb bends sideways.

Therefore, we compare **x coordinates**.

```python
fingers.append(
    1 if lm_list[4][1] > lm_list[3][1] else 0
)
```

This uses Python's **ternary operator**.

Equivalent code:

```python
if lm_list[4][1] > lm_list[3][1]:
    fingers.append(1)
else:
    fingers.append(0)
```

---

# 15. Detecting Other Fingers

The remaining fingers bend vertically.

Therefore, compare **y coordinates**.

```python
for tip in tips[1:]:
```

`tips[1:]` skips the thumb.

```python
fingers.append(
    1 if lm_list[tip][2] < lm_list[tip-2][2] else 0
)
```

If the fingertip is above its PIP joint, the finger is considered **open**.

Otherwise, it is considered **closed**.

---

# 16. Gesture Classification

Once finger states are known, gestures can be classified.

Supported gestures:

| Finger Pattern | Gesture |
|----------------|----------|
| [0,0,0,0,0] | FIST |
| [1,1,1,1,1] | OPEN PALM |
| [0,1,0,0,0] | POINTING |
| [0,1,1,0,0] | PEACE |
| [1,0,0,0,0] | THUMBS UP |

Any unmatched pattern returns:

```
UNKNOWN
```

---

# 17. Integrating Gesture Recognition

Inside the webcam loop:

```python
if lm_list:
    fingers = fingers_up(lm_list)
    gesture = classify_gesture(fingers)

    print(fingers, gesture)

    cv2.putText(
        frame,
        gesture,
        (20,60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0,255,0),
        2
    )
```

Workflow:

```
Capture Frame
      │
      ▼
Detect Hand
      │
      ▼
Extract 21 Landmarks
      │
      ▼
Detect Finger States
      │
      ▼
Generate Finger Pattern
      │
      ▼
Classify Gesture
      │
      ▼
Display Gesture
```

---

# Key Takeaways

- Learned how MediaPipe Hands detects and tracks hands.
- Built a reusable Hand Tracking Module.
- Understood Python classes, constructors, and the use of `self`.
- Extracted all 21 hand landmarks.
- Learned the MediaPipe hand landmark numbering system.
- Implemented finger state detection using landmark coordinates.
- Built a basic gesture recognition pipeline.
- Classified simple hand gestures such as **FIST**, **OPEN PALM**, **POINTING**, **PEACE**, and **THUMBS UP**.
- Structured the project into reusable modules for future gesture-controlled applications.

---

# Learning Outcome

By the end of Week 3, I understood how MediaPipe detects hands, how landmark coordinates are extracted, how reusable Python modules are created, and how hand gestures can be recognized by analyzing the relative positions of finger landmarks. This serves as the foundation for building gesture-controlled games in the coming weeks.
