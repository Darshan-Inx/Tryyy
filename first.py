import random
import string
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from colorama import init, Fore, Style

init(autoreset=True)


class Task:
    def __init__(self, title: str, priority: int, due_date: datetime, tags: Optional[List[str]] = None):
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = False
        self.tags = tags or []

    def mark_done(self):
        self.completed = True

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "due_date": self.due_date.isoformat(),
            "completed": self.completed,
            "tags": self.tags,
        }

    @staticmethod
    def from_dict(data):
        task = Task(
            data["title"],
            data["priority"],
            datetime.fromisoformat(data["due_date"]),
            data.get("tags", [])
        )
        task.completed = data.get("completed", False)
        return task

    def __repr__(self):
        status = f"{Fore.GREEN}✅{Style.RESET_ALL}" if self.completed else f"{Fore.RED}❌{Style.RESET_ALL}"
        tag_str = f" [{', '.join(self.tags)}]" if self.tags else ""
        return f"{status} {self.title}{tag_str} (Priority: {self.priority}, Due: {self.due_date.strftime('%Y-%m-%d')})"


class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, title: str, priority: int, days_until_due: int, tags: Optional[List[str]] = None):
        due_date = datetime.now() + timedelta(days=days_until_due)
        self.tasks.append(Task(title, priority, due_date, tags))

    def mark_task_done(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_done()

    def delete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def upcoming_tasks(self) -> List[Task]:
        return sorted(
            [t for t in self.tasks if not t.completed],
            key=lambda x: (x.priority, x.due_date, x.title),
        )

    def overdue_tasks(self) -> List[Task]:
        now = datetime.now()
        return sorted(
            [t for t in self.tasks if not t.completed and t.due_date < now],
            key=lambda x: x.due_date
        )

    def completed_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.completed]

    def search_tasks(self, keyword: str) -> List[Task]:
        return [t for t in self.tasks if keyword.lower() in t.title.lower()]

    def summary(self) -> Dict[str, int]:
        return {
            "total": len(self.tasks),
            "completed": len(self.completed_tasks()),
            "pending": len([t for t in self.tasks if not t.completed]),
            "overdue": len(self.overdue_tasks()),
        }

    def save_to_file(self, filename="tasks.json"):
        with open(filename, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    def load_from_file(self, filename="tasks.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(d) for d in data]
        except FileNotFoundError:
            self.tasks = []

    def __repr__(self):
        lines = [f"Task Manager ({len(self.tasks)} tasks)"]
        for i, task in enumerate(self.tasks):
            lines.append(f"{i}. {task}")
        return "\n".join(lines)


def random_title(length=6) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def seed_tasks(manager: TaskManager, n: int = 10):
    sample_tags = [["work"], ["personal"], ["urgent"], ["low"]]
    for _ in range(n):
        title = random_title()
        priority = random.randint(1, 5)
        days_until_due = random.randint(-3, 10)
        tags = random.choice(sample_tags)
        manager.add_task(title, priority, days_until_due, tags)


def main():
    manager = TaskManager()
    manager.load_from_file()
    seed_tasks(manager, 5)

    while True:
        print("\n📋 Task Manager Menu:")
        print("1. Show all tasks")
        print("2. Add a task")
        print("3. Complete a task")
        print("4. Delete a task")
        print("5. Upcoming tasks")
        print("6. Overdue tasks")
        print("7. Completed tasks")
        print("8. Search tasks")
        print("9. Summary")
        print("0. Exit")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            print(manager)
        elif choice == "2":
            title = input("Title: ")
            priority = int(input("Priority (1-5): "))
            days = int(input("Days until due: "))
            tags = input("Tags (comma separated): ").split(",") if input else []
            manager.add_task(title, priority, days, tags)
        elif choice == "3":
            index = int(input("Task index to complete: "))
            manager.mark_task_done(index)
        elif choice == "4":
            index = int(input("Task index to delete: "))
            manager.delete_task(index)
        elif choice == "5":
            print("\n--- Upcoming Tasks ---")
            for t in manager.upcoming_tasks():
                print(t)
        elif choice == "6":
            print("\n--- Overdue Tasks ---")
            for t in manager.overdue_tasks():
                print(t)
        elif choice == "7":
            print("\n--- Completed Tasks ---")
            for t in manager.completed_tasks():
                print(t)
        elif choice == "8":
            keyword = input("Keyword to search: ")
            for t in manager.search_tasks(keyword):
                print(t)
        else:
            return


if __name__ == "__main__":
    main()
