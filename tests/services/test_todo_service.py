import pytest
from  flask_server.services.todo_service import TodoList
from flask_server.db import db
from flask_server.models.todo_model import TodoModel
from flask_server.models.list_model import ListModel
from flask_server.app import app



@pytest.fixture(name = 'todos', scope = 'function')
def seed_todolist():
    with app.app_context():
        db.create_all()
        test_list = ListModel(name = 'test_list')
        db.session.add(test_list)
        db.session.commit()

        seed_todos = [
            TodoModel(name = "test_service1", description = "test", is_done = False, list_id = test_list.id),
            TodoModel(name = "test_service2", description = "test", is_done = False, list_id = test_list.id),
            TodoModel(name = "test_service3", description = "test", is_done = False, list_id = test_list.id)
        ]
        db.session.bulk_save_objects(seed_todos)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

@pytest.fixture(name = 'todo_test', scope = 'function')
def todoList():
    return TodoList()

@pytest.fixture(name = "list_ids", scope = 'function')
def get_list_ids(todos):
    
    ids = [todo_list.id for todo_list in ListModel.query.all()]
    return ids

@pytest.fixture(name = "todo_ids", scope = 'function')
def get_todo_ids(todos, list_ids):
    
    ids = [todo.id for todo in TodoModel.query.filter_by(list_id=list_ids[0]).all()]
    return ids


def test_add(todos, todo_test, list_ids):
    todo_test.add(list_ids[0], "test_add", "add")
    assert len(TodoModel.query.filter_by(list_id=list_ids[0]).all()) == 4

def test_remove(todos, todo_test, todo_ids, list_ids):
    todo_test.remove(list_ids[0], todo_ids[0])
    assert len(TodoModel.query.filter_by(list_id=list_ids[0]).all()) == 2

def test_edit(todos, todo_test, todo_ids, list_ids):
    todo = TodoModel.query.filter_by(list_id=list_ids[0], id=todo_ids[0]).first()
    assert todo.name == 'test_service1'
    todo_test.edit(list_ids[0], todo_ids[0],"test_edit")
    assert todo.name == "test_edit"

def test_update_status(todos, todo_test, todo_ids, list_ids):
    todo = TodoModel.query.filter_by(list_id=list_ids[0], id=todo_ids[1]).first()
    assert todo.is_done == False
    todo_test.update_status(list_ids[0], todo_ids[1], True)
    assert todo.is_done == True

def test_get_todos(todos, todo_test, todo_ids, list_ids):
    todo_test.update_status(list_ids[0], todo_ids[0], True)
    assert len(todo_test.get_todos(list_ids[0], "all")["Todos"]) == 3
    assert len(todo_test.get_todos(list_ids[0], "done")["Todos"]) == 1
    assert len(todo_test.get_todos(list_ids[0], "open")["Todos"]) == 2
    

def test_get_todo_by_id(todos, todo_test, todo_ids, list_ids):
    todo_item = todo_test.get_todo_by_id(list_ids[0], todo_ids[0])
    assert todo_item["List name"] == "test_list"
    assert todo_item["Todo"] == "test_service1"
    assert todo_item["Description"] == "test"
    assert todo_item["Completed"] == 'not completed'

