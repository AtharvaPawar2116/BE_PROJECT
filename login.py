import tkinter as tk
from tkinter import ttk, LEFT
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
from subprocess import call

# ===================== MAIN WINDOW =====================
root = tk.Tk()
root.title("Login Form")
root.geometry("700x650+200+50")
root.configure(background="black")

w, h = root.winfo_screenwidth(), root.winfo_screenheight()

# ===================== VARIABLES =====================
username = tk.StringVar()
password = tk.StringVar()

# ===================== BACKGROUND IMAGE =====================
try:
    image2 = Image.open('l1.jpg')
    image2 = image2.resize((w, h), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(image2)

    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0)
except:
    print("Background image not found.")

# ===================== DATABASE SETUP =====================
def create_table():
    conn = sqlite3.connect('evaluation.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_registration(
            Fullname TEXT,
            address TEXT,
            username TEXT,
            Email TEXT,
            Phoneno TEXT,
            Gender TEXT,
            age TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

create_table()

# ===================== FUNCTIONS =====================
def registration():
    root.destroy()
    call(["python", "registration.py"])

def login():
    conn = sqlite3.connect('evaluation.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM admin_registration WHERE username=? AND password=?",
        (username.get(), password.get())
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        ms.showinfo("Success", "Login Successfully!")
        root.destroy()
        call(["python", "GUI_master_old.py"])
    else:
        ms.showerror("Error", "Username or Password not found!")

# ===================== UI DESIGN =====================
title = tk.Label(
    root,
    text="Login Here",
    font=("Algerian", 30, "bold", "italic"),
    bd=5,
    bg="purple",
    fg="white"
)
title.place(x=200, y=150, width=250)

Login_frame = tk.Frame(root, bg="white")
Login_frame.place(x=100, y=300)

tk.Label(
    Login_frame,
    text="Username",
    font=("Times new roman", 20, "bold"),
    bg="white"
).grid(row=1, column=0, padx=20, pady=10)

txtuser = tk.Entry(
    Login_frame,
    bd=5,
    textvariable=username,
    font=("", 15)
)
txtuser.grid(row=1, column=1, padx=20)

tk.Label(
    Login_frame,
    text="Password",
    font=("Times new roman", 20, "bold"),
    bg="white"
).grid(row=2, column=0, padx=50, pady=10)

txtpass = tk.Entry(
    Login_frame,
    bd=5,
    textvariable=password,
    show="*",
    font=("", 15)
)
txtpass.grid(row=2, column=1, padx=20)

btn_log = tk.Button(
    Login_frame,
    text="Login",
    command=login,
    width=15,
    font=("Times new roman", 14, "bold"),
    bg="green",
    fg="black"
)
btn_log.grid(row=3, column=1, pady=10)

btn_reg = tk.Button(
    Login_frame,
    text="Create Account",
    command=registration,
    width=15,
    font=("Times new roman", 14, "bold"),
    bg="red",
    fg="black"
)
btn_reg.grid(row=3, column=0, pady=10)

# ===================== RUN =====================
root.mainloop()