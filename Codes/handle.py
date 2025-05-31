import os
import sys

if hasattr(sys, "_MEIPASS"):
    # Use PyInstaller's temporary folder
    violence_model_path = os.path.join(sys._MEIPASS, "modelnew.h5")
else:
    # Use the normal path during development
    violence_model_path = "modelnew.h5"
