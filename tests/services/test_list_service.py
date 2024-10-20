import pytest
from flask_server.services.list_service import List
from flask_server.models.list_model import ListModel
from flask_server.db import db
from flask_server.app import app

@pytest.fixture(name = 'lists', scope = 'function')
def seed_list():
    with app.app_context():
        db.create_all()
        seed_lists = [
            ListModel(name = "test1"),
            ListModel(name = "test2")
        ]
        db.session.bulk_save_objects(seed_lists)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

@pytest.fixture(name = 'list_test', scope = 'function')
def todoList():
    return List()

@pytest.fixture(name = "list_ids", scope = 'function')
def get_todo_ids(lists):
    
    ids = [list.list_id for list in ListModel.query.all()]
    return ids


def test_add(lists, list_test):
    list_test.add("test_add")
    list_len = ListModel.query.count()
    assert list_len == 3

def test_delete(lists, list_test, list_ids):
    list_test.delete(list_ids[0])
    list_len = ListModel.query.count()
    assert list_len == 1

def test_edit(lists, list_test, list_ids):
    list_test.edit(list_ids[0], "new_name")
    list_edited = db.session.get(ListModel, list_ids[0])
    assert list_edited.name == "new_name"

def test_get_all_lists(lists, list_test):
    assert len(list_test.get_all_lists()) == 2