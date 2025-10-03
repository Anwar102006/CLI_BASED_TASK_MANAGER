"""
Task Manager CLI Application

How to run:
- Make sure you have Python 3 installed.
- Run the app in your terminal:
    python task_manager.py

All tasks are stored in 'tasks.json' in the same directory.
"""

import json
import os
from datetime import datetime
from tabulate import tabulate

TASKS_FILE = 'tasks.json'
DATE_FORMAT = '%Y-%m-%d'
PRIORITY_LEVELS = ['Low', 'Medium', 'High']
STATUS_OPTIONS = ['Pending', 'Completed']

# ---------------------- File Handling ----------------------
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# ---------------------- Utility Functions ----------------------
def generate_task_id(tasks):
    existing_ids = {task['id'] for task in tasks}
    new_id = 1
    while str(new_id) in existing_ids:
        new_id += 1
    return str(new_id)

def validate_date(date_str):
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False

def print_table(tasks):
    if not tasks:
        print('No tasks to display.')
        return
    headers = ['ID', 'Title', 'Description', 'Due Date', 'Status', 'Priority']
    rows = [[t['id'], t['title'], t['description'], t['due_date'], t['status'], t.get('priority', 'Medium')] for t in tasks]
    print(tabulate(rows, headers, tablefmt='grid'))

# ---------------------- Core Features ----------------------
def add_task(tasks):
    print('\n--- Add New Task ---')
    title = input('Enter task title: ').strip()
    description = input('Enter description: ').strip()
    while True:
        due_date = input(f'Enter due date ({DATE_FORMAT}): ').strip()
        if validate_date(due_date):
            break
        print('Invalid date format. Please use YYYY-MM-DD.')
    while True:
        priority = input(f'Enter priority ({'/'.join(PRIORITY_LEVELS)}): ').strip().capitalize()
        if priority in PRIORITY_LEVELS:
            break
        print('Invalid priority. Choose from Low, Medium, High.')
    task_id = generate_task_id(tasks)
    task = {
        'id': task_id,
        'title': title,
        'description': description,
        'due_date': due_date,
        'status': 'Pending',
        'priority': priority
    }
    tasks.append(task)
    save_tasks(tasks)
    print('Task added successfully!')

def view_tasks(tasks):
    print('\n--- All Tasks ---')
    print_table(tasks)

def update_task(tasks):
    print('\n--- Update Task ---')
    task_id = input('Enter Task ID to update: ').strip()
    for task in tasks:
        if task['id'] == task_id:
            print(f"Current Description: {task['description']}")
            desc = input('New Description (leave blank to keep): ').strip()
            if desc:
                task['description'] = desc
            print(f"Current Due Date: {task['due_date']}")
            while True:
                due = input(f'New Due Date ({DATE_FORMAT}, leave blank to keep): ').strip()
                if not due:
                    break
                if validate_date(due):
                    task['due_date'] = due
                    break
                print('Invalid date format.')
            print(f"Current Status: {task['status']}")
            status = input('New Status (Pending/Completed, leave blank to keep): ').strip().capitalize()
            if status in STATUS_OPTIONS:
                task['status'] = status
            print(f"Current Priority: {task.get('priority', 'Medium')}")
            priority = input('New Priority (Low/Medium/High, leave blank to keep): ').strip().capitalize()
            if priority in PRIORITY_LEVELS:
                task['priority'] = priority
            save_tasks(tasks)
            print('Task updated successfully!')
            return
    print('Task ID not found.')

def mark_completed(tasks):
    print('\n--- Mark Task as Completed ---')
    task_id = input('Enter Task ID to mark as completed: ').strip()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'Completed'
            save_tasks(tasks)
            print('Task marked as completed!')
            return
    print('Task ID not found.')

def delete_task(tasks):
    print('\n--- Delete Task ---')
    task_id = input('Enter Task ID to delete: ').strip()
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks.pop(i)
            save_tasks(tasks)
            print('Task deleted successfully!')
            return
    print('Task ID not found.')

def search_tasks(tasks):
    print('\n--- Search Tasks ---')
    keyword = input('Enter keyword to search (title/description): ').strip().lower()
    found = [t for t in tasks if keyword in t['title'].lower() or keyword in t['description'].lower()]
    print_table(found)

def filter_tasks(tasks):
    print('\n--- Filter Tasks ---')
    print('1. Pending')
    print('2. Completed')
    print('3. By Priority')
    choice = input('Select filter option: ').strip()
    if choice == '1':
        filtered = [t for t in tasks if t['status'] == 'Pending']
    elif choice == '2':
        filtered = [t for t in tasks if t['status'] == 'Completed']
    elif choice == '3':
        pr = input(f'Enter priority ({'/'.join(PRIORITY_LEVELS)}): ').strip().capitalize()
        if pr in PRIORITY_LEVELS:
            filtered = [t for t in tasks if t.get('priority', 'Medium') == pr]
        else:
            print('Invalid priority.')
            return
    else:
        print('Invalid option.')
        return
    print_table(filtered)

def task_summary(tasks):
    print('\n--- Task Summary ---')
    total = len(tasks)
    pending = sum(1 for t in tasks if t['status'] == 'Pending')
    completed = sum(1 for t in tasks if t['status'] == 'Completed')
    print(f'Total tasks: {total}')
    print(f'Pending tasks: {pending}')
    print(f'Completed tasks: {completed}')

def sort_tasks(tasks):
    print('\n--- Sort Tasks by Due Date ---')
    sorted_tasks = sorted(tasks, key=lambda t: t['due_date'])
    print_table(sorted_tasks)

def export_to_csv(tasks):
    import csv
    filename = 'tasks_export.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Title', 'Description', 'Due Date', 'Status', 'Priority'])
        for t in tasks:
            writer.writerow([t['id'], t['title'], t['description'], t['due_date'], t['status'], t.get('priority', 'Medium')])
    print(f'Tasks exported to {filename}')

# ---------------------- Main Menu ----------------------
def main():
    tasks = load_tasks()
    while True:
        print('\n==== Task Manager ====')
        print('1. Add Task')
        print('2. View Tasks')
        print('3. Update Task')
        print('4. Mark Task as Completed')
        print('5. Delete Task')
        print('6. Search Tasks')
        print('7. Filter Tasks')
        print('8. Task Summary')
        print('9. Sort Tasks by Due Date')
        print('10. Export Tasks to CSV')
        print('11. Exit')
        choice = input('Select an option (1-11): ').strip()
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            update_task(tasks)
        elif choice == '4':
            mark_completed(tasks)
        elif choice == '5':
            delete_task(tasks)
        elif choice == '6':
            search_tasks(tasks)
        elif choice == '7':
            filter_tasks(tasks)
        elif choice == '8':
            task_summary(tasks)
        elif choice == '9':
            sort_tasks(tasks)
        elif choice == '10':
            export_to_csv(tasks)
        elif choice == '11':
            print('Goodbye!')
            break
        else:
            print('Invalid option. Please enter a number from 1 to 11.')

if __name__ == '__main__':
    main()
