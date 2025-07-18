# todo.py

TASKS_FILE = "tasks.txt"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

def show_tasks(tasks):
    if not tasks:
        print("No tasks in your to-do list.")
    else:
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task}")

def main():
    tasks = load_tasks()

    while True:
        print("\n--- TO-DO LIST MENU ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Remove task")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            task = input("Enter the new task: ").strip()
            tasks.append(task)
            save_tasks(tasks)
            print("Task added.")
        elif choice == "3":
            show_tasks(tasks)
            index = int(input("Enter task number to remove: ")) - 1
            if 0 <= index < len(tasks):
                removed = tasks.pop(index)
                save_tasks(tasks)
                print(f"Removed: {removed}")
            else:
                print("Invalid task number.")
        elif choice == "4":
            print("Exiting the app. Bye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
