import customtkinter as ctk
from home_page import start_home_page  # Import your untouched Home Page (running the Home Page logic)

class BridgePage(ctk.CTkFrame):
    def __init__(self, master, home_callback):
        super().__init__(master)
        self.home_callback = home_callback  # Callback to launch the Home Page

        # Title Label
        self.label = ctk.CTkLabel(self, text="Validating Access...", font=("Arial", 20, "bold"))
        self.label.pack(pady=(50, 10))

        # Continue Button
        self.continue_button = ctk.CTkButton(
            self, text="Continue to Home Page", command=self.open_home_page, width=250, height=50, font=("Roboto", 20)
        )
        self.continue_button.pack(pady=(30, 10))

    def open_home_page(self):
        """Launch the Home Page."""
        self.master.destroy()  # Close the bridge page window
        self.home_callback()  # Invoke the Home Page callback
