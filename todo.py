#!/usr/bin/env python3
import json
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional

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


def add_task(title: str, priority: str = "medium", due: Optional[str] = None):
    tasks = load_tasks()
    
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority.lower(),
        "due": due,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added: {title} [Priority: {priority.upper()}]")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks yet!")
        return

    print(f"\n📋 Your Tasks ({len(tasks)} total):\n")
    for task in tasks:
        status = "✅" if task["done"] else "⭕"
        priority_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.get("priority", "medium"), "🟡")
        
        due_str = f" | 📅 {task['due']}" if task.get("due") else ""
        print(f"{task['id']:2d}. {status} {priority_color} {task['title']}{due_str}")
    print()


def mark_done(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"✅ Task #{task_id} marked as done!")
            return
    print(f"❌ Task #{task_id} not found.")


def delete_task(task_id: int):
    tasks = load_tasks()
    filtered = [t for t in tasks if t["id"] != task_id]
    
    if len(filtered) == len(tasks):
        print(f"❌ Task #{task_id} not found.")
        return
    
    for i, task in enumerate(filtered):
        task["id"] = i + 1
    
    save_tasks(filtered)
    print(f"🗑️ Task #{task_id} deleted.")


def show_stats():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet!")
        return

    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    pending = total - done
    
    overdue = 0
    today = date.today()
    for task in tasks:
        if not task["done"] and task.get("due"):
            try:
                due_date = datetime.strptime(task["due"], "%Y-%m-%d").date()
                if due_date < today:
                    overdue += 1
            except:
                pass

    print("\n📊 Todo Statistics")
    print("=" * 30)
    print(f"Total Tasks     : {total}")
    print(f"✅ Completed    : {done}")
    print(f"⭕ Pending      : {pending}")
    print(f"⚠️  Overdue      : {overdue}")
    print("=" * 30)


def main():
    if len(sys.argv) < 2:
        print("Usage: python todo.py <command> [arguments]")
        print("\nCommands:")
        print("  add <title> [--priority high/medium/low] [--due YYYY-MM-DD]")
        print("  list")
        print("  done <id>")
        print("  delete <id>")
        print("  stats")
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a task title.")
            return
        
        title_parts = []
        priority = "medium"
        due = None
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--due" and i + 1 < len(sys.argv):
                due = sys.argv[i + 1]
                i += 2
            else:
                title_parts.append(sys.argv[i])
                i += 1
        
        title = " ".join(title_parts)
        add_task(title, priority, due)

    elif command == "list":
        list_tasks()

    elif command == "done":
        try:
            mark_done(int(sys.argv[2]))
        except (IndexError, ValueError):
            print("Please provide a valid task ID.")

    elif command == "delete":
        try:
            delete_task(int(sys.argv[2]))
        except (IndexError, ValueError):
            print("Please provide a valid task ID.")

    elif command == "stats":
        show_stats()

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()