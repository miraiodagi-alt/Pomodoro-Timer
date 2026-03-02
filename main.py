from tkinter import *
import math
import os
import sys
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
MARKS = ""
timer = None

# ---------------------------- Additional SETUP ------------------------------- #
# to make sure that it has a secure path of the backgraound image
def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# to tell a break starts by lifitng and a sound
def bring_to_front():
    window.deiconify()
    window.lift()
    window.attributes("-topmost", True)
    # window.after(200, lambda: window.attributes("-topmost", False))
    # window.bell()
    window.focus_force()

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    # to stop the timer counting down
    if timer is not None:
        window.after_cancel(timer)

    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    set_counter.config(text="")
    global REPS
    REPS = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global REPS
    REPS += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if REPS % 8 == 0:
        # If it's the 8th rep:
        title_label.config(text="Break", fg=RED)
        bring_to_front()
        count_down(long_break_sec)
    elif REPS % 2 == 0:
        # If it's the 2nd/4th/6th rep:
        title_label.config(text="Break", fg=PINK)
        bring_to_front()
        count_down(short_break_sec)
    else:
        # If it's the 1st/3rd/5th/7th rep:
        title_label.config(text="Work", fg=GREEN)
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000,count_down, count -1)
    else:
        global MARKS
        if REPS % 2 != 0:
            MARKS += "✔"
            set_counter.config(text=MARKS)

        start_timer()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# tomato_img = PhotoImage(file="tomato.png")
tomato_img = PhotoImage(file=resource_path("tomato.png"))
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

title_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME,45,"bold"))
title_label.grid(column=1,row=0)

canvas.create_image(100,112, image=tomato_img)
timer_text = canvas.create_text(100,130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1,row=1)

start_button = Button(text="Start",command= start_timer, highlightthickness=0)
start_button.grid(column=0,row=2)

reset_button = Button(text="Reset", command= reset_timer, highlightthickness=0)
reset_button.grid(column=2,row=2)

set_counter = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 15, "bold"))
set_counter.grid(column=1,row=3)

window.mainloop()