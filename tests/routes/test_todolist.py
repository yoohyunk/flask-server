import pytest
from flask_server.app import app
from flask_server.routes.todolist import todos


@pytest.fixture(name="c")
def client():
    # mock todos_service data
    todos.todos = []
    todos.add('cleaning', 'at 1pm')
    todos.add('dishes', 'at 2pm')
    todos.add('laundry', 'at 3pm')

    with app.test_client() as c:
        yield c

@pytest.fixture(name = 'ids')
def todo_ids():
    ids = [todo['todo_id'] for todo in todos.todos]
    return ids

def test_get_todo_by_id(c, ids):
    response = c.get(f"/todos/getTodosById?id={ids[0]}")
    data = response.get_json()
    assert data['name'] == 'cleaning'
    assert data['description'] == 'at 1pm'
    assert response.status_code == 200 or response.status_code == 404

def test_get_todos(c):
    response = c.get(f"/todos/getTodos?status=all")
    data = response.get_json()
    assert len(data) == 3
    assert response.status_code == 200 or response.status_code == 404

def test_add_todo(c):
    response = c.post('/todos/addTodo', json = {'todo_item' : 'test_add', 'description' : 'test'})
    assert response.status_code == 201
    response = c.get(f"/todos/getTodos?status=all")
    data = response.get_json()
    assert len(data) == 4
    assert data[3]['name'] == 'test_add'
    assert data[3]['description'] == 'test'

def test_remove_todo(c, ids):
    response = c.delete("/todos/removeTodo", json = {'todo_id' : ids[0]})
    assert response.status_code == 200
    response = c.get(f"/todos/getTodos?status=all")
    data = response.get_json()
    assert len(data) == 2
    assert ids[0] not in [todo['todo_id'] for todo in data]

def test_edit_todo(c, ids):
    response = c.patch("/todos/editTodo", json = {'todo_id' : ids[1], 'new_name' : 'test_edit'})
    assert response.status_code == 200
    response = c.get(f"/todos/getTodosById?id={ids[1]}")
    data = response.get_json()
    assert data['name'] == 'test_edit' 

def test_update_status_todo(c, ids):
    response = c.patch("/todos/updateStatusTodo", json = {'todo_id' : ids[0], 'status' : True})
    assert response.status_code == 200
    response = c.get(f"/todos/getTodosById?id={ids[0]}")
    data = response.get_json()
    assert data['is_done'] == True
