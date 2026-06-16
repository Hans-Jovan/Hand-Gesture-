import cv2
import mediapipe as mp

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

def get_fingers(hand_landmarks):
    """
    Return:
    [thumb, index, middle, ring, pinky]
    1 = open
    0 = closed
    """

    fingers = []

    # Thumb
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]

    if thumb_tip.x < thumb_ip.x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    finger_tips = [8, 12, 16, 20]

    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def detect_gesture(hand_landmarks):
    fingers = get_fingers(hand_landmarks)

    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]

    # Thumbs Up / Down
    if fingers == [1, 0, 0, 0, 0]:

        if thumb_tip.y < thumb_ip.y:
            return "Thumbs Up"

        elif thumb_tip.y > thumb_ip.y:
            return "Thumbs Down"

    # Number 1
    elif fingers == [0, 1, 0, 0, 0]:
        return "1"

    # Number 2
    elif fingers == [0, 1, 1, 0, 0]:
        return "2"

    # Number 3
    elif fingers == [0, 1, 1, 1, 0]:
        return "3"

    # Number 4
    elif fingers == [0, 1, 1, 1, 1]:
        return "4"

    # High Five
    elif fingers == [1, 1, 1, 1, 1]:
        return "High Five"

    return "Unknown"


while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    gesture = "No Hand"

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            gesture = detect_gesture(hand_landmarks)

    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Hand Gesture Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
