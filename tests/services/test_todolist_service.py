import pytest
from  flask_server.services.todolist_service import TodoList
from flask_server.db import db
from flask_server.models.todo_model import TodoModel
from flask_server.app import app



@pytest.fixture(name = 'todos', scope = 'function')
def seed_todolist():
    with app.app_context():
        db.create_all()
        seed_todos = [
            TodoModel(name = "test_service1", description = "test", is_done = False),
            TodoModel(name = "test_service2", description = "test", is_done = False),
            TodoModel(name = "test_service3", description = "test", is_done = False)
        ]
        db.session.bulk_save_objects(seed_todos)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

@pytest.fixture(name = 'todo_test', scope = 'function')
def todoList():
    return TodoList()

@pytest.fixture(name = "todo_ids", scope = 'function')
def get_todo_ids(todos):
    
    ids = [todo.id for todo in TodoModel.query.all()]
    return ids

def test_add(todos, todo_test):
    todo_test.add("test_add", "add")
    assert len(todo_test.get_todos("all")) == 4

def test_remove(todos, todo_test, todo_ids):
    todo_test.remove(todo_ids[0])
    assert len(todo_test.get_todos("all")) == 2

def test_edit(todos, todo_test, todo_ids):
    todo = db.session.get(TodoModel, todo_ids[0])
    assert todo.name == 'test_service1'
    todo_test.edit(todo_ids[0],"test_edit")
    assert todo.name == "test_edit"

def test_update_status(todos, todo_test, todo_ids):
    todo = db.session.get(TodoModel, todo_ids[1])
    assert todo.is_done == False
    todo_test.update_status(todo_ids[1], True)
    assert todo.is_done == True

def test_get_todos(todos, todo_test, todo_ids):
    todo_test.update_status(todo_ids[0], True)
    assert len(todo_test.get_todos("all")) == 3
    assert len(todo_test.get_todos("done")) == 1
    assert len(todo_test.get_todos("open")) == 2
    

def test_get_todo_by_id(todos, todo_test, todo_ids):
    todo_item = todo_test.get_todo_by_id(todo_ids[0])
    assert todo_item["Todo"] == "test_service1"
    assert todo_item["Description"] == "test"
    assert todo_item["Completed"] == 'not completed'

