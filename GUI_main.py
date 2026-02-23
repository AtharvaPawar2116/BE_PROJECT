import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import time
import sqlite3

global fn
fn=""

# ================== ROOT WINDOW ==================
root = tk.Tk()
root.title("Crop Prediction")
root.state("zoomed")
root.configure(bg="#f0f5f1")  # soft background color

# ================== TITLE ==================
title = tk.Label(
    root,
    text="🌾 Crop Prediction Using Machine Learning",
    font=("Segoe UI", 34, "bold"),
    bg="#f0f5f1",
    fg="#1b5e20"
)
title.pack(pady=20)

# ================== MAIN CONTAINER ==================
main_frame = tk.Frame(root, bg="#f0f5f1")
main_frame.pack(fill="both", expand=True, padx=40, pady=20)

# ================== LEFT SIDE (IMAGE) ==================
left_frame = tk.Frame(main_frame, bg="white", bd=0)
left_frame.pack(side="left", padx=20, pady=20)

image2 = Image.open("farmer.jpg")
image2 = image2.resize((750, 700), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(left_frame, image=background_image, bg="white")
background_label.image = background_image
background_label.pack(padx=20, pady=20)

# ================== RIGHT SIDE (PANEL) ==================
frame_alpr = tk.Frame(
    main_frame,
    bg="white",
    bd=0,
    highlightbackground="#2e7d32",
    highlightthickness=2
)
frame_alpr.pack(side="right", padx=60, pady=40)

panel_title = tk.Label(
    frame_alpr,
    text="Welcome",
    font=("Segoe UI", 24, "bold"),
    bg="white",
    fg="#2e7d32"
)
panel_title.pack(pady=40)

# ================== BUTTON STYLE ==================
def login():
    from subprocess import call
    call(["python", "login.py"])  

def register():
    from subprocess import call
    call(["python", "registration.py"])  

def window():
    root.destroy()

# Modern Button Style
def create_button(text, command):
    return tk.Button(
        frame_alpr,
        text=text,
        command=command,
        font=("Segoe UI", 16, "bold"),
        bg="#2e7d32",
        fg="white",
        activebackground="#1b5e20",
        activeforeground="white",
        width=18,
        height=2,
        bd=0,
        cursor="hand2"
    )

button1 = create_button("REGISTRATION", register)
button1.pack(pady=20)

button2 = create_button("LOGIN", login)
button2.pack(pady=20)

root.mainloop()