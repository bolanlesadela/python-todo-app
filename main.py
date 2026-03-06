import customtkinter as ctk
from datetime import datetime
import json
import os

# App settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Data Handling
TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# App
app = ctk.CTk()
app.geometry("600x700")
app.title("My To-Do App")
app.resizable(False, False)

tasks = load_tasks()

# Header
header = ctk.CTkLabel(app, text="My To-Do List", font=ctk.CTkFont(size=20, weight="bold"))
header.pack(pady=(30, 5))


clock_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=13), text_color="gray")
clock_label.pack()

def update_clock():
    now = datetime.now().strftime("%A, %d %B %Y | %H:%M:%S")
    clock_label.configure(text=now)
    app.after(1000, update_clock)

update_clock()

# Input Area
input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.pack(pady=20, padx=30, fill="x")

task_input = ctk.CTkEntry(input_frame, placeholder_text="Enter a task...", height=40, font=ctk.CTkFont(size=14))
task_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

priority_var = ctk.StringVar(value="Medium")
priority_menu = ctk.CTkOptionMenu(input_frame, values=["High", "Medium", "Low"], variable=priority_var, width=100)
priority_menu.pack(side="right")

# Add Button
def add_task():
    text = task_input.get().strip()
    if text:
        task = {"text": text, "priority": priority_var.get(), "done": False}
        tasks.append(task)
        save_tasks(tasks)
        task_input.delete(0, "end")
        refresh_tasks()

add_btn = ctk.CTkButton(app, text="+ Add Task", height=40, font=ctk.CTkFont(size=14, weight="bold"), command=add_task)
add_btn.pack(padx=30, fill="x")

# Task list
scroll_frame = ctk.CTkScrollableFrame(app, label_text="Tasks", height=350)
scroll_frame.pack(pady=20, padx=30, fill="both", expand=True)

priority_colors = {"High": "#FF6B6B", "Medium": "#FFD93D", "Low": "#6BCB77"}

def complete_task(i):
    tasks[i]["done"] = not tasks[i]["done"]
    save_tasks(tasks)
    refresh_tasks()

def delete_task(i):
    tasks.pop(i)
    save_tasks(tasks)
    refresh_tasks()

def refresh_tasks():
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    if not tasks:
        empty = ctk.CTkLabel(scroll_frame, text="No tasks yet. Add one above!", text_color="gray", font=ctk.CTkFont(size=13))
        empty.pack(pady=20)
        return

    for i, task in enumerate(tasks):
        row = ctk.CTkFrame(scroll_frame, corner_radius=10)
        row.pack(fill="x", pady=5)

        color = priority_colors[task["priority"]]
        indicator = ctk.CTkLabel(row, text="●", text_color=color, font=ctk.CTkFont(size=18), width=30)
        indicator.pack(side="left", padx=(10, 5))

        style = "overstrike" if task["done"] else "normal"
        text_color = "gray" if task["done"] else "white"
        task_label = ctk.CTkLabel(row, text=task["text"], font=ctk.CTkFont(size=14, overstrike=task["done"]),
                                  text_color=text_color, anchor="w")
        task_label.pack(side="left", fill="x", expand=True, padx=5)

        priority_badge = ctk.CTkLabel(row, text=task["priority"], text_color=color,
                                      font=ctk.CTkFont(size=11), width=60)
        priority_badge.pack(side="left", padx=5)

        done_btn = ctk.CTkButton(row, text="✓", width=35, height=28,
                                 fg_color="transparent", border_width=1,
                                 command=lambda i=i: complete_task(i))
        done_btn.pack(side="right", padx=5, pady=5)

        del_btn = ctk.CTkButton(row, text="✕", width=35, height=28,
                                fg_color="transparent", border_width=1,
                                text_color="#FF6B6B", border_color="#FF6B6B",
                                command=lambda i=i: delete_task(i))
        del_btn.pack(side="right", padx=(0, 5), pady=5)

refresh_tasks()

# Progress Bar
progress_frame = ctk.CTkFrame(app, fg_color="transparent")
progress_frame.pack(padx=30, fill="x", pady=(0, 20))

progress_label = ctk.CTkLabel(progress_frame, text="", font=ctk.CTkFont(size=12), text_color="gray")
progress_label.pack(anchor="w", pady=(0, 4))

progress_bar = ctk.CTkProgressBar(progress_frame)
progress_bar.pack(fill="x")
progress_bar.set(0)

def update_progress():
    if tasks:
        done = sum(1 for t in tasks if t["done"])
        ratio = done / len(tasks)
        progress_bar.set(ratio)
        progress_label.configure(text=f"{done} of {len(tasks)} tasks completed")
    else:
        progress_bar.set(0)
        progress_label.configure(text="No tasks yet")
    app.after(500, update_progress)

update_progress()

app.mainloop()