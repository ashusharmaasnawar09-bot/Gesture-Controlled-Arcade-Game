import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

while True:

    ret, frame = cap.read()

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand in results.multi_hand_landmarks:

            for id, lm in enumerate(hand.landmark):

                print(
                    f"Landmark {id}: "
                    f"{lm.x:.3f}, "
                    f"{lm.y:.3f}, "
                    f"{lm.z:.3f}"
                )

    cv2.imshow("Coordinates", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
