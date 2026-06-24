import cv2
import mediapipe as mp

import gestures


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb)

    gesture = "NONE"

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        hand_label = "Right"

        if results.multi_handedness:

            hand_label = (
                results
                .multi_handedness[0]
                .classification[0]
                .label
            )

        h, w, _ = frame.shape

        lm_list = []

        for idx, lm in enumerate(hand.landmark):

            cx = int(lm.x * w)
            cy = int(lm.y * h)

            lm_list.append(
                [idx, cx, cy]
            )

        gesture = gestures.classify(
            lm_list,
            hand_label
        )

        print(gesture)

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

    cv2.putText(
        frame,
        gesture,
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Gesture Testing",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
