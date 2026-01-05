# AI Gesture Controller (Web Interface)

A lightweight real-time hand-gesture controller that uses your webcam to control media and volume from a web browser.

## What it does
- Tracks hand landmarks with MediaPipe.
- Maps hand gestures to system/media actions using PyAutoGUI.
- Provides a simple Flask web interface with a live camera feed and activation button.

## Supported gestures
- Pointing Up (index finger) - Increase volume
- Fist (all fingers closed) - Decrease volume
- Peace (index + middle) - Play / Pause media
- Open Palm (all fingers up) - Mute toggle
- OK sign - Gesture detected / extra action

## Tech stack
- Python
- OpenCV (camera / image processing)
- MediaPipe (hand tracking)
- Flask (web UI)
- PyAutoGUI (simulate keyboard/media keys)

## Project structure
- main.py - Flask server and video streaming
- gesture_engine.py - Gesture detection and classification logic
- templates/index.html - Web UI (dark theme)

## Run
1. Start the app:
   - Windows: `python main.py` or `.\python.exe main_web.py`
2. Open your browser
3. Click the ACTIVATE button and use the camera feed to control media/volume with gestures.
