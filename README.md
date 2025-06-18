# 🧠 Smart Task Assignment Dashboard

This is a desktop application that intelligently assigns tasks to employees using optimization algorithms.  
It helps distribute tasks efficiently based on employee skills and availability, and provides a visual comparison of algorithm performance.

---

## ⚙️ Algorithms Used

- ✅ **Greedy Algorithm**  
  Quickly assigns each task to the most suitable available employee without looking ahead. It’s fast but not always optimal.

- 🧬 **Genetic Algorithm**  
  Inspired by natural selection, it evolves a population of solutions using crossover and mutation to reach better assignments over generations.

- 🔥 **Firefly Algorithm**  
  A nature-inspired metaheuristic where each firefly (solution) is attracted to brighter (better) ones. The algorithm explores and improves solutions iteratively.

---

## 📊 Dashboard Features

The application includes a dashboard built with **Tkinter** to:

- Load employee and task data
- Show task assignments for each algorithm
- Display direct vs fallback assignments
- Compare total assignment time
- Visualize summary statistics in a table

---

## 🖥️ Technologies Used

- **Python**
- **Tkinter** (GUI)
- **Pandas** (data handling)
- **Matplotlib** (graph/table visualization)

---
📁 smart-task-dashboard
├── main.py                # Main dashboard GUI
├── greedy.py              # Greedy algorithm implementation
├── firefly.py             # Firefly algorithm implementation
├── genetic.py             # Genetic algorithm implementation
├── utils.py               # Helper functions (e.g. loading data)
├── employees.txt          # Sample employee data
├── tasks.txt              # Sample tasks file (loadable by GUI)
└── task_assignment_table.png   # Visual output of task assignments


## 🚀 How to Run

1. Install Python 3.10+  
2. Install required packages (if not already installed):

   ```bash
   pip install pandas matplotlib
