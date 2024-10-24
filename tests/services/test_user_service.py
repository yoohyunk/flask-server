import pytest
from flask_server.services.user_service import User
from flask_server.models.user_model import UserModel
from flask_server.db import db
from flask_server.app import app

@pytest.fixture(name = 'users', scope = 'function')
def seed_user():
    with app.app_context():
        db.create_all()
        seed_users = [
            UserModel(name = "test_user1"),
            UserModel(name = "test_user2")
        ]
        db.session.bulk_save_objects(seed_users)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

@pytest.fixture(name = 'user_test', scope = 'function')
def todoList():
    return User()

@pytest.fixture(name = "user_ids", scope = 'function')
def get_todo_ids(users):
    
    ids = [user.id for user in UserModel.query.all()]
    return ids

def test_add_user(users, user_test):
    user_test.add_user('test_add_user')
    count_user = UserModel.query.count()
    assert count_user == 3

def test_delete_user(users, user_test, user_ids):
    user_test.delete_user(user_ids[0])
    count_user = UserModel.query.count()
    assert count_user == 1
    assert db.session.get(UserModel, user_ids[0]) is None

def test_edit_user_name(users, user_test, user_ids):
    user_test.edit_user_name(user_ids[0], "test_edit_user_name")
    user_edited = db.session.get(UserModel, user_ids[0])
    assert user_edited.name == "test_edit_user_name"

def test_get_all_users(users, user_test):
    assert len(user_test.get_all_users()) == 2
    