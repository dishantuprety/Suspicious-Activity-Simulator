import customtkinter as ctk
import sqlite3
import bcrypt
from setup_database import initialize_database  # Import the database initialization function

class SignUp(ctk.CTkFrame):
    def __init__(self, master, show_main_callback):
        super().__init__(master)
        master.geometry("800x600")  # Set fixed window size
        master.title("Signup")  # Set window title

        # Handle the close button (X)
        master.protocol("WM_DELETE_WINDOW", self.terminate_app)

        self.show_main_callback = show_main_callback  # Callback to return to main menu

        # Initialize database (ensure the table exists)
        initialize_database()

        # GUI Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)  
        self.grid_columnconfigure(2, weight=1)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=2)

        # Back Button
        self.back_button = ctk.CTkButton(self, text="← Back", command=self.handle_back_button, 
                                         height=30, width=80, fg_color="#333333", hover_color="#555555", 
                                         font=("Arial", 14), corner_radius=30)
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Title
        self.title_label = ctk.CTkLabel(self, text="Sign Up", font=("Impact", 30))
        self.title_label.grid(row=1, column=1, pady=10)

        # Username Entry
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Enter username...", height=40, width=300)
        self.username_entry.grid(row=2, column=1, pady=10)

        # Password Entry
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter Password", show="*", height=40, width=300)
        self.password_entry.grid(row=3, column=1, pady=10)

        # Re-enter Password Entry
        self.repassword_entry = ctk.CTkEntry(self, placeholder_text="Re-enter Password", show="*", height=40, width=300)
        self.repassword_entry.grid(row=4, column=1, pady=10)

        # Security Question
        self.security_question_label = ctk.CTkLabel(self, text="Select Security Question:")
        self.security_question_label.grid(row=5, column=1, pady=(10, 0))

        self.security_question = ctk.CTkComboBox(self, values=[
            "Which is your favorite site?",
            "What is your pet's name?",
            "What is your mother's maiden name?",
            "What is your favorite food?"
        ], height=40, width=300)
        self.security_question.grid(row=6, column=1, pady=10)

        # Security Answer Entry
        self.security_answer = ctk.CTkEntry(self, placeholder_text="Enter answer...", height=40, width=300)
        self.security_answer.grid(row=7, column=1, pady=10)

        # Error Label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 12))
        self.error_label.grid(row=8, column=1, pady=5)
        self.error_label.grid_remove()

        # Sign Up Button
        self.signup_button = ctk.CTkButton(self, text="Sign Up", command=self.sign_up, height=50, width=250,
                                           fg_color="#333333", hover_color="#555555", font=("Impact", 20), corner_radius=30)
        self.signup_button.grid(row=9, column=1, pady=20)

    def handle_back_button(self):
        """Handles back navigation to the main page."""
        self.master.destroy()  # Close the signup page
        if self.show_main_callback:
            self.show_main_callback()  # Show the main page without creating a new window

    def sign_up(self):
        """Handles user registration and stores data in the database."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        repassword = self.repassword_entry.get().strip()
        security_question = self.security_question.get().strip()
        security_answer = self.security_answer.get().strip()

        # Validate inputs
        if not username or not password or not repassword or not security_answer:
            self.error_label.configure(text="⚠ All fields are required!", text_color="red")
            self.error_label.grid()
            return

        if password != repassword:
            self.error_label.configure(text="⚠ Passwords do not match!", text_color="red")
            self.error_label.grid()
            return

        # Hash password & security answer
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        hashed_answer = bcrypt.hashpw(security_answer.encode(), bcrypt.gensalt()).decode()

        # Store in database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (username, password, security_question, security_answer)
                VALUES (?, ?, ?, ?)
            """, (username, hashed_password, security_question, hashed_answer))
            
            conn.commit()
            self.error_label.configure(text="✔ Account created successfully!", text_color="green")
        except sqlite3.IntegrityError:
            self.error_label.configure(text="⚠ Username already exists!", text_color="red")

        conn.close()
        self.error_label.grid()

    def terminate_app(self):
        """Terminate the entire application."""
        self.master.destroy()
        quit()  # Exit the Python program
