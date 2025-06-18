import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_employees(filename="employees.txt"):
    from models import Employee
    employees = []
    with open(filename, 'r') as f:
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split(',')
            if len(parts) != 3: continue
            name, skills, max_hours = parts
            employees.append(Employee(name, skills, max_hours))
    return employees

def load_tasks(filename):
    from models import Task
    tasks = []
    with open(filename, 'r') as f:
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split(',')
            if len(parts) != 3: continue
            name, skill, hours = parts
            tasks.append(Task(name, skill, hours))
    return tasks

def generate_task_table(assignments, filename="task_assignment_table.png"):
    df = pd.DataFrame(assignments)
    if df.empty:
        return
    row_colors = df["Type"].map({"Direct": "#d4f4dd", "Fallback": "#fff3cd"})
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis("off")
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     loc='center',
                     cellLoc='center',
                     rowColours=row_colors)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    plt.title("Task Assignment Table (Direct = Green, Fallback = Yellow)", fontsize=14, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

def show_table_image(img_label, path):
    try:
        img = Image.open(path)
        img = img.resize((640, 500))
        tk_img = ImageTk.PhotoImage(img)
        img_label.config(image=tk_img)
        img_label.image = tk_img
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")

def show_charts(df, chart_frame):
    for widget in chart_frame.winfo_children():
        widget.destroy()
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    skill_counts = Counter(df["Skill"])
    axs[0].pie(skill_counts.values(), labels=skill_counts.keys(), autopct='%1.1f%%', startangle=140)
    axs[0].set_title("Skill Distribution")
    hours = df.groupby("Assigned To")["Hours"].sum()
    axs[1].bar(hours.index, hours.values)
    axs[1].set_title("Employee Load")
    axs[1].tick_params(axis='x', rotation=45)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)