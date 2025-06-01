import customtkinter as ctk
from tkinter import filedialog
import subprocess

def open_file():
    """Opens file dialog to select a video and runs violence detection."""
    file_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")]
    )
    if not file_path:
        return

    print(f"Selected File: {file_path}")
    
    # Run violence detection with the selected file
    subprocess.Popen(["python", "violence_detection.py", file_path])
