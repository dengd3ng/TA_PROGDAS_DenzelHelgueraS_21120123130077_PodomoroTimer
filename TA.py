import tkinter as tk
from tkinter import messagebox
import math
from datetime import datetime

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
history_log = []

def get_total_seconds(entry_h, entry_m, entry_s):
    try:
        h = int(entry_h.get())
    except:
        h = 0
    try:
        m = int(entry_m.get())
    except:
        m = 0
    try:
        s = int(entry_s.get())
    except:
        s = 0
    return (h * 3600) + (m * 60) + s


def clear_history():
    global history_log
    if not history_log:
        messagebox.showinfo("Riwayat", "Riwayat sudah kosong.")
        return
    if messagebox.askyesno("Konfirmasi", "Hapus semua riwayat?"):
        history_log.clear()
        try:
            history_listbox.delete(0, tk.END)
            history_listbox.insert(tk.END, "Belum ada sesi selesai.")
        except NameError:
            pass

def save_to_history():
    now = datetime.now().strftime("%H:%M")
    session_num = math.ceil(reps / 2)
    if tasks:
        task_name = tasks[-1]
    else:
        task_name = "Tanpa Tugas"
    log_entry = f"[{now}] Sesi {session_num}: {task_name}"
    history_log.append(log_entry)
    try:
        history_listbox.insert(tk.END, log_entry)
    except NameError:
        pass

def show_history_window():
    history_window = tk.Toplevel(window)
    history_window.title("Riwayat Fokus")
    history_window.geometry("400x300")
    lbl = tk.Label(history_window, text="Riwayat Sesi Selesai", font=("Arial", 12, "bold"))
    lbl.pack(pady=10)
    history_list = tk.Listbox(history_window, width=50, height=15)
    history_list.pack(padx=10, pady=5)
    if not history_log:
        history_list.insert(tk.END, "Belum ada sesi selesai.")
    else:
        for item in history_log:
            history_list.insert(tk.END, item)
    close_btn = tk.Button(history_window, text="Tutup", command=history_window.destroy)
    close_btn.pack(pady=6)

def add_task():
    task = task_entry.get()
    if task != "":
        tasks.append(task)
        update_task_ui()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Isi nama tugas dulu!")

def delete_selected_task():
    try:
        selected_index = task_listbox.curselection()[0]
        tasks.pop(selected_index)
        update_task_ui()
    except IndexError:
        messagebox.showwarning("Pilih Tugas", "Klik tugas di daftar untuk menghapusnya.")

def update_task_ui():
    task_listbox.delete(0, tk.END)
    for i, task in enumerate(tasks):
        task_listbox.insert(tk.END, f"{i + 1}. {task}")

def start_timer():
    global reps
    reps += 1
    start_button.config(state="disabled")
    work_sec = get_total_seconds(work_h, work_m, work_s)
    short_sec = get_total_seconds(short_h, short_m, short_s)
    long_sec = get_total_seconds(long_h, long_m, long_s)
    if reps % 8 == 0:
        count_down(long_sec)
        title_label.config(text="Istirahat Pjg", fg=RED, font=(FONT_NAME, 35, "bold"))
    elif reps % 2 == 0:
        count_down(short_sec)
        title_label.config(text="Istirahat", fg=PINK, font=(FONT_NAME, 35, "bold"))
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
        if reps % 2 != 0:
            save_to_history()
        start_timer()
        current_session = math.ceil(reps / 2)
        check_marks.config(text=f"Sesi ke-{current_session}")

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
window.title("Pomodoro Timer + History")
window.config(padx=30, pady=30, bg=YELLOW)

title_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
title_label.grid(column=0, row=0, columnspan=4, pady=10)

canvas = tk.Canvas(width=220, height=224, bg=YELLOW, highlightthickness=0)
canvas.create_oval(10, 40, 210, 220, fill=YELLOW, outline=GREEN, width=4)
timer_text = canvas.create_text(110, 130, text="00:00:00", fill="black", font=(FONT_NAME, 30, "bold"))
canvas.grid(column=0, row=1, columnspan=4, pady=10)

