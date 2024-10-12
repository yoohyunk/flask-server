import pytest
from  flask_server.services.todolist_service import TodoList



@pytest.fixture(name = 'todos')
def seed_todolist():
    test_todos = TodoList()
    test_todos.add("study", "9am - 10am")
    test_todos.add("running", "1pm")
    test_todos.add("yoga", "8am")
    test_todos.add("cleaning", "anytime before 10pm")
    return test_todos

@pytest.fixture(name = "todo_ids")
def get_todo_ids(todos):
    ids = [todo['todo_id'] for todo in todos.todos]
    return ids

def test_add(todos):
    todos.add("sleep", "at 11pm")
    assert len(todos.get_todos("all")) == 5

def test_remove(todos, todo_ids):
    todos.remove(todo_ids[0])
    assert len(todos.get_todos("all")) == 3

def test_edit(todos, todo_ids):
    assert todos.todos[1]['name'] == 'running'
    todos.edit(todo_ids[1],"jogging")
    test_item = todos.todos[1]
    assert test_item["name"] == "jogging"

def test_update_status(todos, todo_ids):
    assert todos.todos[0]["is_done"] == False
    todos.update_status(todo_ids[0], True)
    test_item = todos.todos[0]
    assert test_item["is_done"] == True

def test_get_todos(todos, todo_ids):
    todos.update_status(todo_ids[0], True)
    assert len(todos.get_todos("all")) == 4
    assert len(todos.get_todos("done")) == 1
    assert len(todos.get_todos("open")) == 3
    

def test_get_todo_by_id(todos, todo_ids):
    todo_item = todos.get_todo_by_id(todo_ids[0])
    assert todo_item["name"] == "study"
    assert todo_item["description"] == "9am - 10am"
    assert todo_item["is_done"] == False

