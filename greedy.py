# File: greedy.py
import copy

cached_result = {}



def run_greedy(employees, tasks, cache_key=None, use_cache=True):
    global cached_result
    if use_cache and cache_key and cache_key in cached_result:
        return cached_result[cache_key]

    employees = copy.deepcopy(employees)
    assignment = []
    for task in tasks:
        suitable = [e for e in employees if task.skill in e.skills and e.assigned_hours + task.hours <= e.max_hours]
        if suitable:
            selected = min(suitable, key=lambda e: e.assigned_hours)
            selected.assigned_hours += task.hours
            selected.assigned_tasks += 1
            assignment.append(selected)
        else:
            fallback = [e for e in employees if e.assigned_hours + task.hours <= e.max_hours]
            if fallback:
                selected = min(fallback, key=lambda e: e.assigned_hours)
                selected.assigned_hours += task.hours
                selected.assigned_tasks += 1
                assignment.append(selected)
            else:
                assignment.append(None)

    if use_cache and cache_key:
        cached_result[cache_key] = (assignment, employees)
    return assignment, employees


def clear_cache():
    global cached_result
    cached_result = {}
