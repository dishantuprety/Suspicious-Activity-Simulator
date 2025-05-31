import customtkinter as ctk
from login_page import LoginFrame  # Import LoginFrame
from signup_page import SignUp  # Import SignUp
from home_page import start_home_page  # Import the Home Page logic

class MainPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window properties
        self.geometry("800x600")
        self.title("Suspicious Activity Simulator")

        # Title Label (adjusted position)
        self.label = ctk.CTkLabel(self, text="Welcome to the Application!", font=("Arial", 40, "bold"))
        self.label.pack(pady=(50, 20))  # Reduced bottom padding

        # Frame to center buttons
        self.frame = ctk.CTkFrame(self, fg_color="transparent")  # No background shadow
        self.frame.pack(pady=100)  # Added slight top padding

        # Login Button (properly centered)
        self.login_button = ctk.CTkButton(
            self.frame,
            text="Login",
            height=50,
            width=250,
            command=self.open_login,
            font=("Roboto", 20),
            corner_radius=15,
            fg_color="#333333",
            hover_color="#555555",
            bg_color="transparent"
        )
        self.login_button.pack(pady=5)  # Reduced padding between buttons

        # Signup Button (properly centered)
        self.signup_button = ctk.CTkButton(
            self.frame,
            text="Signup",
            height=50,
            width=250,
            command=self.open_signup,
            font=("Roboto", 20),
            corner_radius=15,
            fg_color="#333333",
            hover_color="#555555",
            bg_color="transparent"
        )
        self.signup_button.pack(pady=5)

    def open_login(self):
        """Navigate to the Login Page."""
        self.withdraw()  # Hide the Main Page window
        login_app = ctk.CTk()
        login_frame = LoginFrame(master=login_app)
        login_frame.show_main_callback = self.show_main_page  # Assign callback to return to Main Page
        login_frame.access_home_callback = self.open_home  # Assign callback to access Home Page
        login_frame.pack(fill="both", expand=True)
        login_app.mainloop()

    def open_signup(self):
        """Navigate to the Signup Page."""
        self.withdraw()  # Hide the Main Page window
        signup_app = ctk.CTk()
        signup_frame = SignUp(master=signup_app, show_main_callback=self.show_main_page)
        signup_frame.pack(fill="both", expand=True)
        signup_app.mainloop()

    def open_home(self):
        """Navigate to the Home Page after successful login."""
        self.destroy()  # Close the Main Page and previous windows
        start_home_page()  # Call the start_home_page function from home_page.py

    def show_main_page(self):
        """Reopen the Main Page."""
        self.deiconify()  # Show the Main Page window again


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = MainPage()
    app.mainloop()
