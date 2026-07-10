import cv2 as cv
import mediapipe as mp
import pygame
import random
import sys
import math


# 1. INITIALIZATION & CONFIGURATION


#  MediaPipe Setup (Solutions API ) 
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

#  PyGame Grid / Window Settings 
CELL_SIZE   = 30
GRID_WIDTH  = 30
GRID_HEIGHT = 22
WIDTH       = CELL_SIZE * GRID_WIDTH
HEIGHT      = CELL_SIZE * GRID_HEIGHT

#  Colors 
BG_COLOR     = (15, 15, 25)
SNAKE_HEAD   = (0, 230, 120)
SNAKE_BODY   = (0, 170, 90)
FOOD_COLOR   = (240, 70, 90)
TEXT_COLOR   = (235, 235, 245)
GRID_COLOR   = (30, 30, 45)


#  Helper Functions 
def random_food(snake):
    while True:
        pos = (random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3))
        if pos not in snake:
            return pos

def draw_cell(surface, pos, color):
    x = pos[0] * CELL_SIZE
    y = pos[1] * CELL_SIZE
    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BG_COLOR, rect, 1)


# 2. MAIN APPLICATION LOOP

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gesture Controlled Snake")
    font = pygame.font.SysFont("consolas", 22)
    big_font = pygame.font.SysFont("consolas", 40, bold=True)

    cap = cv.VideoCapture(0)


    # Game State Initialization 
    def reset_game():
        start = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        return [start], (1, 0), random_food([start]), 0

    snake, direction, food, score = reset_game()
    game_over = False
    is_paused = False
    game_started = False    # True only after the player makes a FIST on the welcome screen
    high_score = 0          # resets to 0 every time the program starts

    #GAME SPEED CONTROL
    # We want the snake to move every 150 milliseconds (roughly 6-7 times a second).
    # You can increase this number (e.g., 200) to make it even slower and easier!
    MOVE_DELAY_START = 150               # starting speed (ms between steps)
    MOVE_DELAY_MIN = 80                  # fastest the snake can ever get
    SPEED_STEP = 5                       # how many ms to shave off per food eaten
    MOVE_DELAY = MOVE_DELAY_START        # current delay, will shrink as score grows
    last_move_time = pygame.time.get_ticks()

    # Gesture Stability Variables
    stable_gesture = "NONE"
    previous_gesture = "NONE"
    gesture_counter = 0
    STABILITY_FRAMES = 4

    while True:

        #CAPTURE & PROCESS GESTURE (Runs at max webcam speed)

        success, frame = cap.read()
        if not success:
            print("Camera not found")
            break

        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        angle = 0.0

        if results.multi_hand_landmarks:
            handLms = results.multi_hand_landmarks[0].landmark
            # Solutions API gives handedness via multi_handedness, one entry per detected hand
            handedness_label = results.multi_handedness[0].classification[0].label
            handedness_label = "Left" if handedness_label == "Right" else "Right"

            thumb_tip, thumb_ip = handLms[4], handLms[3]
            index_tip, index_mcp = handLms[8], handLms[5]

            fingers_up = []
            if handedness_label == "Right":
                fingers_up.append(thumb_tip.x < thumb_ip.x)
            else:
                fingers_up.append(thumb_tip.x > thumb_ip.x)

            for tip_id, pip_id in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                fingers_up.append(handLms[tip_id].y < handLms[pip_id].y)

            count = sum(fingers_up)

            dx = index_tip.x - index_mcp.x
            dy = index_mcp.y - index_tip.y
            angle = math.degrees(math.atan2(dy, dx))

            if count == 0:
                gesture = "FIST"
            elif count == 5:
                gesture = "OPEN PALM"
            else:
                if -60 <= angle <= 60:
                    gesture = "POINT RIGHT"
                elif 60 < angle < 120:
                    gesture = "POINT UP"
                elif angle >= 120 or angle <= -120:
                    gesture = "POINT LEFT"
                else:
                    gesture = "POINT DOWN"

            if gesture == previous_gesture:
                gesture_counter += 1
            else:
                gesture_counter = 1
                previous_gesture = gesture

            if gesture_counter >= STABILITY_FRAMES:
                stable_gesture = gesture


        # EVENT HANDLING & DIRECTION UPDATES

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()

        # Direction tracking changes instantly when you point
        if not game_started:
            if stable_gesture == "FIST":
                game_started = True
                snake, direction, food, score = reset_game()
                stable_gesture = "NONE"
                last_move_time = pygame.time.get_ticks() # Reset clock
                MOVE_DELAY = MOVE_DELAY_START   # reset speed on restart
        elif game_over:
            if stable_gesture == "FIST":
                snake, direction, food, score = reset_game()
                game_over = False
                stable_gesture = "NONE"
                last_move_time = pygame.time.get_ticks() # Reset clock
                MOVE_DELAY = MOVE_DELAY_START   # reset speed on restart
        else:
            if stable_gesture == "OPEN PALM":
                is_paused = True
            elif stable_gesture in ["POINT UP", "POINT DOWN", "POINT LEFT", "POINT RIGHT"]:
                is_paused = False

            if not is_paused:
                if stable_gesture == "POINT UP" and direction != (0, 1):
                    direction = (0, -1)
                elif stable_gesture == "POINT DOWN" and direction != (0, -1):
                    direction = (0, 1)
                elif stable_gesture == "POINT LEFT" and direction != (1, 0):
                    direction = (-1, 0)
                elif stable_gesture == "POINT RIGHT" and direction != (-1, 0):
                    direction = (1, 0)

        #  UPDATE GAME STATE (THROTTLED STEP UPDATE) 
        current_time = pygame.time.get_ticks()

        # NEW: TIME CHECK 
        # Only advance the game mechanics if enough milliseconds have passed!
        if game_started and not game_over and not is_paused and (current_time - last_move_time > MOVE_DELAY):
            last_move_time = current_time # Reset time anchor for next step

            head = snake[0]
            new_head = (head[0] + direction[0], head[1] + direction[1])

            hit_wall = (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT)
            hit_self = new_head in snake

            if hit_wall or hit_self:
                game_over = True
                if score > high_score:      # update high score when the game ends
                    high_score = score
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food(snake)
                    MOVE_DELAY = max(MOVE_DELAY_MIN, MOVE_DELAY - SPEED_STEP)      #speed up, but never below minimum
                else:
                    snake.pop()


        # RENDERING (Always updates smoothly)

        screen.fill(BG_COLOR)

        if not game_started:
            #  WELCOME SCREEN 
            title_surf = big_font.render("GESTURE SNAKE", True, SNAKE_HEAD)
            sub_surf = font.render("Make a FIST to start", True, TEXT_COLOR)
            screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, HEIGHT//2 - 40))
            screen.blit(sub_surf, (WIDTH//2 - sub_surf.get_width()//2, HEIGHT//2 + 20))

        else:
            for gx in range(GRID_WIDTH):
                pygame.draw.line(screen, GRID_COLOR, (gx*CELL_SIZE, 0), (gx*CELL_SIZE, HEIGHT))
            for gy in range(GRID_HEIGHT):
                pygame.draw.line(screen, GRID_COLOR, (0, gy*CELL_SIZE), (WIDTH, gy*CELL_SIZE))

            draw_cell(screen, food, FOOD_COLOR)
            for i, segment in enumerate(snake):
                color = SNAKE_HEAD if i == 0 else SNAKE_BODY
                draw_cell(screen, segment, color)

            score_surf = font.render(f"Score: {score} | Gesture: {stable_gesture}", True, TEXT_COLOR)
            hs_surf = font.render(f"Best: {high_score}", True, (255, 215, 0))    # gold color
            screen.blit(score_surf, (8, 6))
            screen.blit(hs_surf, (WIDTH - hs_surf.get_width() - 8, 6))    # pin to top right corner


            if is_paused and not game_over:
                pause_surf = big_font.render("PAUSED", True, TEXT_COLOR)
                sub_surf = font.render("Point in any direction to resume", True, TEXT_COLOR)
                screen.blit(pause_surf, (WIDTH//2 - pause_surf.get_width()//2, HEIGHT//2 - 40))
                screen.blit(sub_surf, (WIDTH//2 - sub_surf.get_width()//2, HEIGHT//2 + 15))

            if game_over:
                msg = big_font.render("GAME OVER", True, FOOD_COLOR)
                sub = font.render("Make a FIST to restart", True, TEXT_COLOR)
                screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 40))
                screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 15))

        pygame.display.flip()

        cv.putText(frame, f"Gesture: {stable_gesture}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv.imshow("Vision Tracking Feedback", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    hands.close()
    cap.release()
    cv.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()
