import tkinter as tk
from collections import Counter
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "sanat.txt")
with open(file_path, "r", encoding="utf-8") as f:
    words = [line.strip().lower() for line in f]
word_counters = {word: Counter(word) for word in words}

MAX_DISPLAY = 50
prefix_full_matches = []
letters_full_matches = []


# --- Callback functions ---
def update_prefix_list(*args):
    global prefix_full_matches
    search_term = prefix_var.get().lower()
    prefix_listbox.delete(0, tk.END)
    if not search_term:
        prefix_full_matches = []
        return
    matches = [w for w in words if w.startswith(search_term)]
    prefix_full_matches = matches
    if len(matches) > MAX_DISPLAY:
        displayed = matches[:MAX_DISPLAY] + [
            f"+{len(matches) - MAX_DISPLAY} more matches"
        ]
    else:
        displayed = matches
    for match in displayed:
        prefix_listbox.insert(tk.END, match)


def update_letters_list(*args):
    global letters_full_matches
    letters = letters_var.get().lower()
    letters_listbox.delete(0, tk.END)
    if not letters:
        letters_full_matches = []
        return
    letters_count = Counter(letters)
    matches = [
        w
        for w, wc in word_counters.items()
        if all(letters_count.get(c, 0) >= count for c, count in wc.items())
    ]
    matches.sort(key=lambda w: (-len(w), w))  # longest first
    letters_full_matches = matches
    if len(matches) > MAX_DISPLAY:
        displayed = matches[:MAX_DISPLAY] + [
            f"+{len(matches) - MAX_DISPLAY} more matches"
        ]
    else:
        displayed = matches
    for match in displayed:
        letters_listbox.insert(tk.END, match)


def expand_prefix_list(event):
    selection = prefix_listbox.curselection()
    if not selection:
        return
    index = selection[0]
    value = prefix_listbox.get(index)
    if value.startswith("+") and prefix_full_matches:
        prefix_listbox.delete(0, tk.END)
        for match in prefix_full_matches:
            prefix_listbox.insert(tk.END, match)


def expand_letters_list(event):
    selection = letters_listbox.curselection()
    if not selection:
        return
    index = selection[0]
    value = letters_listbox.get(index)
    if value.startswith("+") and letters_full_matches:
        letters_listbox.delete(0, tk.END)
        for match in letters_full_matches:
            letters_listbox.insert(tk.END, match)


# --- GUI setup ---
root = tk.Tk()
root.title("Finnish Word Search")

# Configure grid for resizing
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)  # Listboxes expand vertically

# Labels
tk.Label(root, text="Prefix Search:").grid(
    row=0, column=0, padx=10, pady=(10, 0), sticky="w"
)
tk.Label(root, text="Letters Search (any order):").grid(
    row=0, column=1, padx=10, pady=(10, 0), sticky="w"
)

# Entry fields
prefix_var = tk.StringVar()
prefix_var.trace_add("write", update_prefix_list)
tk.Entry(root, textvariable=prefix_var).grid(row=1, column=0, padx=10, sticky="ew")

letters_var = tk.StringVar()
letters_var.trace_add("write", update_letters_list)
tk.Entry(root, textvariable=letters_var).grid(row=1, column=1, padx=10, sticky="ew")

# Prefix Listbox with scrollbar
prefix_frame = tk.Frame(root)
prefix_frame.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="nsew")
prefix_frame.grid_rowconfigure(0, weight=1)
prefix_frame.grid_columnconfigure(0, weight=1)

prefix_listbox = tk.Listbox(prefix_frame)
prefix_listbox.grid(row=0, column=0, sticky="nsew")
prefix_listbox.bind("<<ListboxSelect>>", expand_prefix_list)

prefix_scrollbar = tk.Scrollbar(
    prefix_frame, orient="vertical", command=prefix_listbox.yview
)
prefix_scrollbar.grid(row=0, column=1, sticky="ns")
prefix_listbox.config(yscrollcommand=prefix_scrollbar.set)

# Letters Listbox with scrollbar
letters_frame = tk.Frame(root)
letters_frame.grid(row=2, column=1, padx=10, pady=(5, 10), sticky="nsew")
letters_frame.grid_rowconfigure(0, weight=1)
letters_frame.grid_columnconfigure(0, weight=1)

letters_listbox = tk.Listbox(letters_frame)
letters_listbox.grid(row=0, column=0, sticky="nsew")
letters_listbox.bind("<<ListboxSelect>>", expand_letters_list)

letters_scrollbar = tk.Scrollbar(
    letters_frame, orient="vertical", command=letters_listbox.yview
)
letters_scrollbar.grid(row=0, column=1, sticky="ns")
letters_listbox.config(yscrollcommand=letters_scrollbar.set)

root.mainloop()
