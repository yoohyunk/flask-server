import pytest
from flask_server.app import app
from flask_server.db import db
from flask_server.models.user_model import UserModel
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

@pytest.fixture(name = 'c', scope = 'function')    
def client(users):
    return app.test_client()


def test_signup(c, users):
    response = c.post(f'users/signup', json = {"email": "test_add", "password": "test"})
    assert response.status_code == 201
    assert 'jwt' in response.json

def test_signup_no_email(c, users):
    response = c.post(f'users/signup', json = {"password": "test"})
    assert response.status_code == 400

def test_signup_no_password(c, users):
    response = c.post(f'users/signup', json = {"email": "test_add"})
    assert response.status_code == 400

def test_signup_duplicate(c, users):
    response = c.post(f'users/signup', json = {"email": "test1", "password": "test"})
    assert response.status_code == 400

def test_login(c, users):
    response = c.post(f'users/login', json = {"email": "test1", "password": "test"})
    assert response.status_code == 200
    assert 'jwt' in response.json

def test_login_no_email(c, users):
    response = c.post(f'users/login', json = {"password": "test"})
    assert response.status_code == 400

def test_login_no_password(c, users):
    response = c.post(f'users/login', json = {"email": "test1"})
    assert response.status_code == 400

def test_login_invalid(c, users):
    response = c.post(f'users/login', json = {"email": "test1", "password": "tests"})
    assert response.status_code == 401