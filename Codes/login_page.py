import customtkinter as ctk
import sqlite3
import bcrypt

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        master.geometry("800x600")  # Set fixed window size
        master.title("Login")  # Set window title

        # Handle the close button (X)
        master.protocol("WM_DELETE_WINDOW", self.terminate_app)

        # Callbacks assigned manually from the parent method
        self.show_main_callback = None  # Initialize callback for returning to main menu
        self.access_home_callback = None  # Initialize callback for accessing home page

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=3)

        # Back Button
        self.back_button = ctk.CTkButton(
            self, text="← Back", command=self.handle_back_button, 
            height=35, width=80, fg_color="#333333", hover_color="#444444", 
            font=("Arial", 14), corner_radius=30
        )
        self.back_button.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        # Title
        self.title_label = ctk.CTkLabel(self, text="Login", font=("Roboto", 30))
        self.title_label.grid(row=1, column=1, pady=5)

        # Username Entry
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Enter username...", height=40, width=300)
        self.username_entry.grid(row=2, column=1, pady=5)

        # Password Entry
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter Password", show="*", height=40, width=300)
        self.password_entry.grid(row=3, column=1, pady=5)

        # Error Label (Hidden Initially)
        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 12))
        self.error_label.grid(row=4, column=1, pady=5)
        self.error_label.grid_remove()  # Hide initially

        # Login Button
        self.login_button = ctk.CTkButton(
            self, text="Login", command=self.login, height=50, width=290,
            fg_color="#333333", hover_color="#555555", font=("Impact", 30), corner_radius=30
        )
        self.login_button.grid(row=5, column=1, pady=10)

    def handle_back_button(self):
        """Handles back navigation."""
        if self.show_main_callback:
            self.master.destroy()  # Close login window
            self.show_main_callback()  # Navigate back to main page

    def login(self):
        """Handles the login logic using the database."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.show_error("⚠ Username & password required!")
            return

        try:
            with sqlite3.connect("users.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM users WHERE username=?", (username,))
                user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode(), user[0].encode()):
                self.error_label.grid_remove()
                self.show_success_window()  # Open a themed success window
                if self.access_home_callback:
                    self.master.destroy()
                    self.access_home_callback()
            else:
                self.show_error("⚠ Invalid credentials!")  # Prevents username enumeration

        except sqlite3.Error as e:
            self.show_error("⚠ Database error!")
            print(f"Database Error: {e}")

    def show_error(self, message):
        """Displays error messages."""
        self.error_label.configure(text=message)
        self.error_label.grid()

    def show_success_window(self):
        """Shows a themed login success popup centered on the parent window."""
        success_popup = ctk.CTkToplevel(self.master)
        success_popup.geometry("350x150")
        success_popup.title("Login Successful")
        success_popup.configure(fg_color="#222222")  

    # Get dimensions of the parent window
        self.master.update_idletasks() 
        master_x = self.master.winfo_x()  
        master_y = self.master.winfo_y()   
        master_width = self.master.winfo_width()  
        master_height = self.master.winfo_height()  

    # Calculate position for centering
        popup_width =200
        popup_height = 175
        center_x = master_x + (master_width // 2) - (popup_width // 2)
        center_y = master_y + (master_height // 2) - (popup_height // 2)

    # Set the popup window position
        success_popup.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")

        success_label = ctk.CTkLabel(success_popup, text="Welcome", font=("Arial", 20), text_color="white")
        success_label.pack(pady=20)

        close_button = ctk.CTkButton(success_popup, text="OK", command=success_popup.destroy,
                                 height=40, width=100, fg_color="#111111", hover_color="#222222")
        close_button.pack(pady=10)

        success_popup.transient(self.master)  # Make the popup modal
        success_popup.grab_set()
        self.master.wait_window(success_popup)

    def terminate_app(self):
        """Terminate the entire application."""
        self.master.destroy()
        quit()  # Exit the Python program
