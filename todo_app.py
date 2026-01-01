"""
Evolution of Todo - Phase I
In-memory Python console application for single user task management.
"""
from typing import List, Optional


class Task:
    """
    Represents a single todo item in the application.

    Attributes:
        id (int): Sequential numeric identifier, auto-assigned, unique
        description (str): Text content describing the task, non-empty
        completed (bool): Status indicator, true if complete, false if incomplete
    """

    def __init__(self, task_id: int, description: str, completed: bool = False):
        """
        Initialize a Task object.

        Args:
            task_id (int): The unique identifier for the task
            description (str): The task description
            completed (bool): Whether the task is completed (default: False)
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if not isinstance(description, str) or not description.strip():
            raise ValueError("Task description must be a non-empty string")

        self.id = task_id
        self.description = description.strip()
        self.completed = completed

    def __repr__(self):
        """String representation of the Task object."""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}. {self.description}"

    def to_dict(self):
        """Convert the Task object to a dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed
        }


class TodoApp:
    """
    Main Todo application class that manages tasks in memory.
    """

    def __init__(self):
        """Initialize the Todo application with empty task list and ID counter."""
        self.tasks: List[Task] = []
        self.next_id = 1

    def _validate_description(self, description: str) -> bool:
        """
        Validate that the task description is not empty or contains only whitespace.

        Args:
            description (str): The description to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(description, str):
            return False
        return bool(description.strip())

    def _get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Find and return a task by its ID.

        Args:
            task_id (int): The ID of the task to find

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def add_task(self, description: str) -> Task:
        """
        Add a new task to the application.

        Args:
            description (str): The description of the task

        Returns:
            Task: The newly created task

        Raises:
            ValueError: If the description is invalid
        """
        if not self._validate_description(description):
            raise ValueError("Task description must be a non-empty string")

        task = Task(self.next_id, description, completed=False)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the application.

        Returns:
            List[Task]: All tasks in the application
        """
        return self.tasks[:]

    def update_task(self, task_id: int, new_description: str) -> bool:
        """
        Update a task's description by ID.

        Args:
            task_id (int): The ID of the task to update
            new_description (str): The new description for the task

        Returns:
            bool: True if the task was updated, False if not found

        Raises:
            ValueError: If the new description is invalid
        """
        if not self._validate_description(new_description):
            raise ValueError("Task description must be a non-empty string")

        task = self._get_task_by_id(task_id)
        if task is None:
            return False

        task.description = new_description.strip()
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if not found
        """
        task = self._get_task_by_id(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        return True

    def mark_task_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete by ID.

        Args:
            task_id (int): The ID of the task to mark complete

        Returns:
            bool: True if the task was marked complete, False if not found
        """
        task = self._get_task_by_id(task_id)
        if task is None:
            return False

        task.completed = True
        return True

    def mark_task_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete by ID.

        Args:
            task_id (int): The ID of the task to mark incomplete

        Returns:
            bool: True if the task was marked incomplete, False if not found
        """
        task = self._get_task_by_id(task_id)
        if task is None:
            return False

        task.completed = False
        return True


class TodoCLI:
    """
    Command-line interface for the Todo application.
    """

    def __init__(self):
        """Initialize the CLI with a TodoApp instance."""
        self.app = TodoApp()

    def display_menu(self):
        """Display the main menu options to the user."""
        print("\n" + "="*40)
        print("TODO APPLICATION")
        print("="*40)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")
        print("="*40)

    def get_user_choice(self) -> str:
        """
        Get and validate user menu selection.

        Returns:
            str: The user's menu choice
        """
        try:
            choice = input("Enter your choice (1-7): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\n\nOperation cancelled by user.")
            return "7"  # Return exit option

    def handle_add_task(self):
        """Handle the add task functionality."""
        try:
            description = input("Enter task description: ").strip()
            if not self.app._validate_description(description):
                print("Error: Task description cannot be empty.")
                return

            task = self.app.add_task(description)
            print(f"Task added successfully with ID: {task.id}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_view_tasks(self):
        """Handle the view tasks functionality."""
        tasks = self.app.get_all_tasks()

        if not tasks:
            print("\nNo tasks found. Your list is empty!")
            return

        print("\nYour Tasks:")
        print("-" * 50)
        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"[{status}] {task.id}. {task.description}")

    def handle_update_task(self):
        """Handle the update task functionality."""
        try:
            task_id_str = input("Enter task ID to update: ").strip()
            if not task_id_str.isdigit():
                print("Error: Task ID must be a number.")
                return

            task_id = int(task_id_str)
            task = self.app._get_task_by_id(task_id)
            if task is None:
                print(f"Error: Task with ID {task_id} not found.")
                return

            new_description = input(f"Enter new description for task {task_id}: ").strip()
            if not self.app._validate_description(new_description):
                print("Error: Task description cannot be empty.")
                return

            if self.app.update_task(task_id, new_description):
                print(f"Task {task_id} updated successfully.")
            else:
                print(f"Error: Could not update task {task_id}.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_delete_task(self):
        """Handle the delete task functionality."""
        try:
            task_id_str = input("Enter task ID to delete: ").strip()
            if not task_id_str.isdigit():
                print("Error: Task ID must be a number.")
                return

            task_id = int(task_id_str)
            if self.app.delete_task(task_id):
                print(f"Task {task_id} deleted successfully.")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_mark_complete(self):
        """Handle marking a task as complete."""
        try:
            task_id_str = input("Enter task ID to mark complete: ").strip()
            if not task_id_str.isdigit():
                print("Error: Task ID must be a number.")
                return

            task_id = int(task_id_str)
            if self.app.mark_task_complete(task_id):
                print(f"Task {task_id} marked as complete.")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_mark_incomplete(self):
        """Handle marking a task as incomplete."""
        try:
            task_id_str = input("Enter task ID to mark incomplete: ").strip()
            if not task_id_str.isdigit():
                print("Error: Task ID must be a number.")
                return

            task_id = int(task_id_str)
            if self.app.mark_task_incomplete(task_id):
                print(f"Task {task_id} marked as incomplete.")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo Application!")
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.handle_add_task()
            elif choice == "2":
                self.handle_view_tasks()
            elif choice == "3":
                self.handle_update_task()
            elif choice == "4":
                self.handle_delete_task()
            elif choice == "5":
                self.handle_mark_complete()
            elif choice == "6":
                self.handle_mark_incomplete()
            elif choice == "7":
                print("Thank you for using the Todo Application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")


def main():
    """Main entry point for the application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()