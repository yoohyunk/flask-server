from typing import List, Literal, Optional, TypedDict
import uuid
import random

random.seed(123)

def random_uuid():
    return uuid.UUID(bytes=bytes(random.getrandbits(8) for _ in range(16)), version=4)

class TodoItem(TypedDict):
    todo_id: str
    name: str
    description: str
    is_done: bool


def create_todo_item(name: str, description: str) -> TodoItem:
    todo_id = str(random_uuid())
    return {
        "todo_id": todo_id,
        "name": name,
        "description": description,
        "is_done": False,
        }



class TodoList:
    def __init__(self) -> None:
        self.todos: List[TodoItem] = []

    def add(self, todo: str, description: Optional[str] = "") -> None:
        # Create a new todo item
        new_item = TodoItem(create_todo_item(todo, description))
        self.todos.append(new_item)
        return True

    def remove(self, todo_id: str) -> None:
        # Remove a todo item
        for todo in self.todos:
            if todo["todo_id"] == todo_id:
                self.todos.remove(todo)
                return True
        return False

    def edit(self, todo_id: str, new_name: str) -> None:
        # Edit a todo item
        for i in self.todos:
            if i["todo_id"] == todo_id:
                i["name"] = new_name
                return True
        return False

    def update_status(self, todo_id: str, is_done: bool) -> None:
        # Update the status of a todo item
        for todo in self.todos:
            if todo["todo_id"] == todo_id:
                todo["is_done"] = is_done
                return True
        raise KeyError(f"Todo item with ID {todo_id} not found.")

    def get_todos(self, show_completed: Literal["open", "done", "all"]) -> dict:
        # Get all the todo items
        # can also filter by "open" = show all incomplete todos, "done" = show all completed todos, "all" = show all todos
        
        if show_completed == "all":
            return self.todos 

        is_completed = True if show_completed == "done" else False
        todo_list = [todo for todo in self.todos if todo["is_done"] == is_completed]
        return todo_list

    def get_todo_by_id(self, todo_id: str) -> dict:
        # Get a todo item by its id)
        for item in self.todos:
            if item["todo_id"] == todo_id:
                return item
        return False