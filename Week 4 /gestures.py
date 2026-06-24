import math


def _distance(lm_list, p1, p2):
    x1, y1 = lm_list[p1][1], lm_list[p1][2]
    x2, y2 = lm_list[p2][1], lm_list[p2][2]

    return math.hypot(
        x2 - x1,
        y2 - y1
    )


def _hand_scale(lm_list):

    ref = _distance(
        lm_list,
        0,
        9
    )

    if ref == 0:
        return 1

    return ref


def fingers_up(
    lm_list,
    hand_label="Right"
):

    fingers = []

    # Thumb

    if hand_label == "Right":

        if lm_list[4][1] > lm_list[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    else:

        if lm_list[4][1] < lm_list[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    # Index Middle Ring Pinky

    tip_ids = [8, 12, 16, 20]

    for tip in tip_ids:

        if lm_list[tip][2] < lm_list[tip - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def classify(
    lm_list,
    hand_label="Right"
):

    if len(lm_list) < 21:
        return "NONE"

    fingers = fingers_up(
        lm_list,
        hand_label
    )

    scale = _hand_scale(lm_list)

    pinch_distance = (
        _distance(lm_list, 4, 8)
        / scale
    )

    # OK Sign

    if (
        pinch_distance < 0.3
        and fingers[2]
        and fingers[3]
        and fingers[4]
    ):
        return "OK"

    # Fist

    if fingers == [0, 0, 0, 0, 0]:
        return "FIST"

    # Open Palm

    if fingers == [1, 1, 1, 1, 1]:
        return "OPEN_PALM"

    # Point

    if fingers == [0, 1, 0, 0, 0]:
        return "POINT"

    # Peace

    if fingers == [0, 1, 1, 0, 0]:
        return "PEACE"

    # Thumbs Up

    if fingers == [1, 0, 0, 0, 0]:
        return "THUMB"

    return "UNKNOWN"
