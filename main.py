import tkinter as tk
from tkinter import filedialog
from utils import load_employees, load_tasks, generate_task_table, show_table_image
from genetic import GeneticAlgorithm
from greedy import run_greedy, clear_cache
from firefly import FireflyAlgorithm
import pandas as pd
import copy
import time

root = tk.Tk()
root.title("Smart Task Assignment Dashboard")
root.geometry("1280x800")
root.configure(bg="#f2f4f6")

result_text = None
stats_text = None
img_label = None
algo_choice = tk.StringVar(value="")

loaded = False
stored_results = {}
tasks_list = []
employee_list = []


def save_stats():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        content = stats_text.get(1.0, tk.END)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)


def browse_file():
    global loaded, stored_results, tasks_list, employee_list
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return
    tasks_list = load_tasks(file_path)
    employee_list = load_employees("employees.txt")
    stored_results.clear()

    start = time.time()
    ga = GeneticAlgorithm(copy.deepcopy(employee_list), tasks_list)
    genetic_assignment = ga.run()
    genetic_time = time.time() - start

    start = time.time()
    greedy_assignment, greedy_employees = run_greedy(copy.deepcopy(employee_list), tasks_list, cache_key="greedy")
    greedy_time = time.time() - start

    start = time.time()
    fa = FireflyAlgorithm(copy.deepcopy(employee_list), tasks_list)
    firefly_assignment = fa.run()
    firefly_time = time.time() - start

    stored_results["Genetic"] = (genetic_assignment, copy.deepcopy(employee_list), genetic_time)
    stored_results["Greedy"] = (greedy_assignment, greedy_employees, greedy_time)
    stored_results["Firefly"] = (firefly_assignment, copy.deepcopy(employee_list), firefly_time)

    loaded = True
    result_text.delete(1.0, tk.END)
    stats_text.delete(1.0, tk.END)


def display_results(algo):
    if not loaded or algo not in stored_results:
        return

    assignment, employees, _ = stored_results[algo]
    result_text.delete(1.0, tk.END)
    stats_text.delete(1.0, tk.END)
    assignment_records = []

    for task, emp in zip(tasks_list, assignment):
        if emp is None:
            result_text.insert(tk.END, f"{task.name} ({task.skill} - {task.hours}h) --> ❌ No available employee\n")
            continue
        is_direct = task.skill in emp.skills
        assignment_records.append({
            "Task": task.name,
            "Skill": task.skill,
            "Hours": task.hours,
            "Assigned To": emp.name,
            "Type": "Direct" if is_direct else "Fallback"
        })
        line = f"{task.name} ({task.skill} - {task.hours}h) --> {emp.name}"
        if not is_direct:
            line += " (fallback)"
        result_text.insert(tk.END, line + "\n")

    df = pd.DataFrame(assignment_records)
    if not df.empty:
        generate_task_table(assignment_records)
        show_table_image(img_label, "task_assignment_table.png")
        stats_text.insert(tk.END, f"📌 Total tasks: {len(df)}\n")
        direct = df[df["Type"] == "Direct"].shape[0]
        fallback = df[df["Type"] == "Fallback"].shape[0]
        stats_text.insert(tk.END, f"✅ Direct Assignments: {direct}\n")
        stats_text.insert(tk.END, f"⚠️ Fallback Assignments: {fallback}\n")
        stats_text.insert(tk.END, "\n📋 Employee Load Summary:\n")
        for emp in employees:
            stats_text.insert(tk.END, f"- {emp.name}: {emp.assigned_tasks} task(s), {emp.assigned_hours} hour(s)\n")


def compare_algorithms():
    if not loaded:
        return

    result_text.delete(1.0, tk.END)
    stats_text.delete(1.0, tk.END)

    def count_direct(assignment):
        return sum(1 for task, emp in zip(tasks_list, assignment) if emp and task.skill in emp.skills)

    stats_text.insert(tk.END, "🔎 Comparison Result:\n")
    for algo in ["Genetic", "Greedy", "Firefly"]:
        assignment, _, exec_time = stored_results[algo]
        direct = count_direct(assignment)
        stats_text.insert(tk.END, f"{algo} - Direct Assignments: {direct}, Time: {exec_time:.3f} seconds\n")

    best = max(
        [("Genetic", count_direct(stored_results["Genetic"][0])),
         ("Greedy", count_direct(stored_results["Greedy"][0])),
         ("Firefly", count_direct(stored_results["Firefly"][0]))],
        key=lambda x: x[1]
    )
    stats_text.insert(tk.END, f"\n✅ Best performer in direct assignments: {best[0]}\n")


def show_section(section):
    result_text.pack_forget()
    stats_text.pack_forget()
    img_label.pack_forget()
    if section == "result":
        result_text.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=False)
    elif section == "stats":
        stats_text.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=False)
    elif section == "img":
        img_label.pack(pady=10)

# === GUI Layout ===
header = tk.Label(root, text="📊 Smart Task Assignment Dashboard", font=("Segoe UI", 20, "bold"), bg="#f2f4f6", fg="#2d3436")
header.pack(pady=15)

button_frame = tk.Frame(root, bg="#f2f4f6")
button_frame.pack(pady=10)

btn_style = {"font": ("Arial", 12), "padx": 8, "pady": 6}

tk.Button(button_frame, text="📂 Load Task File", command=browse_file, bg="#dfe6e9", **btn_style).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="🔁 Show Genetic Result", command=lambda: display_results("Genetic"), bg="#b2bec3", **btn_style).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="⚡ Show Greedy Result", command=lambda: display_results("Greedy"), bg="#ffeaa7", **btn_style).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="🔥🐝 Show Firefly Result", command=lambda: display_results("Firefly"), bg="#a29bfe", **btn_style).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="📊 Compare All Algorithms", command=compare_algorithms, bg="#fab1a0", **btn_style).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="💾 Save Stats", command=save_stats, bg="#55efc4", **btn_style).pack(side=tk.LEFT, padx=5)


section_frame = tk.Frame(root, bg="#f2f4f6")
section_frame.pack(pady=5)

tk.Button(section_frame, text="📝 Assignment Result", command=lambda: show_section("result"), bg="#fab1a0", **btn_style).pack(side=tk.LEFT, padx=5)
tk.Button(section_frame, text="📈 Statistics", command=lambda: show_section("stats"), bg="#81ecec", **btn_style).pack(side=tk.LEFT, padx=5)
tk.Button(section_frame, text="🖼️ Table", command=lambda: show_section("img"), bg="#ffeaa7", **btn_style).pack(side=tk.LEFT, padx=5)


result_text = tk.Text(root, height=12, font=("Segoe UI", 15), wrap=tk.WORD, bd=2, relief=tk.SUNKEN)
stats_text = tk.Text(root, height=10, font=("Segoe UI", 15), wrap=tk.WORD, bd=2, relief=tk.SUNKEN)
img_label = tk.Label(root, bg="#ffffff", bd=2, relief=tk.SOLID)


root.mainloop()
