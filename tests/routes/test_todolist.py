import pytest
from flask_server.app import app


@pytest.fixture(name="c")
def client():
    with app.test_client() as c:
        yield c


def test_hello_world(c):
    response = c.get("/todolist/get-todos")
    assert response.status_code == 200
    assert response.json == {"todos": []}
