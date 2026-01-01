"""
Tests for the Todo Application.

This module contains unit tests for all functionality specified in the
Phase I specification and implementation plan.
"""

import pytest
from todo_app import Task, TodoApp


class TestTaskClass:
    """Test the Task class functionality."""

    def test_task_creation_valid(self):
        """Test creating a valid Task object."""
        task = Task(1, "Test description")
        assert task.id == 1
        assert task.description == "Test description"
        assert task.completed is False

    def test_task_creation_with_completion_status(self):
        """Test creating a Task with completed status."""
        task = Task(1, "Test description", completed=True)
        assert task.id == 1
        assert task.description == "Test description"
        assert task.completed is True

    def test_task_creation_invalid_id_negative(self):
        """Test creating a Task with negative ID."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(-1, "Test description")

    def test_task_creation_invalid_id_zero(self):
        """Test creating a Task with zero ID."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(0, "Test description")

    def test_task_creation_invalid_description_empty(self):
        """Test creating a Task with empty description."""
        with pytest.raises(ValueError, match="Task description must be a non-empty string"):
            Task(1, "")

    def test_task_creation_invalid_description_whitespace_only(self):
        """Test creating a Task with whitespace-only description."""
        with pytest.raises(ValueError, match="Task description must be a non-empty string"):
            Task(1, "   ")

    def test_task_creation_invalid_description_none(self):
        """Test creating a Task with None description."""
        with pytest.raises(ValueError, match="Task description must be a non-empty string"):
            Task(1, None)

    def test_task_repr(self):
        """Test the string representation of a Task."""
        task = Task(1, "Test description", completed=True)
        expected = "[✓] 1. Test description"
        assert repr(task) == expected

        task_incomplete = Task(2, "Incomplete task", completed=False)
        expected_incomplete = "[○] 2. Incomplete task"
        assert repr(task_incomplete) == expected_incomplete

    def test_task_to_dict(self):
        """Test converting Task to dictionary."""
        task = Task(1, "Test description", completed=True)
        expected_dict = {
            "id": 1,
            "description": "Test description",
            "completed": True
        }
        assert task.to_dict() == expected_dict


