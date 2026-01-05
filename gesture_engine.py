import cv2
import mediapipe as mp
import math

class GestureEngine:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=1, 
            min_detection_confidence=0.8, 
            model_complexity=1
        )

    def process_frame(self, img):
        # Convert BGR to RGB for MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        
        current_gesture = "Waiting..."
        hand_info = "None"
        
        if results.multi_hand_landmarks:
            hand_info = results.multi_handedness[0].classification[0].label
            for hand_lms in results.multi_hand_landmarks:
                # Draw the skeleton on the image
                self.mp_drawing.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                lms = hand_lms.landmark

                # --- FINGER DETECTION LOGIC ---
                fingers = []
                # Thumb (Handedness corrected)
                if hand_info == "Right":
                    fingers.append(lms[4].x < lms[3].x)
                else:
                    fingers.append(lms[4].x > lms[3].x)

                # Index, Middle, Ring, Pinky
                for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                    fingers.append(lms[tip].y < lms[pip].y)

                up_count = fingers.count(True)

                # --- GESTURE MAPPING ---
                dist_ok = math.sqrt((lms[4].x-lms[8].x)**2 + (lms[4].y-lms[8].y)**2 + (lms[4].z-lms[8].z)**2)

                if up_count == 1 and fingers[1]:
                    current_gesture = "VOLUME UP"
                elif up_count == 0:
                    current_gesture = "VOLUME DOWN"
                elif up_count == 2 and fingers[1] and fingers[2]:
                    current_gesture = "PLAY / PAUSE"
                elif up_count == 5:
                    current_gesture = "MUTE TOGGLE"
                elif up_count == 2 and fingers[1] and fingers[4]:
                    current_gesture = "ROCK ON"
                elif dist_ok < 0.05 and fingers[2] and fingers[3] and fingers[4]:
                    current_gesture = "OK SIGN"

        return img, current_gesture, hand_info