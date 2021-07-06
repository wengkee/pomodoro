import math
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
UNIT_SEC = 60  # to ease testing

rep = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global rep, timer
    window.after_cancel(timer)
    rep = 0
    label_timer.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text=format_duration(WORK_MIN*UNIT_SEC))
    label_done.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global rep
    rep += 1
    if rep % 8 == 0:
        count_down(LONG_BREAK_MIN * UNIT_SEC)
        label_timer.config(text="Break", fg=RED)
    elif rep % 2 == 0:
        count_down(SHORT_BREAK_MIN * UNIT_SEC)
        label_timer.config(text="Break", fg=PINK)
    else:
        count_down(WORK_MIN * UNIT_SEC)
        label_timer.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(seconds):
    global rep
    canvas.itemconfig(timer_text, text=format_duration(seconds))

    if seconds > 0:
        global timer
        timer = window.after(1000, count_down, seconds - 1)
    elif seconds == 0:
        if rep % 2 > 0:
            tick = label_done.cget("text") + "✓"
            label_done.config(text=tick)
        start_timer()


def format_duration(seconds):
    display_min = math.floor(seconds / 60)
    display_sec = seconds % 60

    if display_sec < 10:
        display_sec = f"0{display_sec}"

    return f"{display_min}:{display_sec}"


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

label_timer = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 40, "bold"), bg=YELLOW)
label_timer.grid(row=0, column=1, rowspan=2)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=img)
timer_text = canvas.create_text(100, 130, text=format_duration(WORK_MIN * UNIT_SEC), fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=2, column=1)

button_start = Button(text="Start", highlightthickness=0, command=start_timer)
button_start.grid(row=3, column=0)

button_reset = Button(text="Reset", highlightthickness=0, command=reset_timer)
button_reset.grid(row=3, column=2)

label_done = Label(fg=GREEN, font=(FONT_NAME, 12, "bold"), bg=YELLOW)
label_done.grid(row=4, column=1)

window.mainloop()
