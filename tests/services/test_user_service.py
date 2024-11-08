import pytest
from flask_server.services.user_service import UserService
from flask_server.db import db
from flask_server.models.user_model import UserModel
from flask_server.app import app
from flask_server.utils.hash_user_password import hash_password


@pytest.fixture(name = 'users', scope = 'function')
def seed_user():
    with app.app_context():
        db.create_all()
        
        user1 = UserModel(email = "test1", password_hash = hash_password("test"))
        user2 = UserModel(email = "test2", password_hash = hash_password("test"))

        
        db.session.bulk_save_objects([user1, user2])
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

@pytest.fixture(name = 'user_service', scope = 'function')
def user():
    return UserService()


def test_add_user(users, user_service):
    user_len_before = UserModel.query.count()
    assert user_len_before == 2

    user_service.add_user("test_add", "test")
    user_len_after = UserModel.query.count()
    assert user_len_after == 3

def test_add_user_duplicate(users, user_service):
    user_len_before = UserModel.query.count()
    assert user_len_before == 2

    user_service.add_user("test1", "test")
    user_len_after = UserModel.query.count()
    assert user_len_after == 2  

def test_find_user(users, user_service):
    user = user_service.find_user("test1", "test")
    assert user is not False

def test_find_user_invalid(users, user_service):
    user = user_service.find_user("test1", "tests")
    assert user is False