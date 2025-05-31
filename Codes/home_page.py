import customtkinter as ctk
import os
import sys
from PIL import Image
import cv2
from keras.models import load_model
from collections import deque
from tkinter import filedialog
from violence_detection import detect_violence
import time
from about_page import create_about_page  # Import the About Us page function

def start_home_page():
    # Load the violence detection model
    violence_model_path = os.path.join(sys._MEIPASS, "modelnew.h5") if hasattr(sys, "_MEIPASS") else "modelnew.h5"
    violence_model = load_model(violence_model_path)

    # Initialize a queue for predictions
    Q = deque(maxlen=128)

    # Initialize the app
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # Main application window
    root = ctk.CTk()
    root.title("Dashboard")
    root.geometry("800x600")

    # Configure grid layout
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(1, weight=1)

    # Top bar
    top_frame = ctk.CTkFrame(root, height=60, corner_radius=0, fg_color="#1c1c1c")
    top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
    top_frame.grid_propagate(False)

    # Add "Home," "About Us," and "Help" buttons in the top bar
    def go_home():
        main_frame.tkraise()  # Bring the main dashboard frame to the front

    def open_about_page():
        about_frame = create_about_page(root)  # Call the About Us page function
        about_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
        about_frame.tkraise()

    def open_help_page():
        help_frame = ctk.CTkFrame(root, fg_color="#2a2a2a")
        help_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
        help_frame.tkraise()

        # Add a placeholder in the help page
        ctk.CTkLabel(
            help_frame,
            text="Help Section - Content Coming Soon!",
            font=("Arial", 24, "bold"),
            text_color="white"
        ).pack(expand=True, padx=20, pady=20)

    # Menu Bar Buttons
    ctk.CTkButton(
        top_frame,
        text="Home",
        command=go_home,
        width=100,
        corner_radius=10,
        fg_color="#333333",
        text_color="white",
        hover_color="#555555",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=10, pady=10)

    ctk.CTkButton(
        top_frame,
        text="About Us",
        command=open_about_page,
        width=100,
        corner_radius=10,
        fg_color="#333333",
        text_color="white",
        hover_color="#555555",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=10, pady=10)

    ctk.CTkButton(
        top_frame,
        text="Help",
        command=open_help_page,
        width=100,
        corner_radius=10,
        fg_color="#333333",
        text_color="white",
        hover_color="#555555",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=10, pady=10)

    # Home page content
    main_frame = ctk.CTkFrame(root, fg_color="#2a2a2a")
    main_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
    main_frame.grid_columnconfigure((0, 1, 2), weight=1)
    main_frame.grid_rowconfigure((0, 1, 2), weight=1)

    # Title Frame
    title_frame = ctk.CTkFrame(main_frame, height=80)
    title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="ew")
    title_frame.grid_propagate(False)

    ctk.CTkLabel(
        title_frame,
        text="Welcome to the Simulator!",
        font=("Arial", 50, "bold"),
        text_color="#cccccc"
    ).pack(expand=True, padx=10, pady=10)

    # Function to load images safely
    def load_image(path, size):
        try:
            return ctk.CTkImage(Image.open(path), size=size)
        except Exception:
            return None

    live_feed_icon = load_image("live_feed_icon.png", (30, 30))
    recorded_icon = load_image("recorded_icon.png", (30, 30))

    # Define the Live Feed function
    def detect_live_feed():
        print("Starting live feed violence detection...")
        cap = cv2.VideoCapture(0)  # Open the default camera
        if not cap.isOpened():
            print("Error: Cannot access the camera.")
            return

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read frame. Exiting...")
                    break

                frame = detect_violence(frame, violence_model, Q)

                cv2.imshow("Live Feed - Violence Detection", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Live feed stopped.")

    # Define the Recorded Feed function
    def detect_recorded_feed():
        print("Select a video file for violence detection...")
        video_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mkv"), ("All Files", "*.*")]
        )
        if not video_path:
            print("No file selected. Operation cancelled.")
            return

        print(f"Selected file: {video_path}")
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Cannot open video file {video_path}.")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30

        frame_delay = int(1000 / fps)

        try:
            while cap.isOpened():
                start_time = time.time()
                ret, frame = cap.read()
                if not ret:
                    print("End of video or failed to read frame.")
                    break

                frame = detect_violence(frame, violence_model, Q)

                cv2.imshow("Recorded Feed - Violence Detection", frame)

                processing_time = int((time.time() - start_time) * 1000)
                effective_delay = max(1, frame_delay - processing_time)
                if cv2.waitKey(effective_delay) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Recorded feed processing stopped.")

    # Create buttons for Live Feed and Recorded Feed
    def create_button(frame, text, command, icon, row, column, sticky):
        ctk.CTkButton(
            frame,
            text=text,
            command=command,
            height=50,
            width=250,
            corner_radius=10,
            fg_color="#333333",
            text_color="white",
            hover_color="#555555",
            font=("Arial", 18, "bold"),
            image=icon,
            compound="left"
        ).grid(row=row, column=column, pady=15, sticky=sticky)

    create_button(main_frame, "   Live Feed", detect_live_feed, live_feed_icon, row=1, column=0, sticky="e")
    create_button(main_frame, "   Recorded", detect_recorded_feed, recorded_icon, row=1, column=2, sticky="w")

    # Run the application
    root.after(100, lambda: main_frame.tkraise())
    root.mainloop()
