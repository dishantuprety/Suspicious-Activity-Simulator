import customtkinter as ctk
import cv2
import threading
import numpy as np
import tensorflow as tf
from keras.models import load_model
from collections import deque
from violence_detection import detect_violence  # Import detection function

# Load TensorFlow model efficiently
violence_model_path = "modelnew.h5"
violence_model = load_model(violence_model_path)  # Ensure TF 2.x compatibility

# Global stop event
stop_event = threading.Event()

def open_camera(camera_index=0):
    """Opens webcam and applies violence detection in real-time."""
    
    def camera_thread():
        print("🔹 Live Feed Started | Violence Detection Active")

        Q = deque(maxlen=128)  # Buffer for predictions
        cap = cv2.VideoCapture(camera_index)  # Open selected webcam

        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return

        while not stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Failed to capture frame")
                break
            
            frame = cv2.resize(frame, (640, 480))  # Resize for consistency

            # Run violence detection
            frame = detect_violence(frame, violence_model, Q)

            # Show updated frame with violence detection
            cv2.imshow("Live Feed - Press 'q' to Close", frame)

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_event.set()

        cap.release()  # Release the camera
        cv2.destroyAllWindows()  # Close the window
        print("🔹 Live Feed Stopped")

    # Run the camera function in a separate thread
    threading.Thread(target=camera_thread, daemon=True).start()

def stop_camera():
    """Stops the camera thread."""
    stop_event.set()
