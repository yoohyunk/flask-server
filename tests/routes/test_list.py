import pytest
from flask_server.app import app
from flask_server.app import app
from flask_server.db import db
from flask_server.models.list_model import ListModel
from flask_server.models.user_list_model import UserListAssociationModel
from unittest.mock import patch, MagicMock

@pytest.fixture(name="lists", scope = "function")
def seed_todolist():
    with app.app_context():
        db.create_all()
        list1 = ListModel(name = "test1")
        association1 = UserListAssociationModel(user_id='Y2xpbWF0ZXdpdGhpbnRvb2toZWFkZWRmaWxsbXlzZWxmZm9ybWNvbW11bml0eWNhcGk=', list_id=list1.id, permission='admin')
        
        db.session.bulk_save_objects([list1, association1])
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

@pytest.fixture(name = 'c', scope = 'function')    
def client(lists):
    return app.test_client()

@pytest.fixture(name = "list_ids", scope = 'function')
def get_list_ids(lists):
    ids = [todoList.id for todoList in ListModel.query.all()]
    return ids

@pytest.fixture(name = "user_id_none", autouse=True)
def mock_get_user_none():
    with patch("flask_server.routes.list.get_user", return_value=None) as mock:
        yield mock

@pytest.fixture(name = "user_id")
def mock_get_user_valid():
    with patch("flask_server.routes.list.get_user", return_value={"user_id": "Y2xpbWF0ZXdpdGhpbnRvb2toZWFkZWRmaWxsbXlzZWxmZm9ybWNvbW11bml0eWNhcGk="}) as mock:
        yield mock

@pytest.fixture(name = "list_service")
def mock_list_services():
    with patch("flask_server.routes.list.lists") as mock:
        mock.add.return_value = True
        mock.remove.return_value = True
        mock.delete.return_value = True
        mock.edit.return_value = True
        mock.get_all_lists.return_value = True
        yield mock

def test_add_list_no_id(c, user_id_none):
    response = c.post(f'/lists/', json = {'list_name' : 'test_add'})
    assert response.status_code == 401

def test_add_list_no_list_name(c, user_id):
    response = c.post(f'/lists/', json = {})
    assert response.status_code == 400

def test_add_list(c, user_id, list_service):
    response = c.post(f'/lists/', json = {'list_name' : 'test_add'})
    list_service.add.assert_called_once()
    assert response.status_code == 201

def test_delete_list_no_user(c, user_id_none, list_ids):
    response = c.delete(f'/lists/{list_ids[0]}')
    assert response.status_code == 401

def test_delete_list_no_list(c, user_id, list_ids):
    response = c.delete(f'/lists/n')
    assert response.status_code == 404

def test_delete_list(c, user_id, list_service, list_ids):
    response = c.delete(f'/lists/{list_ids[0]}')
    list_service.delete.assert_called_once()
    assert response.status_code == 200


def test_edit_todo_no_user(c,  user_id_none, list_ids):
    response = c.patch(f"/lists/{list_ids[0]}", json = {'new_name' : 'test_edit'})
    assert response.status_code == 401

def test_edit_todo_no_list(c,  user_id, list_ids):
    response = c.patch(f"/lists/n", json = {'new_name' : 'test_edit'})
    assert response.status_code == 404

def test_edit_todo_no_new_name(c,  user_id, list_ids):
    response = c.patch(f"/lists/{list_ids[0]}", json = {})
    assert response.status_code == 400

def test_edit_todo_no_new_name(c, list_service, user_id, list_ids):
    response = c.patch(f"/lists/{list_ids[0]}", json = {'new_name' : 'test_edit'})
    list_service.edit.assert_called_once()
    assert response.status_code == 200
   
def test_get_lists_no_user(c, user_id_none):
    response = c.get('/lists/')
    assert response.status_code == 401
   
def test_get_lists(c, user_id, list_service):
    response = c.get('/lists/')
    list_service.get_all_lists.assert_called_once()
    assert response.status_code == 200