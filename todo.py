#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added: {title}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks yet!")
        return

    print(f"\n📋 Your Tasks ({len(tasks)} total):\n")
    for task in tasks:
        status = "✅" if task["done"] else "⭕"
        print(f"{task['id']:2d}. {status} {task['title']}")
    print()


def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"✅ Task #{task_id} marked as done!")
            return
    print(f"❌ Task #{task_id} not found.")


def delete_task(task_id):
    tasks = load_tasks()
    filtered = [t for t in tasks if t["id"] != task_id]
    
    if len(filtered) == len(tasks):
        print(f"❌ Task #{task_id} not found.")
        return
    
    # Re-number tasks
    for i, task in enumerate(filtered):
        task["id"] = i + 1
    
    save_tasks(filtered)
    print(f"🗑️ Task #{task_id} deleted.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python todo.py <command> [arguments]")
        print("\nCommands:")
        print("  add <title>     - Add a new task")
        print("  list            - Show all tasks")
        print("  done <id>       - Mark task as done")
        print("  delete <id>     - Delete a task")
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a task title.")
        else:
            title = " ".join(sys.argv[2:])
            add_task(title)

    elif command == "list":
        list_tasks()

    elif command == "done":
        if len(sys.argv) < 3:
            print("Please provide task ID.")
        else:
            try:
                mark_done(int(sys.argv[2]))
            except ValueError:
                print("Task ID must be a number.")

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Please provide task ID.")
        else:
            try:
                delete_task(int(sys.argv[2]))
            except ValueError:
                print("Task ID must be a number.")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()