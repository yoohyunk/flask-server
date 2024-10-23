from typing import List, Literal, Optional, TypedDict
import uuid
import random
from flask_server.models.todo_model import TodoModel
from flask_server.models.list_model import ListModel
from flask_server.db import db

random.seed(123)

# def random_uuid():
#     return uuid.UUID(bytes=bytes(random.getrandbits(8) for _ in range(16)), version=4)

class TodoItem(TypedDict):
    name: str
    description: str
    is_done: bool
    

# def create_todo_item(name: str, description: str) -> TodoItem:
#     new_todo = TodoItem(name, description, False)
#     return new_todo
    



class TodoList:
    def add(self, listId: str, todo: str, description: Optional[str] = "") -> None:
        
        list_exist = db.session.get(ListModel, listId)

        if list_exist:
            new_todo = TodoModel(
                list_id = listId,
                name = todo,
                description = description,
                is_done = False
            )

            db.session.add(new_todo)
            db.session.commit()

            return True
        
        return False

    def remove(self, listId: str, todo_id: str) -> None:
        # Remove a todo item
        todo_to_delete = TodoModel.query.filter_by(list_id = listId, id = todo_id).first()

        if todo_to_delete:
            db.session.delete(todo_to_delete)
            db.session.commit()
            return True
            
        return False

    def edit(self,listId: str, todo_id: str, new_name: str) -> None:
        todo_to_edit = TodoModel.query.filter_by(list_id = listId, id = todo_id).first()
        if todo_to_edit:
            todo_to_edit.name = new_name
            db.session.commit()
            return True
        return False

    def update_status(self,listId: str, todo_id: str, is_done: bool) -> None:
        todo_to_edit = TodoModel.query.filter_by(list_id = listId, id = todo_id).first()
        if todo_to_edit:
            todo_to_edit.is_done = is_done
            db.session.commit()
            return True
        return False

    def get_todos(self, listId: str, show_completed: Literal["open", "done", "all"]) -> dict:
        # Get all the todo items
        # can also filter by "open" = show all incomplete todos, "done" = show all completed todos, "all" = show all todos
        todoList = db.session.get(ListModel, listId)
        if not todoList:
            return False

        if show_completed == "all":
            todos = TodoModel.query.filter_by(list_id = listId).all()
            todo_list=[{
                "Id" : todo.id,
                "Todo" : todo.name,
                "Description" : todo.description,
                "completed" : "completed" if todo.is_done == 1 else "not completed" 
            } for todo in todos]
            return {
                "List name" : todoList.name,
                "List id" : todoList.id,
                "Todos" : todo_list
                }

        is_completed = True if show_completed == "done" else False
        todos = TodoModel.query.filter_by(list_id = listId, is_done=is_completed).all()
        todo_list=[{
            "Id" : todo.id,
            "Todo" : todo.name,
            "Description" : todo.description,
            "completed" : "completed" if todo.is_done == 1 else "not completed" 
        } for todo in todos]
        return {
            "List name" : todoList.name,
            "List id" : todoList.id,
            "Todos" : todo_list
            }

    def get_todo_by_id(self, listId: str, todo_id: str) -> dict:
        # Get a todo item by its id)
        todo_item = TodoModel.query.filter_by(list_id = listId, id = todo_id).first()
        todo_list = db.session.get(ListModel, listId)
        completed = "completed" if todo_item.is_done == 1 else "not completed"
        if todo_item:
            return {
                "List name" : todo_list.name,
                "List id" : todo_item.list_id,
                "Id" : todo_item.id,
                "Todo" : todo_item.name,
                "Description" : todo_item.description,
                "Completed" : completed
            }
        return False
    
