import cv2
import time
import math
import numpy as np
import subprocess
import handtracking as htm


wCam, hCam = 640, 480


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detectionCon=0.7)

pTime = 0

volBar = 400
volPer = 0
prevVolume = -1      # prevents sending AppleScript every frame

while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    # Detect hand
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        # Thumb tip
        x1, y1 = lmList[4][1], lmList[4][2]

        # Index finger tip
        x2, y2 = lmList[8][1], lmList[8][2]

        # Midpoint
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw fingertips
        cv2.circle(img, (x1, y1), 12, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 12, (255, 0, 255), cv2.FILLED)

        # Line joining them
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Midpoint
        cv2.circle(img, (cx, cy), 12, (255, 0, 255), cv2.FILLED)

        # Distance
        length = math.hypot(x2 - x1, y2 - y1)

        # Convert distance to percentage
        volPer = np.interp(length, [50, 300], [0, 100])

        # Volume Bar
        volBar = np.interp(length, [50, 300], [400, 150])

        # Convert to integer
        macVolume = int(volPer)

        # Update only if volume changes by at least 2%
        if abs(macVolume - prevVolume) >= 2:

            subprocess.run(
                [
                    "osascript",
                    "-e",
                    f"set volume output volume {macVolume}"
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            prevVolume = macVolume

        # Fingers touching
        if length < 50:
            cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)

    # Volume Bar
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400),
                  (255, 0, 0), cv2.FILLED)

    # Volume %
    cv2.putText(img,
                f'{int(volPer)}%',
                (35, 440),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 0),
                2)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
    pTime = cTime

    cv2.putText(img,
                f'FPS: {int(fps)}',
                (10, 40),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 255),
                2)

    cv2.imshow("Gesture Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
