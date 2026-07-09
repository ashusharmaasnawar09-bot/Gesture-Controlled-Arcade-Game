# Week 5: Understanding the Snake Game (Pygame)

## Goal

This week focused on understanding the provided keyboard-controlled Snake Game built using Pygame. The objective was to learn how the game is structured so that keyboard controls can later be replaced with hand gesture controls using MediaPipe in the upcoming weeks.

---

## Key Concepts Learned

### 1. Game Loop

Understood how every game continuously runs inside an infinite loop where it:

- Reads user input
- Updates game state
- Draws all game objects
- Refreshes the display

---

### 2. Event Handling

Learned how Pygame detects keyboard events using:

- Arrow Keys
- Space Bar
- P key
- Quit Event

and how these events control the snake.

---

### 3. Snake Movement

Studied how the snake moves by:

- Creating a new head
- Adding it to the front of the snake
- Removing the tail if food is not eaten
- Keeping the tail when food is eaten to increase the snake's length

---

### 4. Food Generation

Learned how random food positions are generated while ensuring food never appears inside the snake's body.

---

### 5. Collision Detection

Understood how the game checks for:

- Wall collisions
- Self collisions

and ends the game when either occurs.

---

### 6. Score System

Explored how:

- Current Score
- High Score

are updated and displayed during gameplay.

---

### 7. Pause and Restart

Learned how game states are managed to support:

- Pause
- Resume
- Restart after Game Over

without restarting the entire program.

---

### 8. Rendering

Understood how Pygame draws:

- Snake
- Food
- Grid
- Score
- High Score
- Welcome Screen
- Game Over Screen

every frame.

---

## Code Structure

The project is organized into four major sections:

- Initialization
- Event Handling
- Game Logic
- Rendering

This separation makes it easier to replace keyboard controls with gesture controls in future weeks.

---

## Understanding for Future Integration

Instead of directly controlling the snake using keyboard inputs, the game will later receive commands from the gesture recognition module developed in previous weeks.

The overall game logic remains unchanged. Only the input source will be replaced.

Current Input:

```
Keyboard → Direction → Snake Movement
```

Future Input:

```
Hand Gesture → Direction → Snake Movement
```

---

## Outcome

By the end of Week 5, I gained a clear understanding of the internal working of the Snake Game. This prepares me for the next phase of the project, where MediaPipe-based hand gestures will be integrated to control the snake without using the keyboard.
