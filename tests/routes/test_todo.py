import pytest
from flask_server.app import app
from flask_server.routes.todo import todos
from flask_server.app import app
from flask_server.db import db
from flask_server.models.todo_model import TodoModel
from flask_server.models.list_model import ListModel



@pytest.fixture(name="todos", scope = "function")
def seed_todolist():
    with app.app_context():
        db.create_all()
        test_list = ListModel(name = 'test_list')
        db.session.add(test_list)
        db.session.commit()
        print(test_list.id)
        seed_todos = [
            TodoModel(name = "test_route1", description = "test", is_done = False, list_id = test_list.id),
            TodoModel(name = "test_route2", description = "test", is_done = False, list_id = test_list.id),
            TodoModel(name = "test_route3", description = "test", is_done = False, list_id = test_list.id)
        ]
        db.session.bulk_save_objects(seed_todos)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

@pytest.fixture(name = 'c', scope = 'function')    
def client(todos):
    return app.test_client()

@pytest.fixture(name = "list_ids", scope = 'function')
def get_list_ids(todos):
    ids = [todoList.id for todoList in ListModel.query.all()]
    return ids

@pytest.fixture(name = "ids", scope = 'function')
def get_todo_ids(todos, list_ids):
    
    ids = [todo.id for todo in TodoModel.query.filter_by(list_id=list_ids[0]).all()]
    return ids

def test_get_todo_by_id(c, ids, list_ids):
    response = c.get(f"/lists/{list_ids[0]}/{ids[0]}")
    data = response.get_json()
    assert data['List name'] == 'test_list'
    assert data['Todo'] == 'test_route1'
    assert data['Description'] == 'test'
    assert response.status_code == 200 or response.status_code == 404

def test_get_todos(c, list_ids):
    response = c.get(f"/lists/{list_ids[0]}?status=all")
    data = response.get_json()
    assert len(data['Todos']) == 3
    assert response.status_code == 200 or response.status_code == 404

def test_add_todo(c, list_ids):
    response = c.post(f'/lists/{list_ids[0]}', json = {'todo_item' : 'test_add', 'description' : 'test'})
    assert response.status_code == 201
    response = c.get(f"/lists/{list_ids[0]}?status=all")
    data = response.get_json()
    assert len(data['Todos']) == 4
    assert data['List name'] == 'test_list'
    assert data['Todos'][3]['Todo'] == 'test_add'
    assert data['Todos'][3]['Description'] == 'test'

def test_remove_todo(c, ids, list_ids):
    response = c.delete(f"/lists/{list_ids[0]}/{ids[0]}")
    assert response.status_code == 200
    response = c.get(f"/lists/{list_ids[0]}?status=all")
    data = response.get_json()
    assert len(data['Todos']) == 2
    assert ids[0] not in [todo['Id'] for todo in data['Todos']]

def test_edit_todo(c, ids, list_ids):
    response = c.patch(f"/lists/{list_ids[0]}/{ids[0]}/name", json = {'new_name' : 'test_edit'})
    assert response.status_code == 200
    response = c.get(f"/lists/{list_ids[0]}/{ids[0]}")
    data = response.get_json()
    assert data['Todo'] == 'test_edit' 

def test_update_status_todo(c, ids, list_ids):
    response = c.patch(f"/lists/{list_ids[0]}/{ids[0]}/status", json = {'status' : True})
    assert response.status_code == 200
    response = c.get(f"/lists/{list_ids[0]}/{ids[0]}")
    data = response.get_json()
    assert data['Completed'] == 'completed'
