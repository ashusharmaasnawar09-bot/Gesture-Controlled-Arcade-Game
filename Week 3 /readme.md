# Week 3: Hand Landmark Detection and Gesture Recognition


## Hand Landmark Model

MediaPipe Hands returns 21 landmarks for each detected hand.

Landmark Indexing:

0  -> Wrist

Thumb:
1 -> 2 -> 3 -> 4

Index Finger:
5 -> 6 -> 7 -> 8

Middle Finger:
9 -> 10 -> 11 -> 12

Ring Finger:
13 -> 14 -> 15 -> 16

Pinky Finger:
17 -> 18 -> 19 -> 20

Important fingertip indices:

4
8
12
16
20

---

## Coordinate System

MediaPipe returns normalized coordinates.

x ∈ [0,1]
y ∈ [0,1]

Conversion to pixel coordinates:

px = int(x * frame_width)

py = int(y * frame_height)

z coordinate represents relative depth.

---

## Hand Tracking Pipeline

Webcam Frame
      ↓
BGR → RGB Conversion
      ↓
MediaPipe Processing
      ↓
21 Landmark Detection
      ↓
Coordinate Extraction
      ↓
Gesture Classification
      ↓
Gesture Visualization

---

## Basic Gesture Logic

Finger is considered UP if:

tip_y < pip_y

because image coordinates increase downward.

Example:

Index Finger

tip = landmark 8

pip = landmark 6

Condition:

landmark[8].y < landmark[6].y

---

## Gestures Implemented

1. FIST

[0,0,0,0,0]

2. OPEN PALM

[1,1,1,1,1]

3. POINTING

[0,1,0,0,0]

4. PEACE

[0,1,1,0,0]

5. THUMBS UP

[1,0,0,0,0]