class TestTodoApp:
    """Test the TodoApp class functionality."""

    def setup_method(self):
        """Set up a fresh TodoApp instance for each test."""
        self.app = TodoApp()

    def test_initial_state(self):
        """Test initial state of TodoApp."""
        assert len(self.app.tasks) == 0
        assert self.app.next_id == 1

    def test_validate_description_valid(self):
        """Test valid description validation."""
        assert self.app._validate_description("Valid description") is True

    def test_validate_description_empty(self):
        """Test empty description validation."""
        assert self.app._validate_description("") is False

    def test_validate_description_whitespace_only(self):
        """Test whitespace-only description validation."""
        assert self.app._validate_description("   ") is False

    def test_validate_description_none(self):
        """Test None description validation."""
        assert self.app._validate_description(None) is False

    def test_get_task_by_id_found(self):
        """Test getting a task by ID that exists."""
        task = self.app.add_task("Test task")
        found_task = self.app._get_task_by_id(task.id)
        assert found_task is not None
        assert found_task.id == task.id
        assert found_task.description == task.description

    def test_get_task_by_id_not_found(self):
        """Test getting a task by ID that doesn't exist."""
        result = self.app._get_task_by_id(999)
        assert result is None

    def test_add_task_success(self):
        """Test adding a task successfully."""
        task = self.app.add_task("New task")
        assert len(self.app.tasks) == 1
        assert task.id == 1
        assert task.description == "New task"
        assert task.completed is False
        assert self.app.next_id == 2

    def test_add_task_empty_description(self):
        """Test adding a task with empty description."""
        with pytest.raises(ValueError, match="Task description must be a non-empty string"):
            self.app.add_task("")

    def test_add_task_whitespace_description(self):
        """Test adding a task with whitespace-only description."""
        with pytest.raises(ValueError, match="Task description must be a non-empty string"):
            self.app.add_task("   ")

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when list is empty."""
        tasks = self.app.get_all_tasks()
        assert len(tasks) == 0

    def test_get_all_tasks_with_content(self):
        """Test getting all tasks when list has content."""
        task1 = self.app.add_task("Task 1")
        task2 = self.app.add_task("Task 2")
        tasks = self.app.get_all_tasks()
        assert len(tasks) == 2
        assert task1 in tasks
        assert task2 in tasks

    def test_update_task_success(self):
        """Test updating a task successfully."""
        task = self.app.add_task("Original task")
        result = self.app.update_task(task.id, "Updated task")
        assert result is True
        assert len(self.app.tasks) == 1
        assert self.app.tasks[0].description == "Updated task"

    def test_update_task_not_found(self):
        """Test updating a task that doesn't exist."""
        result = self.app.update_task(999, "Updated task")
        assert result is False

    def test_update_task_empty_description(self):
        """Test updating a task with empty description."""
        task = self.app.add_task("Original task")
        with pytest.raises(ValueError, match="Task description must be a non-empty string"):
            self.app.update_task(task.id, "")

    def test_update_task_whitespace_description(self):
        """Test updating a task with whitespace-only description."""
        task = self.app.add_task("Original task")
        with pytest.raises(ValueError, match="Task description must be a non-empty string"):
            self.app.update_task(task.id, "   ")

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        task = self.app.add_task("Task to delete")
        initial_count = len(self.app.tasks)
        result = self.app.delete_task(task.id)
        assert result is True
        assert len(self.app.tasks) == initial_count - 1

    def test_delete_task_not_found(self):
        """Test deleting a task that doesn't exist."""
        result = self.app.delete_task(999)
        assert result is False

    def test_mark_task_complete_success(self):
        """Test marking a task as complete."""
        task = self.app.add_task("Test task")
        assert task.completed is False
        result = self.app.mark_task_complete(task.id)
        assert result is True
        assert task.completed is True

    def test_mark_task_complete_not_found(self):
        """Test marking a task as complete when it doesn't exist."""
        result = self.app.mark_task_complete(999)
        assert result is False

    def test_mark_task_incomplete_success(self):
        """Test marking a task as incomplete."""
        task = self.app.add_task("Test task")
        task.completed = True  # Mark as complete first
        assert task.completed is True
        result = self.app.mark_task_incomplete(task.id)
        assert result is True
        assert task.completed is False

    def test_mark_task_incomplete_not_found(self):
        """Test marking a task as incomplete when it doesn't exist."""
        result = self.app.mark_task_incomplete(999)
        assert result is False


class TestTodoAppIntegration:
    """Test integration scenarios for the TodoApp."""

    def setup_method(self):
        """Set up a fresh TodoApp instance for each test."""
        self.app = TodoApp()

    def test_full_workflow(self):
        """Test a full workflow of adding, viewing, updating, marking, and deleting tasks."""
        # Add multiple tasks
        task1 = self.app.add_task("First task")
        task2 = self.app.add_task("Second task")
        task3 = self.app.add_task("Third task")

        # Verify all tasks exist
        all_tasks = self.app.get_all_tasks()
        assert len(all_tasks) == 3

        # Update one task
        result = self.app.update_task(task2.id, "Updated second task")
        assert result is True
        assert self.app._get_task_by_id(task2.id).description == "Updated second task"

        # Mark a task as complete
        result = self.app.mark_task_complete(task1.id)
        assert result is True
        assert self.app._get_task_by_id(task1.id).completed is True

        # Delete a task
        result = self.app.delete_task(task3.id)
        assert result is True
        assert self.app._get_task_by_id(task3.id) is None

        # Verify final state
        remaining_tasks = self.app.get_all_tasks()
        assert len(remaining_tasks) == 2
        for task in remaining_tasks:
            assert task.id in [task1.id, task2.id]

    def test_error_scenarios(self):
        """Test various error scenarios as specified in the specification."""
        # Test adding empty task
        with pytest.raises(ValueError):
            self.app.add_task("")

        # Add a valid task
        task = self.app.add_task("Valid task")

        # Test updating with empty description
        with pytest.raises(ValueError):
            self.app.update_task(task.id, "")

        # Test operations on non-existent task
        assert self.app.delete_task(999) is False
        assert self.app.update_task(999, "New description") is False
        assert self.app.mark_task_complete(999) is False
        assert self.app.mark_task_incomplete(999) is False