tk.Label(window, text="Jam", bg=YELLOW, font=("Arial", 8, "bold")).grid(row=2, column=1)
tk.Label(window, text="Mnt", bg=YELLOW, font=("Arial", 8, "bold")).grid(row=2, column=2)
tk.Label(window, text="Dtk", bg=YELLOW, font=("Arial", 8, "bold")).grid(row=2, column=3)

def create_input_row(label, r, h_val, m_val, s_val):
    tk.Label(window, text=label, bg=YELLOW, anchor="e").grid(row=r, column=0, sticky="e", padx=5)
    e_h = tk.Entry(window, width=4)
    e_h.insert(0, str(h_val))
    e_h.grid(row=r, column=1, padx=2)
    e_m = tk.Entry(window, width=4)
    e_m.insert(0, str(m_val))
    e_m.grid(row=r, column=2, padx=2)
    e_s = tk.Entry(window, width=4)
    e_s.insert(0, str(s_val))
    e_s.grid(row=r, column=3, padx=2)
    return e_h, e_m, e_s

work_h, work_m, work_s = create_input_row("Fokus:", 3, 0, 25, 0)
short_h, short_m, short_s = create_input_row("Istirahat Pdk:", 4, 0, 5, 0)
long_h, long_m, long_s = create_input_row("Istirahat Pjg:", 5, 0, 20, 0)

start_button = tk.Button(text="Mulai Timer", command=start_timer, bg=GREEN, fg="white")
start_button.grid(column=0, row=6, columnspan=2, pady=10, sticky="ew", padx=2)

reset_button = tk.Button(text="Reset Timer", command=reset_timer, bg=RED, fg="white")
reset_button.grid(column=2, row=6, columnspan=2, pady=10, sticky="ew", padx=2)

check_marks = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15))
check_marks.grid(column=0, row=7, columnspan=4)

tk.Frame(window, height=2, bd=1, relief="sunken", bg=GREEN).grid(row=8, column=0, columnspan=4, sticky="ew", pady=20)
tk.Label(window, text="Daftar Tugas", bg=YELLOW, font=(FONT_NAME, 12, "bold")).grid(row=9, column=0, columnspan=4)

task_entry = tk.Entry(window, width=18)
task_entry.grid(row=10, column=0, columnspan=2, pady=5, sticky="ew", padx=2)

add_task_btn = tk.Button(text="Tambah", command=add_task, bg=BLUE, fg="white", width=8)
add_task_btn.grid(row=10, column=2, pady=5, padx=2)

delete_btn = tk.Button(text="Hapus", command=delete_selected_task, bg=GRAY, fg="white", width=8)
delete_btn.grid(row=10, column=3, pady=5, padx=2)

task_listbox = tk.Listbox(window, height=5, width=35, bg="white")
task_listbox.grid(row=11, column=0, columnspan=4, pady=5)

history_frame = tk.Frame(window, bg=YELLOW)
history_frame.grid(row=0, column=4, rowspan=12, padx=(10,0), sticky="n")

tk.Label(history_frame, text="Riwayat Sesi", bg=YELLOW, font=(FONT_NAME, 12, "bold")).pack(pady=(6,4))
history_listbox = tk.Listbox(history_frame, width=40, height=18, bg="white")
history_listbox.pack(padx=6, pady=4)

if not history_log:
    history_listbox.insert(tk.END, "Belum ada sesi selesai.")
else:
    for item in history_log:
        history_listbox.insert(tk.END, item)

btn_frame_side = tk.Frame(history_frame, bg=YELLOW)
btn_frame_side.pack(pady=6)

clear_side_btn = tk.Button(btn_frame_side, text="Hapus Riwayat", command=clear_history, width=14)
clear_side_btn.grid(row=0, column=0, padx=4)

history_btn = tk.Button(window, text="Buka Riwayat (Popup)", command=show_history_window, bg=YELLOW, fg="black", relief="groove")
history_btn.grid(row=12, column=0, columnspan=4, pady=10, sticky="ew")

window.mainloop()