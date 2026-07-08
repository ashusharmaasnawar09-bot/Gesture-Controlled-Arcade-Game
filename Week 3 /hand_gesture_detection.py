import cv2
import mediapipe as mp




mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mpDraw = mp.solutions.drawing_utils




cap = cv2.VideoCapture(0)


# Function to check which fingers are up

def fingers_up(lm_list):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb (Right Hand + Mirrored Webcam)
    if lm_list[4][1] > lm_list[3][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other four fingers
    for tip in tips[1:]:
        if lm_list[tip][2] < lm_list[tip - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


# Function to classify gesture

def classify_gesture(fingers):

    if fingers == [0, 0, 0, 0, 0]:
        return "FIST"

    elif fingers == [1, 1, 1, 1, 1]:
        return "OPEN PALM"

    elif fingers == [0, 1, 0, 0, 0]:
        return "POINTING"

    elif fingers == [0, 1, 1, 0, 0]:
        return "PEACE"

    elif fingers == [1, 0, 0, 0, 0]:
        return "THUMBS UP"
    elif fingers == [0,0,1,0,0]:
        return "F*ck you"

    else:
        return "UNKNOWN"




while True:

    success, frame = cap.read()

    if not success:
        break

    # Mirror Image
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect Hands
    results = hands.process(rgb)

    lm_list = []

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        # Draw Hand Skeleton
        mpDraw.draw_landmarks(
            frame,
            hand,
            mpHands.HAND_CONNECTIONS
        )

        h, w, c = frame.shape

        # Store Landmark Coordinates
        for id, lm in enumerate(hand.landmark):

            cx = int(lm.x * w)
            cy = int(lm.y * h)

            lm_list.append([id, cx, cy])

            # Draw Landmark Number
            cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        # Gesture Recognition
        fingers = fingers_up(lm_list)

        gesture = classify_gesture(fingers)

      
        print(fingers, gesture)

        # Display Gesture
        cv2.putText(
            frame,
            gesture,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    
    cv2.imshow("Gesture Recognition", frame)

  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




cap.release()
cv2.destroyAllWindows()
