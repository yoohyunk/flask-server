import pytest
from flask_server.services.list_service import ListService
from flask_server.models.list_model import ListModel
from flask_server.models.user_list_model import UserListAssociationModel
from flask_server.db import db
from flask_server.app import app

@pytest.fixture(name = 'lists', scope = 'function')
def seed_list():
    with app.app_context():
        db.create_all()
        
        list1 = ListModel(name = "test1")
        list2 = ListModel(name = "test2")
        association1 = UserListAssociationModel(user_id='Y2xpbWF0ZXdpdGhpbnRvb2toZWFkZWRmaWxsbXlzZWxmZm9ybWNvbW11bml0eWNhcGk=', list_id=list1.id, permission='admin')
        association2 = UserListAssociationModel(user_id='ZGFtYWdlYXNpZGVrbmlmZXJvcGVoaWRlcm9zZXJvcGVvYnRhaW5maWd1cmV0b25ndWU=', list_id=list2.id, permission='collaborator')
        
        db.session.bulk_save_objects([list1, list2, association1, association2])
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

@pytest.fixture(name = 'list_service', scope = 'function')
def todoList():
    return ListService()

@pytest.fixture(name = "list_ids", scope = 'function')
def get_list_ids(lists):
    
    ids = [list.id for list in ListModel.query.all()]
    return ids


def test_add(lists, list_service):
    list_len_before = UserListAssociationModel.query.filter_by(user_id='ZGFtYWdlYXNpZGVrbmlmZXJvcGVoaWRlcm9zZXJvcGVvYnRhaW5maWd1cmV0b25ndWU=').count()
    assert list_len_before == 1

    list_service.add("ZGFtYWdlYXNpZGVrbmlmZXJvcGVoaWRlcm9zZXJvcGVvYnRhaW5maWd1cmV0b25ndWU=","test_add")
    list_len_after = UserListAssociationModel.query.filter_by(user_id='ZGFtYWdlYXNpZGVrbmlmZXJvcGVoaWRlcm9zZXJvcGVvYnRhaW5maWd1cmV0b25ndWU=').count()
    assert list_len_after == 2

def test_delete(lists, list_service, list_ids):
    list_len_before = UserListAssociationModel.query.filter_by(user_id='Y2xpbWF0ZXdpdGhpbnRvb2toZWFkZWRmaWxsbXlzZWxmZm9ybWNvbW11bml0eWNhcGk=').count()
    assert list_len_before == 1
    list_service.delete('Y2xpbWF0ZXdpdGhpbnRvb2toZWFkZWRmaWxsbXlzZWxmZm9ybWNvbW11bml0eWNhcGk=', list_ids[0])
    list_len_after = UserListAssociationModel.query.filter_by(user_id='Y2xpbWF0ZXdpdGhpbnRvb2toZWFkZWRmaWxsbXlzZWxmZm9ybWNvbW11bml0eWNhcGk=').first()
    assert list_len_after is None

def test_edit(lists, list_service, list_ids):
    list_service.edit('Y2xpbWF0ZXdpdGhpbnRvb2toZWFkZWRmaWxsbXlzZWxmZm9ybWNvbW11bml0eWNhcGk=',list_ids[0], "new_name")
    list_edited = db.session.get(ListModel, list_ids[0])
    assert list_edited.name == "new_name"

def test_get_all_lists(lists, list_service):
    assert len(list_service.get_all_lists('Y2xpbWF0ZXdpdGhpbnRvb2toZWFkZWRmaWxsbXlzZWxmZm9ybWNvbW11bml0eWNhcGk=')) == 1