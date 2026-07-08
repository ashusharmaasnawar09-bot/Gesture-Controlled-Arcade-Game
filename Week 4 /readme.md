# Week 4: Gesture Logic & Building the Gesture Module

## Overview

In Week 4, the focus shifted from simply detecting whether fingers were open or closed to understanding the **geometry of the hand**. Instead of treating the hand as five fingers, it is now treated as **21 landmark points in 2D space**. Using the relative positions and distances between these landmarks, more reliable and reusable gesture recognition can be implemented.

This week also introduced a dedicated **`gestures.py`** module that encapsulates all gesture recognition logic, making it easy to reuse across multiple projects.

---

## Learning Objectives

- Understand geometric relationships between hand landmarks
- Calculate Euclidean distance between landmarks
- Normalize distances to make gesture detection camera-distance independent
- Handle left and right hands correctly using MediaPipe Handedness
- Build a reusable `gestures.py` module
- Classify multiple hand gestures
- Test gesture recognition using a standalone script
- Build a gesture-controlled volume controller

---

# 1. Thinking of the Hand as Geometry

In previous weeks, gesture recognition was based only on whether fingers were **up** or **down**.

This week, the hand is treated as **21 points in a 2D coordinate system**.

This allows us to answer questions such as:

- Are two fingers touching?
- How far apart are they?
- Is the hand making a pinch gesture?
- Can gesture detection work regardless of the hand's distance from the camera?

---

# 2. Measuring Distance Between Landmarks

The distance between any two landmarks can be calculated using the Euclidean distance formula.

```
Distance = √((x₂ - x₁)² + (y₂ - y₁)²)
```

Python provides this calculation directly through:

```python
math.hypot(dx, dy)
```

Example:

```python
distance(lm_list, 4, 8)
```

Measures the distance between

- Thumb Tip (Landmark 4)
- Index Finger Tip (Landmark 8)

Implementation:

```python
def distance(lm_list, p1, p2):
    x1, y1 = lm_list[p1][1], lm_list[p1][2]
    x2, y2 = lm_list[p2][1], lm_list[p2][2]
    return math.hypot(x2 - x1, y2 - y1)
```

---

# 3. Why Raw Pixel Distance Fails

Suppose two users perform the exact same pinch gesture.

**Person A**

- Close to the camera
- Thumb distance = 80 pixels

**Person B**

- Far from the camera
- Thumb distance = 30 pixels

Although the gesture is identical, the measured pixel distance is different.

Using a fixed threshold such as

```python
if distance < 40:
```

will work for one user but fail for another.

---

# 4. Normalization

The solution is **Normalization**.

Instead of comparing raw pixel distances, divide the distance by a reference length that scales with the hand size.

A good reference is the distance between:

- Wrist (Landmark 0)
- Middle Finger MCP (Landmark 9)

```python
def normalized_distance(lm_list, p1, p2):
    ref = distance(lm_list, 0, 9)

    if ref == 0:
        return 0

    return distance(lm_list, p1, p2) / ref
```

Example

```
Hand Size = 150 pixels

Thumb Distance = 45 pixels

Normalized Distance

45 / 150 = 0.30
```

This ratio remains nearly constant even if the hand moves closer to or farther from the camera.

---

# 5. Handedness

The thumb moves sideways, unlike the other fingers.

During Week 3, thumb detection assumed only the right hand.

```python
if thumb_tip_x > thumb_joint_x:
    thumb = 1
```

This works correctly only for the **right hand**.

For the left hand, the comparison becomes the opposite.

MediaPipe automatically predicts whether a detected hand is **Left** or **Right**.

After processing:

```python
results = hands.process(rgb)
```

The handedness information is stored in:

```python
results.multi_handedness
```

Extracting the label:

```python
label = results.multi_handedness[0].classification[0].label
```

Possible outputs:

```
Left
Right
```

---

# 6. Why `cv2.flip()` Matters

Most webcam applications mirror the webcam image.

```python
frame = cv2.flip(frame, 1)
```

Without flipping, raising the right hand appears on the left side of the screen.

Flipping the frame creates a mirror effect, making interaction more natural.

Since the image is mirrored, correct thumb detection must consider whether the detected hand is left or right.

---

# 7. Correct Thumb Detection

```python
def thumb_up(lm_list, hand_label):

    if hand_label == "Right":
        return lm_list[4][1] > lm_list[3][1]

    else:
        return lm_list[4][1] < lm_list[3][1]
```

This works correctly for both hands.

---

# 8. Building `gestures.py`

Instead of writing gesture recognition logic inside every project, a dedicated module is created.

```
gestures.py
```

Any future project can simply import it.

