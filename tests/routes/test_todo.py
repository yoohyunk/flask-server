import pytest
from flask_server.app import app
from flask_server.routes.todo import todos
from flask_server.app import app
from flask_server.db import db
from flask_server.models.todo_model import TodoModel



@pytest.fixture(name="todos", scope = "function")
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

@pytest.fixture(name = 'c', scope = 'function')    
def client(todos):
    return app.test_client()

@pytest.fixture(name = "ids", scope = 'function')
def get_todo_ids(todos):
    
    ids = [todo.id for todo in TodoModel.query.all()]
    return ids

def test_get_todo_by_id(c, ids):
    response = c.get(f"/todos/getTodosById?id={ids[0]}")
    data = response.get_json()
    assert data['Todo'] == 'test_service1'
    assert data['Description'] == 'test'
    assert response.status_code == 200 or response.status_code == 404

def test_get_todos(c):
    response = c.get(f"/todos/getTodos?status=all")
    data = response.get_json()
    assert len(data) == 3
    assert response.status_code == 200 or response.status_code == 404

def test_add_todo(c):
    response = c.post('/todos/addTodo', json = {'todo_item' : 'test_add', 'description' : 'test'})
    assert response.status_code == 201
    response = c.get(f"/todos/getTodos?status=all")
    data = response.get_json()
    assert len(data) == 4
    assert data[2]['Todo'] == 'test_service3'
    assert data[2]['Description'] == 'test'

def test_remove_todo(c, ids):
    response = c.delete("/todos/removeTodo", json = {'todo_id' : ids[0]})
    assert response.status_code == 200
    response = c.get(f"/todos/getTodos?status=all")
    data = response.get_json()
    assert len(data) == 2
    assert ids[0] not in [todo['Id'] for todo in data]

def test_edit_todo(c, ids):
    response = c.patch("/todos/editTodo", json = {'todo_id' : ids[1], 'new_name' : 'test_edit'})
    assert response.status_code == 200
    response = c.get(f"/todos/getTodosById?id={ids[1]}")
    data = response.get_json()
    assert data['Todo'] == 'test_edit' 

def test_update_status_todo(c, ids):
    response = c.patch("/todos/updateStatusTodo", json = {'todo_id' : ids[0], 'status' : True})
    assert response.status_code == 200
    response = c.get(f"/todos/getTodosById?id={ids[0]}")
    data = response.get_json()
    assert data['Completed'] == 'completed'
