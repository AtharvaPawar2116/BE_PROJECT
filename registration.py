# ================= IMPORTS =================
import tkinter as tk
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import re
import random
import os
import cv2

# ================= WINDOW =================
window = tk.Tk()
window.geometry("700x700")
window.title("REGISTRATION FORM")
window.configure(bg="#e8f5e9")

# ================= VARIABLES =================
Fullname = tk.StringVar()
address = tk.StringVar()
username = tk.StringVar()
Email = tk.StringVar()
Phoneno = tk.StringVar()
var = tk.IntVar()
age = tk.IntVar()
password = tk.StringVar()
password1 = tk.StringVar()

# ================= DATABASE =================
db = sqlite3.connect('evaluation.db')
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS admin_registration
               (Fullname TEXT, address TEXT, username TEXT,
                Email TEXT, Phoneno TEXT, Gender TEXT,
                age TEXT , password TEXT)""")
db.commit()

# ================= PASSWORD CHECK =================
def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    if len(passwd) < 6:
        return False
    if not any(char.isdigit() for char in passwd):
        return False
    if not any(char.isupper() for char in passwd):
        return False
    if not any(char.islower() for char in passwd):
        return False
    if not any(char in SpecialSym for char in passwd):
        return False
    return True

# ================= INSERT FUNCTION =================
def insert():
    fname = Fullname.get()
    addr = address.get()
    un = username.get()
    email = Email.get()
    mobile = Phoneno.get()
    gender = var.get()
    user_age = age.get()
    pwd = password.get()
    cnpwd = password1.get()

    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()

        find_user = ('SELECT * FROM admin_registration WHERE username = ?')
        c.execute(find_user, [(un)])
        if c.fetchall():
            ms.showerror('Error!', 'Username Taken Try a Different One.')
            return

        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regex, email):
            ms.showerror("Error", "Please Enter valid email")
            return

        if fname == "" or fname.isdigit():
            ms.showerror("Error", "Please enter valid name")
            return

        if addr == "":
            ms.showerror("Error", "Please Enter Address")
            return

        if len(mobile) != 10:
            ms.showerror("Error", "Please Enter 10 digit mobile number")
            return

        if user_age <= 0 or user_age > 100:
            ms.showerror("Error", "Please Enter valid age")
            return

        if not password_check(pwd):
            ms.showerror("Error", "Password must contain uppercase, lowercase, number and symbol")
            return

        if pwd != cnpwd:
            ms.showerror("Error", "Passwords do not match")
            return

        c.execute("""INSERT INTO admin_registration
                  (Fullname, address, username, Email, Phoneno, Gender, age, password)
                  VALUES(?,?,?,?,?,?,?,?)""",
                  (fname, addr, un, email, mobile, gender, user_age, pwd))

        db.commit()
        ms.showinfo('Success!', 'Account Created Successfully!')
        window.destroy()

# ================= BACKGROUND IMAGE =================
image2 = Image.open('r2.jpg')
image2 = image2.resize((700, 700), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0)

# ================= TITLE =================
title = tk.Label(window,
                 text="Create Your Account",
                 font=("Segoe UI", 26, "bold"),
                 bg="#1b5e20",
                 fg="white",
                 width=30)
title.place(x=90, y=40)

label_font = ("Segoe UI", 12, "bold")
entry_font = ("Segoe UI", 12)
label_bg = "white"

# ================= FORM FIELDS =================
def create_label(text, x, y):
    tk.Label(window, text=text, font=label_font,
             bg=label_bg).place(x=x, y=y)

def create_entry(variable, x, y, show=None):
    tk.Entry(window, textvariable=variable,
             font=entry_font, width=25,
             bd=2, relief="groove",
             show=show).place(x=x, y=y)

create_label("Full Name", 120, 130)
create_entry(Fullname, 330, 130)

create_label("Address", 120, 180)
create_entry(address, 330, 180)

create_label("Email", 120, 230)
create_entry(Email, 330, 230)

create_label("Phone Number", 120, 280)
create_entry(Phoneno, 330, 280)

create_label("Gender", 120, 330)
tk.Radiobutton(window, text="Male", variable=var,
               value=1, bg=label_bg).place(x=330, y=330)
tk.Radiobutton(window, text="Female", variable=var,
               value=2, bg=label_bg).place(x=420, y=330)

create_label("Age", 120, 380)
create_entry(age, 330, 380)

create_label("Username", 120, 430)
create_entry(username, 330, 430)

create_label("Password", 120, 480)
create_entry(password, 330, 480, show="*")

create_label("Confirm Password", 120, 530)
create_entry(password1, 330, 530, show="*")

# ================= REGISTER BUTTON =================
btn = tk.Button(window,
                text="REGISTER",
                font=("Segoe UI", 14, "bold"),
                bg="#2e7d32",
                fg="white",
                activebackground="#1b5e20",
                activeforeground="white",
                width=18,
                bd=0,
                cursor="hand2",
                command=insert)
btn.place(x=240, y=600)

window.mainloop()