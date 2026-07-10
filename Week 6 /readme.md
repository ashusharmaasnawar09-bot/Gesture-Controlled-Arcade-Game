# Week 6: Gesture-Controlled Snake Game

## Goal

This week focuses on integrating the hand gesture recognition system developed in the previous weeks with the Snake game. Instead of controlling the snake using the keyboard, the game is controlled entirely through real-time hand gestures detected using **MediaPipe Hands** and **OpenCV**.

The objective is to understand how a computer vision application can communicate with a game loop, making the gameplay completely touch-free.

---

# What I Learned

## 1. Integrating Computer Vision with a Game

Before this week, there were two completely independent programs:

### Gesture Detection Program
- Opens the webcam
- Detects a hand
- Recognizes gestures

### Snake Game
- Runs the game
- Reads keyboard input
- Moves the snake
- Draws the game

This week both programs were combined into a single application.

---

## 2. Single Loop Architecture

The entire application runs inside one main loop.

```
while True:

    Read Webcam

          ↓

    Detect Hand

          ↓

    Recognize Gesture

          ↓

    Update Snake Direction

          ↓

      Move Snake

          ↓

      Draw Game

          ↓

   Display Both Windows
```

Every iteration performs both computer vision and game logic sequentially.

---

## 3. Why Single Loop?

This project uses a **single-loop architecture** because:

- Easy to understand
- Easy to debug
- Perfect for beginners
- No synchronization issues
- Suitable for slower games like Snake

Although the overall frame rate depends on MediaPipe's processing speed, Snake does not require extremely high FPS, making this approach practical and reliable.

---

## 4. Threading (Concept)

I also learned another possible architecture called **threading**.

Instead of one loop, two loops run simultaneously.

### Thread 1

```
Read Webcam

↓

Detect Gesture

↓

Store Gesture

↓

Repeat
```

### Thread 2

```
Read Gesture

↓

Move Snake

↓

Draw Game

↓

Repeat
```

The game runs independently of the gesture detector, producing smoother gameplay. However, threading introduces additional concepts such as:

- Threads
- Shared variables
- Synchronization
- Locks
- Race conditions

Since these concepts are beyond the scope of this project, the single-loop approach was used.

---

# Gesture Stability Filter

One of the biggest challenges during integration was gesture instability.

When changing from one gesture to another, the hand naturally passes through intermediate poses.

For example:

```
RIGHT

↓

UP

↓

LEFT

↓

DOWN
```

Without any filtering, the snake immediately reacts to every temporary pose, resulting in random direction changes.

To solve this problem, a **stability filter** was implemented.

A gesture is only accepted after it has been detected consistently for multiple consecutive frames.

---

## Stability Variables

```
stable_gesture
```

Stores the gesture that the game actually follows.

---

```
previous_gesture
```

Stores the gesture detected in the previous frame.

---

```
gesture_counter
```

Counts how many consecutive frames contain the same gesture.

---

```
STABILITY_FRAMES
```

Number of consecutive matching frames required before trusting a gesture.

Current value:

```
4 Frames
```

At approximately **18 FPS**, this corresponds to roughly **0.22 seconds**, providing a good balance between responsiveness and stability.

---

# Gesture Recognition

Gesture recognition is performed in two stages.

---

## Finger Counting

The first step is counting how many fingers are extended.

Detected gestures include:

- FIST
- OPEN PALM

These gestures are identified purely from the number of fingers raised.

---

## Direction Detection

Finger count alone cannot distinguish:

- Point Left
- Point Right
- Point Up
- Point Down

because all of them contain exactly one raised finger.

To solve this, the direction of the index finger is calculated.

The following landmarks are used:

- Landmark 5 (Index MCP)
- Landmark 8 (Index Tip)

These two points create a vector representing the pointing direction.

---

## Angle Calculation

The direction vector is computed using

```
dx = tip.x - mcp.x
dy = mcp.y - tip.y
```

Notice that **dy is intentionally reversed** because image coordinates increase downward.

The angle is then calculated using

```
atan2(dy, dx)
```

and converted into degrees.

The resulting angle is grouped into four ranges:

- Point Right
- Point Up
- Point Left
- Point Down

Using angle ranges instead of exact values makes the detector much more tolerant to small hand movements.

---

# Gesture to Game Mapping

| Gesture | Action |
|----------|--------|
| ✊ FIST | Start Game / Restart Game |
| ☝️ POINT UP | Move Up |
| 👇 POINT DOWN | Move Down |
| 👈 POINT LEFT | Move Left |
| 👉 POINT RIGHT | Move Right |
| ✋ OPEN PALM | Pause Game |

Pointing in any direction automatically resumes the game after pausing.

---

# Game Integration

The keyboard controls from Week 5 were replaced by gesture input.

Instead of checking keyboard events,

```
Arrow Key

↓

Change Direction
```

the game now performs

```
Recognized Gesture

↓

Update Direction
```

The snake movement logic itself remains unchanged.

Only the source of the input changed.

---

# Time-Based Snake Movement

The webcam processes frames continuously.

Without limiting the snake's movement speed, the snake would move once every frame, making the game unplayable.

Instead, movement is controlled using

```
pygame.time.get_ticks()
```

The snake moves only after a fixed delay (`MOVE_DELAY`) has elapsed.

This separates:

- Webcam frame rate
- Game movement speed

making the gameplay consistent across different computers and webcams.

---

# Webcam Feedback Window

A separate OpenCV window displays:

- Live webcam feed
- Detected hand landmarks
- Current recognized gesture

This provides immediate visual feedback and greatly simplifies debugging.

---


# Final Outcome

Successfully developed a **Gesture-Controlled Snake Game** where the keyboard is completely replaced by real-time hand gestures.

The project combines **Computer Vision**, **Geometry**, and **Game Development** into a single interactive application while maintaining smooth gameplay through gesture stabilization and time-based movement.
