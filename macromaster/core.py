import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Controller
import threading
import time

# controller for sending virtual keyboard events
keyboard = Controller()
macro_runnin = False  # self explanatory
status_colors = {  # label color changes when running or stopped
    "running": "green",
    "stopped": "red",
}
blink_on = False  # tracks the current blink state
# Dark theme colors
BG_COLOR = "#2E2E2E"  # Dark gray background
FG_COLOR = "white"  # Default text color
BUTTON_START_BG = "#4CAF50"  # Green button
BUTTON_STOP_BG = "#f44336"  # Red button
ENTRY_BG = "#444444"  # Slightly lighter entry background


# macro loop
def run_macro(keys, delay):
    time.sleep(2)  # 2 second wait after start
    global macro_runnin
    while macro_runnin:
        for key in keys:
            if not macro_runnin:
                break
            keyboard.press(key)
            keyboard.release(key)
            time.sleep(delay)


# function to start the macro
def start_macro():
    global macro_runnin
    keys_input = keys_entry.get()
    if not keys_input:
        messagebox.showwarning("Input error", "Enter at least one key!")
        return
    keys = keys_input.split(",")  # keys separated by comma
    try:
        delay = float(delay_entry.get())
    except ValueError:
        messagebox.showwarning("Input error", "Delay must be a number!")
        return
    macro_runnin = True
    threading.Thread(target=run_macro, args=(keys, delay), daemon=True).start()
    status_label.config(text="Macro Running", fg=status_colors["running"])
    blink_status(status_label)
    keys_entry.config(state="disabled")
    delay_entry.config(state="disabled")


# function to stop the macro
def stop_macro():
    global macro_runnin
    macro_runnin = False
    keys_entry.config(state="normal")
    delay_entry.config(state="normal")
    status_label.config(text="Macro Stopped", fg=status_colors["stopped"])


# Blinking status
def blink_status(label):
    global blink_on
    # only blink if running
    if macro_runnin:
        blink_on = not blink_on
        # toggle between green and lighter green
        color = "#90ee90" if blink_on else status_colors["running"]
        status_label.config(fg=color)
        # schedule next blink
        status_label.after(500, lambda: blink_status(label))  # blinks every 500ms
    else:
        # ensures color returns to red when stopped
        blink_on = False
        label.config(fg=status_colors["stopped"])


# -------------GUI setup
root = tk.Tk()
root.title("MacroMaster")
root.geometry("400x250")
root.resizable(False, False)
root.attributes("-topmost", True)
root.configure(bg=BG_COLOR)  # dark gray background
# -------------Input frame
input_frame = tk.Frame(root, bg=BG_COLOR)
input_frame.pack(pady=10)

tk.Label(
    input_frame, text="Keys (comma-separated, e.g., a,b,c):", bg=BG_COLOR, fg=FG_COLOR
).pack()
keys_entry = tk.Entry(input_frame, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
keys_entry.pack()

tk.Label(
    input_frame,
    text="Delay between keys (seconds):",
    bg=BG_COLOR,
    fg=FG_COLOR,
).pack(pady=(10, 0))
delay_entry = tk.Entry(input_frame, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
delay_entry.pack()
delay_entry.insert(0, "1")
# -------------------- Button Frame --------------------
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=10)

start_button = tk.Button(
    button_frame,
    text="Start Macro",
    bg=BUTTON_START_BG,
    fg="white",
    activebackground="#45a049",
    command=lambda: start_macro(),
)
start_button.pack(side="left", padx=5)

note_label = tk.Label(
    button_frame,
    text="(starts after 2 seconds)",
    font=("Arial", 8),
    bg=BG_COLOR,
    fg=FG_COLOR,
)
note_label.pack(side="left")

stop_button = tk.Button(
    root,
    text="Stop Macro",
    bg=BUTTON_STOP_BG,
    fg="white",
    activebackground="#da190b",
    command=lambda: stop_macro(),
)
stop_button.pack(pady=5)

# -------------------- Status Label --------------------
status_label = tk.Label(
    root,
    text="Macro stopped",
    fg=status_colors["stopped"],
    bg=BG_COLOR,
    font=("Arial", 12),
)
status_label.pack(pady=5)
root.mainloop()
