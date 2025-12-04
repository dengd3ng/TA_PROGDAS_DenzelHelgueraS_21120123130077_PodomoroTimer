import tkinter as tk
from tkinter import messagebox
import math

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLUE = "#9bb0de"
GRAY = "#555555"
FONT_NAME = "Courier"

reps = 0
timer = None
tasks = [] 

def get_total_seconds(entry_h, entry_m, entry_s):
    try: h = int(entry_h.get())
    except: h = 0
    try: m = int(entry_m.get())
    except: m = 0
    try: s = int(entry_s.get())
    except: s = 0
    return (h * 3600) + (m * 60) + s

#Tambah Tugas
def push_task():
    task = task_entry.get()
    if task != "":
        tasks.append(task) # Push
        update_task_ui()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Isi nama tugas dulu!")

#Selesai Tugas
def pop_task():
    if tasks:
        completed_task = tasks.pop()
        update_task_ui()
        messagebox.showinfo("Selesai", f"Tugas '{completed_task}' selesai!")
    else:
        messagebox.showwarning("Kosong, Tidak ada Tugas!.")

def update_task_ui():
    task_listbox.delete(0, tk.END)
    for i, task in enumerate(tasks):
        task_listbox.insert(tk.END, f"{i + 1}. {task}")

#Mulai Timer
def start_timer():
    global reps
    reps += 1
    start_button.config(state="disabled")

    work_sec = get_total_seconds(work_h, work_m, work_s)
    short_sec = get_total_seconds(short_h, short_m, short_s)
    long_sec = get_total_seconds(long_h, long_m, long_s)

    if reps % 8 == 0:
        count_down(long_sec)
        title_label.config(text="Long Break", fg=RED, font=(FONT_NAME, 35, "bold"))
    elif reps % 2 == 0:
        count_down(short_sec)
        title_label.config(text="Break", fg=PINK, font=(FONT_NAME, 35, "bold"))
    else:
        count_down(work_sec)
        if tasks:
            current_task = tasks[-1]
            title_label.config(text=f"Fokus: {current_task}", fg=GREEN, font=(FONT_NAME, 15, "bold"))
        else:
            title_label.config(text="Fokus!", fg=GREEN, font=(FONT_NAME, 35, "bold"))

def count_down(count):
    global timer
    
    hours = count // 3600
    remainder = count % 3600
    minutes = remainder // 60
    seconds = remainder % 60
    
    time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    canvas.itemconfig(timer_text, text=time_formatted)

    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)

def reset_timer():
    global reps
    if timer:
        window.after_cancel(timer)
    
    canvas.itemconfig(timer_text, text="00:00:00")
    title_label.config(text="Timer", fg=GREEN, font=(FONT_NAME, 35, "bold"))
    check_marks.config(text="")
    reps = 0
    start_button.config(state="normal")

window = tk.Tk()
window.title("Pomodoro Timer")
window.config(padx=30, pady=30, bg=YELLOW)

title_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
title_label.grid(column=0, row=0, columnspan=4, pady=10)

canvas = tk.Canvas(width=220, height=224, bg=YELLOW, highlightthickness=0)
canvas.create_oval(10, 40, 210, 220, fill=YELLOW, outline=GREEN, width=4)
timer_text = canvas.create_text(110, 130, text="00:00:00", fill="black", font=(FONT_NAME, 30, "bold"))
canvas.grid(column=0, row=1, columnspan=4, pady=10)

tk.Label(window, text="H", bg=YELLOW, font=("Arial", 8, "bold")).grid(row=2, column=1)
tk.Label(window, text="M", bg=YELLOW, font=("Arial", 8, "bold")).grid(row=2, column=2)
tk.Label(window, text="S", bg=YELLOW, font=("Arial", 8, "bold")).grid(row=2, column=3)

def create_input_row(label, r, h_val, m_val, s_val):
    tk.Label(window, text=label, bg=YELLOW, anchor="e").grid(row=r, column=0, sticky="e", padx=5)
    e_h = tk.Entry(window, width=4); e_h.insert(0, str(h_val)); e_h.grid(row=r, column=1, padx=2)
    e_m = tk.Entry(window, width=4); e_m.insert(0, str(m_val)); e_m.grid(row=r, column=2, padx=2)
    e_s = tk.Entry(window, width=4); e_s.insert(0, str(s_val)); e_s.grid(row=r, column=3, padx=2)
    return e_h, e_m, e_s

work_h, work_m, work_s = create_input_row("Kerja:", 3, 0, 0, 0)
short_h, short_m, short_s = create_input_row("Break:", 4, 0, 0, 0)
long_h, long_m, long_s = create_input_row("Long Break:", 5, 0, 0, 0)

start_button = tk.Button(text="Mulai Timer", command=start_timer, bg=GREEN, fg="white")
start_button.grid(column=0, row=6, columnspan=2, pady=10, sticky="ew", padx=2)

reset_button = tk.Button(text="Reset Timer", command=reset_timer, bg=RED, fg="white")
reset_button.grid(column=2, row=6, columnspan=2, pady=10, sticky="ew", padx=2)

check_marks = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15))
check_marks.grid(column=0, row=7, columnspan=4)

tk.Frame(window, height=2, bd=1, relief="sunken", bg=GREEN).grid(row=8, column=0, columnspan=4, sticky="ew", pady=20)
tk.Label(window, text="Tugas", bg=YELLOW, font=(FONT_NAME, 12, "bold")).grid(row=9, column=0, columnspan=4)

task_entry = tk.Entry(window, width=18)
task_entry.grid(row=10, column=0, columnspan=2, pady=5, sticky="ew", padx=2)

add_task_btn = tk.Button(text="Tambah", command=push_task, bg=BLUE, fg="white", width=8)
add_task_btn.grid(row=10, column=2, pady=5, padx=2)

pop_btn = tk.Button(text="Selesai", command=pop_task, bg=RED, fg="white", width=12)
pop_btn.grid(row=10, column=3, pady=5, padx=2)

task_listbox = tk.Listbox(window, height=5, width=35, bg="white")
task_listbox.grid(row=11, column=0, columnspan=4, pady=5)

window.mainloop()