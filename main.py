import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

parser = argparse.ArgumentParser()

parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by ID")
parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
parser.add_argument("-clr", "--clear", help="Clear all tasks", action="store_true")

parser.add_argument("task", type=str, nargs="?", help="Task to add")

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if args.list:
    tasks = load_tasks()
    if len(tasks) == 0:
        print("No tasks found")
    else:
        for task in tasks:
            status = "x" if task["done"] else " "
            print(f"[{status}] {task['id']}: {task['task']}")
    sys.exit(0)
elif args.complete:
    tasks = load_tasks()
    found_task = False
    for task in tasks:
        if task["id"] == args.complete:
            found_task = True
            task["done"] = True
            save_tasks(tasks)
            print(f"Task {args.complete} marked as complete")
            break
    if not found_task:
        print(f"Task with ID of {args.complete} not found")
elif args.delete:
    tasks = load_tasks()
    found_task = False
    for task in tasks:
        if task["id"] == args.delete:
            found_task = True
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Task with ID of {args.delete} deleted")
    if not found_task:
        print(f"Task with ID of {args.delete} not found")
elif args.clear:
    save_tasks([])
    print("All tasks have been cleared")
elif args.task:
    tasks = load_tasks()
    if len(tasks) == 0:
        new_id = 1
    else:
        new_id = tasks[-1]["id"] + 1

    tasks.append({"id": new_id, "task": args.task, "done": False})
    save_tasks(tasks)
    
    print(f"Task {args.task} added with ID of {new_id}")