import pytest
from flask_server.app import app
from flask_server.app import app
from flask_server.db import db
from flask_server.models.user_model import UserModel

@pytest.fixture(name="users", scope = "function")
def seed_user():
    with app.app_context():
        db.create_all()
        seed_users = [
            UserModel(name = "test_route1"),
            UserModel(name = "test_route2"),
            UserModel(name = "test_route3")
        ]
        db.session.bulk_save_objects(seed_users)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()


@pytest.fixture(name = 'c', scope = 'function')    
def client(users):
    return app.test_client()

@pytest.fixture(name = "user_ids", scope = 'function')
def get_list_ids(users):
    ids = [user.id for user in UserModel.query.all()]
    return ids


def test_add_user(c):
    response = c.post(f'/users/', json = {'user_name' : 'test_add'})
    assert response.status_code == 201
    assert len(UserModel.query.all()) == 4

def test_delete_user(c, user_ids):
    response = c.delete(f'/users/{user_ids[0]}')
    assert response.status_code == 200
    assert len(UserModel.query.all()) == 2
    assert db.session.get(UserModel, user_ids[0]) is None

def test_edit_user_name(c, user_ids):
    response = c.patch(f'/users/{user_ids[0]}', json = {'new_name' : 'test_edit'})
    assert response.status_code == 200
    assert db.session.get(UserModel, user_ids[0]).name == "test_edit"

def test_get_all_users(c):
    response = c.get('/users/')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 3