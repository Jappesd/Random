import random
import time
import sys
import tkinter as tk
import threading

thinking_phrases = [
    "Consulting the archives...",
    "Thinking...",
    "Questioning reality...",
    "Phoning a friend...",
    "Looking for the manual...",
    "Asking a different AI...",
    "Loading wisdom (0%)...",
]

answers = [
    "Yes. Absolutely. No doubt about it.",
    "No. And you should stop asking.",
    "Perhaps.",
    "Probably. But only on Tuesdays.",
    "The answer was obvious before you asked.",
    "That depends on factors im legally not allowed to explain",
    "I already answered this. You just forgot.",
    "Interesting question. Wrong, but interesting.",
    "42. Now stop asking.",
    "You cant handle the truth!",
    "Yes. Obviously.",
    "No. And I'm disappointed you asked.",
    "Maybe. But you don't deserve to know.",
    "That's a terrible question. Next.",
    "Absolutely not. Hope that helps.",
    "Sure. Whatever makes you feel better.",
]

contradictions = [
    "Actually, ignore everything i just said.",
    "Wait. That might be incorrect",
    "New information detected. Disregard previous output.",
    "I have changed my mind.",
    "Actually, never mind.",
    "Wait. That's wrong.",
    "I have reconsidered.",
    "Ignore that.",
]

refusals = [
    "Ask something better.",
    "No.",
    "I refuse to answer that.",
    "That question makes me uncomfortable.",
    "Ask again later. Or don't.",
    "I am not in the mood for this." "Thats it im calling 911.",
]


def fake_thinking():
    status_label.config(text=random.choice(thinking_phrases) + "...")
    progress.set(0)

    for i in range(1, 101):
        time.sleep(random.uniform(0.01, 0.04))
        progress.set(i)
        progress_bar.update()
        if random.random() < 0.03:
            progress.set(random.randint(0, 40))
        if random.random() < 0.05:
            status_label.config(text="Recalculating...")
    status_label.config(text="Done. Probably.")


def generate_answer():
    if random.random() < 0.15:
        return random.choice(refusals)

    response = random.choice(answers)

    if random.random() < 0.3:
        time.sleep(1)
        response += "\n\n" + random.choice(contradictions)
    return response


def ask_oracle():
    question = entry.get().strip()

    if not question:
        output.config(text="You didn't even ask anything.")
        return

    ask_button.config(state="disabled")
    output.config(text="")
    status_label.config(text="Initializing Cosmic Wisdom...")

    def task():
        fake_thinking()
        answer = generate_answer()
        output.config(text=answer)
        ask_button.config(state="normal")
        ask_button.config(
            text=random.choice(
                [
                    "Ask Again (Why?)",
                    "Try Another Question",
                    "That Was a Mistake",
                    "Go Ahead. Ask.",
                ]
            )
        )

    threading.Thread(target=task, daemon=True).start()


root = tk.Tk()
root.title("Totally Legit AI Oracle v.0.0.1")
root.geometry("500x350")
root.resizable(False, False)

title = tk.Label(root, text="🔮 AI ORACLE", font=("Segoe UI", 18, "bold"))
title.pack(pady=10)

entry = tk.Entry(root, font=("Segoe UI", 12))
entry.pack(fill="x", padx=20)

ask_button = tk.Button(
    root, text="Ask the Oracle", font=("Segoe UI", 11), command=ask_oracle
)
ask_button.pack(pady=10)

progress = tk.IntVar()
progress_bar = tk.Scale(
    root,
    from_=0,
    to=100,
    orient="horizontal",
    variable=progress,
    showvalue=False,
    length=400,
)
progress_bar.pack()

status_label = tk.Label(root, text="Idle.", font=("Segoe UI", 10))
status_label.pack(pady=5)

output = tk.Label(
    root, text="", font=("Segoe UI", 11), wraplength=460, justify="center"
)
output.pack(pady=20)

root.mainloop()
