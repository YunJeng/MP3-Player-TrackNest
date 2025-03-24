import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector
from PIL import Image, ImageTk

class Login:
    def __init__(self, win, main_app_callback):
        self.win = win
        self.main_app_callback = main_app_callback
        self.win.title("Login or Sign Up")
        self.win.geometry("400x300")
        logo = Image.open('logo.png')
        self.win.tk.call('wm', 'iconphoto', win._w, ImageTk.PhotoImage(logo))
        #self.win.configure(bg="#061933")
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '12345678',
            'database': 'mp3'
        }
        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self.win, text="Name")
        self.name_label.pack(pady=(30, 0))
        self.name_entry = tk.Entry(self.win)
        self.name_entry.pack(pady=(5, 30))

        self.password_label = tk.Label(self.win, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.win, show="*")
        self.password_entry.pack(pady=(5, 30))

        self.login_button = tk.Button(self.win, text="Login", command=self.login)
        self.login_button.pack()

        self.signup_button = tk.Button(self.win, text="Sign Up", command=self.show_signup)
        self.signup_button.pack()
    
    def login(self):
        name = self.name_entry.get()
        password = self.password_entry.get()
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Member WHERE Name=%s AND Password=%s", (name, password))
        user = cursor.fetchone()
        memberid = user['MemberID']
        if user:
            self.win.destroy()
            self.main_app_callback(memberid)
        else:
            messagebox.showerror("Error", "Invalid login credentials")
    
    def show_signup(self):
        self.signup_window = tk.Toplevel(self.win)
        self.signup_window.title("Sign Up")
        self.signup_window.geometry("300x530")

        self.signup_name_label = tk.Label(self.signup_window, text="Name")
        self.signup_name_label.pack(pady=(30, 0))
        self.signup_name_entry = tk.Entry(self.signup_window)
        self.signup_name_entry.pack(pady=(5, 30))

        self.signup_email_label = tk.Label(self.signup_window, text="Email")
        self.signup_email_label.pack()
        self.signup_email_entry = tk.Entry(self.signup_window)
        self.signup_email_entry.pack(pady=(5, 30))

        self.signup_date_label = tk.Label(self.signup_window, text="Registration Date")
        self.signup_date_label.pack()
        self.signup_date_entry = tk.Entry(self.signup_window)
        self.signup_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.signup_date_entry.pack(pady=(5, 30))

        self.signup_password_label = tk.Label(self.signup_window, text="Password")
        self.signup_password_label.pack()
        self.signup_password_entry = tk.Entry(self.signup_window, show="*")
        self.signup_password_entry.pack(pady=(5, 30))

        
        self.signup_account_type_label = tk.Label(self.signup_window, text="Account Type (free/student)")
        self.signup_account_type_label.pack()
        self.account_type_var = tk.StringVar(self.signup_window)
        self.account_type_var.set(" ")
        self.signup_account_type_option = tk.OptionMenu(self.signup_window, self.account_type_var, "free", "student")
        self.signup_account_type_option.pack(pady=(5, 30))
        self.signup_button = tk.Button(self.signup_window, text="Sign Up", command=self.signup)
        self.signup_button.pack(pady=(5, 30))

    def signup(self):
        name = self.signup_name_entry.get()
        email = self.signup_email_entry.get()
        reg_date = self.signup_date_entry.get()
        password = self.signup_password_entry.get()
        account_type = self.account_type_var.get()
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO member (Name, Email, JoinDate, Password, MemberType)"
                       "VALUES (%s, %s, %s, %s, %s)",
                       (name, email, reg_date, password, account_type))
        conn.commit()
        conn.close()
        self.signup_window.destroy()
        messagebox.showinfo("Success", "Account created successfully")

if __name__ == "__main__":
    win = tk.Tk()
    app = Login(win, None)
    win.mainloop()