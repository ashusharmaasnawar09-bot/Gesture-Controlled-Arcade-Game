# Week 4: Gesture Logic and Gesture Module


### Finger Up Detection

A finger is considered up if:

tip_y < pip_y

Examples:

Index:

Landmark 8 < Landmark 6

Middle:

Landmark 12 < Landmark 10

---

### Euclidean Distance

Distance between two landmarks:

distance =
sqrt(
(x2-x1)^2 +
(y2-y1)^2
)

Used for:

- Pinch detection
- OK gesture
- Future game controls

---

### Relative Position

Used for:

- Thumb detection
- Hand orientation
- Directional gestures

---

## Distance Normalization

Problem:

Raw pixel distance changes when hand moves closer or farther from camera.

Solution:

Normalize by hand size.

Reference:

Wrist (0)
to
Middle MCP (9)

normalized_distance =
distance / hand_scale

Benefits:

- Camera distance invariant
- More robust gesture recognition

---

## Handedness

MediaPipe provides:

Left
Right

Thumb logic changes depending on handedness.

Right Hand:

thumb_tip_x > thumb_joint_x

Left Hand:

thumb_tip_x < thumb_joint_x

---

## Gestures Implemented

1. FIST

[0,0,0,0,0]

2. OPEN_PALM

[1,1,1,1,1]

3. POINT

[0,1,0,0,0]

4. PEACE

[0,1,1,0,0]

5. THUMB

[1,0,0,0,0]

6. OK

Thumb tip near index tip
(normalized distance)

---

## Software Design

The module exposes one public function:

classify(lm_list, hand_label)

Input:

Hand landmarks

Output:

Gesture name string

Examples:

OPEN_PALM
PEACE
POINT
FIST
OK
