import pytest
from flask_server.app import app
from flask_server.routes.todo import todos
from flask_server.app import app
from flask_server.db import db
from flask_server.models.todo_model import TodoModel
from flask_server.models.list_model import ListModel
from flask_server.models.user_list_model import UserListAssociationModel
from unittest.mock import patch, MagicMock



@pytest.fixture(name="todos", scope = "function")
def seed_todolist():
    with app.app_context():
        db.create_all()
        list1 = ListModel(name = "test1")
        association1 = UserListAssociationModel(user_id='Y2xpbWF0ZXdpdGhpbnRvb2toZWFkZWRmaWxsbXlzZWxmZm9ybWNvbW11bml0eWNhcGk=', list_id=list1.id, permission='admin')
        
        db.session.bulk_save_objects([list1, association1])
        db.session.commit()
        seed_todos = [
            TodoModel(name = "test_service1", description = "test", is_done = False, list_id = list1.id),
            TodoModel(name = "test_service2", description = "test", is_done = False, list_id = list1.id),
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

@pytest.fixture(name = "user_id_none", autouse=True)
def mock_get_user_none():
    with patch("flask_server.routes.todo.get_user", return_value=None) as mock:
        yield mock

@pytest.fixture(name = "user_id")
def mock_get_user_valid():
    with patch("flask_server.routes.todo.get_user", return_value={"user_id": "Y2xpbWF0ZXdpdGhpbnRvb2toZWFkZWRmaWxsbXlzZWxmZm9ybWNvbW11bml0eWNhcGk="}) as mock:
        yield mock

@pytest.fixture(name = "todo_service")
def mock_todo_services():
    with patch("flask_server.routes.todo.todos") as mock:
        mock.add.return_value = True
        mock.remove.return_value = True
        mock.delete.return_value = True
        mock.edit.return_value = True
        mock.update_status.return_value = True
        mock.get_todos.return_value = True
        mock.get_todo_by_id.return_value = True
        yield mock


def test_get_todo_by_id_no_user(c,user_id_none, ids, list_ids):
    response = c.get(f"/lists/{list_ids[0]}/{ids[0]}")
    assert response.status_code == 401

def test_get_todo_by_id_no_list(c,user_id, ids):
    response = c.get(f"/lists/jdjkl/{ids[0]}")
    assert response.status_code == 404

def test_get_todo_by_id_no_item(c,user_id, list_ids):
    response = c.get(f"/lists/{list_ids[0]}/hjlj")
    assert response.status_code == 404

def test_get_todo_by_id_no_user(c,todo_service, user_id, ids, list_ids):
    response = c.get(f"/lists/{list_ids[0]}/{ids[0]}")
    todo_service.get_todo_by_id.assert_called_once()
    assert response.status_code == 200



def test_get_todos_no_user(c, user_id_none, list_ids):
    response = c.get(f"/lists/{list_ids[0]}?status=all")
    assert response.status_code == 401

def test_get_todos_no_list(c, user_id):
    response = c.get(f"/lists/sjfl?status=all")
    assert response.status_code == 404

def test_get_todos_no_status(c, user_id, list_ids):
    response = c.get(f"/lists/{list_ids[0]}?status=")
    assert response.status_code == 404

def test_get_todos(c,todo_service, user_id, list_ids):
    response = c.get(f"/lists/{list_ids[0]}?status=all")
    todo_service.get_todos.assert_called_once()
    assert response.status_code == 200


def test_add_todo_no_user(c, user_id_none, list_ids):
    response = c.post(f'/lists/{list_ids[0]}', json = {'todo_item' : 'test_add', 'description' : 'test'})
    assert response.status_code == 401

def test_add_todo_no_list(c, user_id):
    response = c.post(f'/lists/dljsl', json = {'todo_item' : 'test_add', 'description' : 'test'})
    assert response.status_code == 404
    
def test_add_todo_data(c, user_id, list_ids):
    response = c.post(f'/lists/{list_ids[0]}', json = {})
    assert response.status_code == 400

def test_add_todo(c, user_id, list_ids, todo_service):
    response = c.post(f'/lists/{list_ids[0]}', json = {'todo_item' : 'test_add', 'description' : 'test'})
    todo_service.add.assert_called_once()
    assert response.status_code == 201

def test_remove_todo_no_user(c, ids, list_ids, user_id_none):
    response = c.delete(f"/lists/{list_ids[0]}/{ids[0]}")
    assert response.status_code == 401

def test_remove_todo_no_list(c, ids, user_id):
    response = c.delete(f"/lists/ksedl/{ids[0]}")
    assert response.status_code == 404
    
def test_remove_todo_no_item(c, list_ids, user_id):
    response = c.delete(f"/lists/{list_ids[0]}/dgd")
    assert response.status_code == 404

def test_remove_todo(c, ids, list_ids, user_id, todo_service):
    response = c.delete(f"/lists/{list_ids[0]}/{ids[0]}")
    todo_service.remove.assert_called_once()
    assert response.status_code == 200

def test_edit_todo_no_user(c, ids, list_ids, user_id_none):
    response = c.patch(f"/lists/{list_ids[0]}/{ids[0]}/name", json = {'new_name' : 'test_edit'})
    assert response.status_code == 401
    
def test_edit_todo_no_list(c, ids, user_id):
    response = c.patch(f"/lists/fgdg/{ids[0]}/name", json = {'new_name' : 'test_edit'})
    assert response.status_code == 404

def test_edit_todo_no_item(c, list_ids, user_id):
    response = c.patch(f"/lists/{list_ids[0]}/dsff/name", json = {'new_name' : 'test_edit'})
    assert response.status_code == 404

def test_edit_todo_no_data(c, ids, list_ids, user_id):
    response = c.patch(f"/lists/{list_ids[0]}/{ids[0]}/name", json = {})
    assert response.status_code == 400

def test_edit_todo(c, ids, list_ids, user_id, todo_service):
    response = c.patch(f"/lists/{list_ids[0]}/{ids[0]}/name", json = {'new_name' : 'test_edit'})
    todo_service.edit.assert_called_once()
    assert response.status_code == 200
    
def test_update_status_todo_no_user(c, ids, list_ids, user_id_none):
    response = c.patch(f"/lists/{list_ids[0]}/{ids[0]}/status", json = {'status' : True})
    assert response.status_code == 401
    
def test_update_status_todo_no_list(c, ids, user_id):
    response = c.patch(f"/lists/sjgf/{ids[0]}/status", json = {'status' : True})
    assert response.status_code == 404
    
def test_update_status_todo_no_item(c, list_ids, user_id):
    response = c.patch(f"/lists/{list_ids[0]}/dkjsl/status", json = {'status' : True})
    assert response.status_code == 404

def test_update_status_todo_no_status(c, ids, list_ids, user_id):
    response = c.patch(f"/lists/{list_ids[0]}/{ids[0]}/status", json = {})
    assert response.status_code == 400

def test_update_status_todo(c, ids, list_ids, user_id, todo_service):
    response = c.patch(f"/lists/{list_ids[0]}/{ids[0]}/status", json = {'status' : True})
    todo_service.update_status.assert_called_once()
    assert response.status_code == 200