```python
import gestures

gesture = gestures.classify(lm_list)
```

This modular design improves readability, maintainability, and code reuse.

---

# 9. Helper Functions

### `_distance()`

Calculates Euclidean distance between two landmarks.

```python
def _distance(lm_list, p1, p2):
```

The leading underscore indicates that this function is intended for internal use.

---

### `_hand_scale()`

Computes a reference hand size.

```python
def _hand_scale(lm_list):
```

The wrist-to-middle-knuckle distance is used as the scaling reference.

---

# 10. Detecting Finger States

```python
def fingers_up(lm_list, hand_label="Right"):
```

Returns

```
[Thumb, Index, Middle, Ring, Pinky]
```

where

```
1 = Finger Up

0 = Finger Folded
```

Thumb detection depends on handedness.

The remaining four fingers compare the fingertip with the PIP joint using y-coordinates.

---

# 11. Gesture Classification

The main function is

```python
classify(lm_list, hand_label)
```

The first step is a safety check.

```python
if not lm_list or len(lm_list) < 21:
    return "NONE"
```

This prevents crashes when no hand is detected.

---

# 12. Pinch Detection

A pinch gesture is detected by measuring the normalized distance between

- Thumb Tip (4)
- Index Finger Tip (8)

```python
pinch = _distance(lm_list, 4, 8) / scale
```

If

```python
pinch < 0.3
```

and the remaining fingers are open,

the gesture is classified as

```
OK
```

---

# 13. Supported Gestures

| Finger Pattern | Gesture |
|---------------|----------|
| [0,0,0,0,0] | FIST |
| [1,1,1,1,1] | OPEN PALM |
| [0,1,0,0,0] | POINT |
| [0,1,1,0,0] | PEACE |
| [1,0,0,0,0] | THUMB |
| Pinch | OK |

Any unmatched pattern returns

```
UNKNOWN
```

---

# 14. Testing the Gesture Module

A separate testing script (`test_gesture.py`) was created.

Workflow:

```
Open Webcam
      │
      ▼
Detect Hand
      │
      ▼
Extract Landmarks
      │
      ▼
Detect Left/Right Hand
      │
      ▼
Classify Gesture
      │
      ▼
Display Gesture Name
```

This script verifies that the gesture recognition module functions correctly before integrating it into larger applications.

---

# 15. Mini Project: Gesture-Based Volume Control

The concepts learned this week were applied to build a **gesture-controlled system volume controller**.

The application measures the distance between:

- Thumb Tip (Landmark 4)
- Index Finger Tip (Landmark 8)

The measured distance is then mapped to the computer's system volume.

Workflow:

```
Capture Webcam Frame
        │
        ▼
Detect Hand
        │
        ▼
Locate Thumb & Index Tips
        │
        ▼
Measure Distance
        │
        ▼
Map Distance to Volume
        │
        ▼
Update System Volume
        │
        ▼
Display Volume Bar
```

### Windows Implementation

The Windows version uses **PyCAW** to control the system master volume.

Key concepts learned:

- Windows Audio Endpoint API
- PyCAW
- Volume interpolation
- Real-time volume updates

---

### macOS Implementation

On macOS, system volume is controlled using **AppleScript** executed from Python.

```python
osascript
```

The gesture logic remains identical; only the operating system interface changes.

---

# Concepts Learned

- Euclidean Distance
- Geometry-Based Gesture Recognition
- Distance Normalization
- Camera Distance Invariance
- MediaPipe Handedness
- Left vs Right Thumb Detection
- Modular Programming
- Helper Functions
- Gesture Classification
- Pinch Detection
- Webcam Mirroring
- System Volume Control
- Cross-Platform Gesture Applications

---

# Key Takeaways

- Treated the hand as a collection of 21 geometric landmarks instead of simply open or closed fingers.
- Implemented Euclidean distance calculations between landmarks.
- Learned why normalization is essential for camera-distance independent gesture recognition.
- Used MediaPipe Handedness to correctly detect thumb orientation for both left and right hands.
- Built a reusable `gestures.py` module for gesture recognition.
- Added support for pinch-based gesture detection.
- Created a standalone gesture testing application.
- Applied gesture recognition to build a real-time system volume controller.
- Explored both Windows (PyCAW) and macOS (AppleScript) implementations for controlling system volume.

---

# Learning Outcome

By the end of Week 4, I understood how geometric relationships between hand landmarks can be used to build robust gesture recognition systems. I learned how to normalize distances, correctly handle left and right hands, organize gesture logic into reusable modules, and apply these concepts to real-world applications such as gesture-controlled system volume adjustment. These concepts provide the foundation for developing more advanced gesture-controlled games and human-computer interaction systems in the following weeks.
