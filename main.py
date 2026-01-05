# .\python.exe main.py 

from flask import Flask, render_template, Response, redirect, url_for
import cv2
import pyautogui
import time
from gesture_engine import GestureEngine

app = Flask(__name__)

# Global state
engine = GestureEngine()
is_running = False
cap = None

def get_camera():
    global cap
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)
    return cap

def stop_camera():
    global cap
    if cap is not None:
        cap.release()
        cap = None

def generate_frames():
    global is_running
    # Local stability variables
    last_gesture = ""
    gesture_count = 0
    last_action_time = 0
    cooldown = 0.4

    camera = get_camera()
    
    while is_running:
        success, frame = camera.read()
        if not success:
            break
        
        frame = cv2.flip(frame, 1)
        current_time = time.time()

        # Execute Engine Logic
        frame, current_gesture, hand_info = engine.process_frame(frame)

        # Stability Logic
        if current_gesture == last_gesture:
            gesture_count += 1
        else:
            gesture_count = 0
            last_gesture = current_gesture

        display_text = last_gesture if gesture_count > 3 else "Processing..."

        # PyAutoGUI Actions
        if gesture_count > 5 and (current_time - last_action_time > cooldown):
            actions = {
                "VOLUME UP": "volumeup",
                "VOLUME DOWN": "volumedown",
                "PLAY / PAUSE": "playpause",
                "MUTE TOGGLE": "volumemute"
            }
            if display_text in actions:
                pyautogui.press(actions[display_text])
                last_action_time = current_time

        # UI Overlay
        cv2.rectangle(frame, (0, 0), (480, 80), (40, 40, 40), -1)
        cv2.putText(frame, f"Hand: {hand_info}", (10, 25), 1, 1, (255, 255, 0), 1)
        color = (0, 255, 0) if gesture_count > 3 else (0, 165, 255)
        cv2.putText(frame, display_text, (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)

        # Stream Encoding
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    stop_camera()

@app.route('/')
def index():
    return render_template('index.html', active=is_running)

@app.route('/start')
def start():
    global is_running
    is_running = True
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    global is_running
    is_running = False
    return redirect(url_for('index'))

@app.route('/video_feed')
def video_feed():
    if is_running:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return ""

if __name__ == "__main__":
    # Ensure camera is off at start
    stop_camera()
    app.run(host='0.0.0.0', port=5000, debug=False)

