import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not capture frame")
        break

    h, w, c = frame.shape

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb)

    gesture = "No Hand"

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

           
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

        
            landmarks = []

            for id, lm in enumerate(hand_landmarks.landmark):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                landmarks.append((cx, cy))


            if len(landmarks) == 21:

                fingers = []

                # Thumb
                if landmarks[4][0] > landmarks[3][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Index
                if landmarks[8][1] < landmarks[6][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Middle
                if landmarks[12][1] < landmarks[10][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Ring
                if landmarks[16][1] < landmarks[14][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Pinky
                if landmarks[20][1] < landmarks[18][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # 3 Gestures

                # Fist
                if fingers == [0,0,0,0,0]:
                    gesture = "FIST"

                # Open Palm
                elif fingers == [1,1,1,1,1]:
                    gesture = "OPEN PALM"

                # Peace Sign
                elif fingers == [0,1,1,0,0]:
                    gesture = "PEACE"

                # Print Gesture
                print(gesture)

    cv2.putText(
        frame,
        gesture,
        (20,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow(
        "Gesture Detection",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
