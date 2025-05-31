import numpy as np
import cv2
import time
import sys
import tensorflow as tf
from keras.models import load_model
import os

from collections import deque
from human_detection import SimpleDetector, draw_boxes  # Import human detection module
from alert import send_telegram_alert

# Ensure TensorFlow 2.x compatibility
tf.compat.v1.disable_eager_execution()
from tensorflow.keras import backend as K
K.clear_session()

# Load models
human_model_path = r"C:\Users\disha\OneDrive\Desktop\finalyearproject\ssd_mobilenet_v2_coco_2018_03_29\frozen_inference_graph.pb"

if hasattr(sys, "_MEIPASS"):
    violence_model_path = os.path.join(sys._MEIPASS, "modelnew.h5")
else:
    violence_model_path = "modelnew.h5"

print(f"Loading violence model from: {violence_model_path}")  # Debug statement

# Initialize human detection model
human_detector = SimpleDetector(human_model_path)

# Load violence detection model
violence_model = load_model(violence_model_path)
Q = deque(maxlen=128)

last_alert_time = 0
ALERT_INTERVAL = 60  # Time in seconds between alerts

def detect_violence(frame, model, queue, threshold=0.50):
    """Run violence detection model on the given frame."""
    global last_alert_time

    # Preprocess the frame
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    processed_frame = cv2.resize(processed_frame, (128, 128)).astype("float32") / 255.0
    processed_frame = np.expand_dims(processed_frame, axis=0)

    # Predict using the model
    preds = model.predict(processed_frame, verbose=0)[0]
    queue.append(preds)

    # Compute the rolling average of predictions
    results = np.array(queue).mean(axis=0)

    # Define violence_detected
    violence_detected = (results > threshold)[0]  # True if violence detected

    # Set label and color
    label = "Violence Detected" if violence_detected else "No Violence"
    text_color = (0, 0, 255) if violence_detected else (0, 255, 0)

    # Draw label on frame
    cv2.putText(frame, label, (35, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.25, text_color, 3)

    # Call Telegram alert function if violence is detected
    current_time = time.time()
    if violence_detected and (current_time - last_alert_time >= ALERT_INTERVAL):
        print("\U0001F6A8 Violence detected! Sending alert...")
        send_telegram_alert()
        last_alert_time = current_time

    return frame

if __name__ == "__main__":
    # Get input source (live feed or recorded video)
    video_path = sys.argv[1] if len(sys.argv) > 1 else 0  # Default to live feed

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video source.")
        exit()

    threshold = 0.3
    fps_list = []

    try:
        while cap.isOpened():
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                print("End of video or failed to read frame.")
                break

            frame = cv2.resize(frame, (640, 480))

            # Detect humans
            boxes, scores, classes, num = human_detector.detect_humans(frame, threshold=threshold)

            # Draw bounding boxes and check if humans are detected
            frame, human_detected = draw_boxes(frame, boxes, scores, classes, threshold)

            if human_detected:
                frame = detect_violence(frame, violence_model, Q)

            # Calculate FPS
            end_time = time.time()
            fps = 1 / (end_time - start_time)
            fps_list.append(fps)
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Show the frame
            cv2.imshow("Human & Violence Detection", frame)

            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

        if fps_list:
            avg_fps = sum(fps_list) / len(fps_list)
            print(f"Average FPS: {avg_fps:.2f}")
