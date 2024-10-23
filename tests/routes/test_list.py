import pytest
from flask_server.app import app
from flask_server.app import app
from flask_server.db import db
from flask_server.models.list_model import ListModel

@pytest.fixture(name="lists", scope = "function")
def seed_todolist():
    with app.app_context():
        db.create_all()
        seed_todos = [
            ListModel(name = "test_route1"),
            ListModel(name = "test_route2"),
            ListModel(name = "test_route3")
        ]
        db.session.bulk_save_objects(seed_todos)
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


def test_add_list(c):
    response = c.post(f'/lists', json = {'list_name' : 'test_add'})
    assert response.status_code == 201
    assert len(ListModel.query.all()) == 4

def test_delete_list(c, list_ids):
    response = c.delete(f'/lists/{list_ids[0]}')
    assert response.status_code == 200
    assert len(ListModel.query.all()) == 2
    assert db.session.get(ListModel, list_ids[0]) is None

def test_edit_todo(c, list_ids):
    response = c.patch(f"/lists/{list_ids[0]}", json = {'new_name' : 'test_edit'})
    assert response.status_code == 200
    assert db.session.get(ListModel, list_ids[0]).name == 'test_edit'

def test_get_lists(c):
    response = c.get('/lists')
    assert response.status_code == 200
    assert len(ListModel.query.all()) == 3