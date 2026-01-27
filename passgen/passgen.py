import string
import random
import tkinter as tk
from tkinter import messagebox

# print(string.ascii_letters, string.digits, string.punctuation)

letterpool = [i for i in string.ascii_letters]
numberpool = [i for i in string.digits]
punctuationpool = [i for i in string.punctuation]

allpool = [letterpool, numberpool, punctuationpool]


def generate_password():

    try:
        length = int(length_var.get())
        if length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Invalid input", "Password length must be a positive integer"
        )
        return
    # guarantee atleast 1 of each character type
    pools = [letterpool]
    guaranteed = [random.choice(letterpool)]

    if numbers_var.get():
        pools.append(numberpool)
        guaranteed.append(random.choice(numberpool))
    if symbols_var.get():
        pools.append(punctuationpool)
        guaranteed.append(random.choice(punctuationpool))

    passchars = guaranteed[:]
    for i in range(length - len(guaranteed)):
        passchars.append(random.choice(random.choice(pools)))
    random.shuffle(passchars)
    password = "".join(passchars)
    password_var.set(password)
    update_strength(password)


def update_strength(password):
    score = 0
    length = len(password)

    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in punctuationpool for c in password):
        score += 1
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 1

    if score <= 2:
        strength_var.set("Weak")
        width = 70
        color = "#c0392b"
    elif score <= 4:
        strength_var.set("Medium")
        width = 140
        color = "#f39c12"
    else:
        strength_var.set("Strong")
        width = 200
        color = "#27ae60"

    strength_canvas.coords(strength_rect, 0, 0, width, 10)
    strength_canvas.itemconfig(strength_rect, fill=color)


def copy_to_clip():
    password = password_var.get()
    if not password:
        messagebox.showwarning("Nothing to copy")
        return
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()
    messagebox.showinfo("Copied", "Password copied to clipboard")


# --- UI setup ---
root = tk.Tk()
root.title("Password Generator")
root.resizable(False, False)
root.geometry("400x280")

# dark mode colors
bg = "#1e1e1e"
fg = "#ffffff"
entry_bg = "#2b2b2b"
btn_bg = "#3c3f41"
btn_active = "#4e5254"

root.configure(bg=bg)

# variables
length_var = tk.StringVar(value="15")
password_var = tk.StringVar()
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
strength_var = tk.StringVar(value="")
# length input
tk.Label(root, text="Password length:", background=bg, foreground=fg).pack(pady=(12, 0))
tk.Entry(
    root,
    textvariable=length_var,
    width=10,
    justify="center",
    bg=entry_bg,
    fg=fg,
    insertbackground=fg,
).pack()

# checkboxes
checkbox_frame = tk.Frame(root, bg=bg)
checkbox_frame.pack(pady=8)

tk.Checkbutton(
    checkbox_frame,
    text="Include Numbers",
    variable=numbers_var,
    bg=bg,
    fg=fg,
    selectcolor=bg,
    activebackground=bg,
    activeforeground=fg,
).pack(anchor="w")

tk.Checkbutton(
    checkbox_frame,
    text="Include Symbols",
    variable=symbols_var,
    bg=bg,
    fg=fg,
    selectcolor=bg,
    activebackground=bg,
    activeforeground=fg,
).pack(anchor="w")
# button
tk.Button(
    root,
    text="Generate Password",
    command=generate_password,
    background=btn_bg,
    foreground=fg,
    activebackground=btn_active,
    activeforeground=fg,
    relief="flat",
).pack(pady=8)

# password display
tk.Entry(
    root,
    textvariable=password_var,
    width=35,
    justify="center",
    state="readonly",
    readonlybackground=entry_bg,
    foreground=fg,
).pack()

# strength meter
tk.Label(root, textvariable=strength_var, background=bg, foreground=fg).pack(
    pady=(6, 2)
)

strength_canvas = tk.Canvas(root, width=200, height=10, bg="#444", highlightthickness=0)
strength_canvas.pack(pady=(0, 6))
strength_rect = strength_canvas.create_rectangle(0, 0, 0, 10, fill="#444", outline="")


# copy button
tk.Button(
    root,
    text="Copy to Clipboard",
    command=copy_to_clip,
    background=btn_bg,
    foreground=fg,
    activebackground=btn_active,
    activeforeground=fg,
    relief="flat",
).pack(pady=8)

root.mainloop()
