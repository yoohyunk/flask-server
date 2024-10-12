import pytest
from flask_server.app import app
from flask_server.services.todolist_service import TodoList



@pytest.fixture(name="c")
def client():
    with app.test_client() as c:
        yield c



# def test_get_todo_by_id(c):
#     response = client.get("/todos/getTodosById?id=da0d2822-568f-45b3-be29-00e76fc616e0")
#     assert response.status_code == 200 or response.status_code == 404
