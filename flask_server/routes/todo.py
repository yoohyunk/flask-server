from flask import Blueprint, jsonify,request
from  ..services.todo_service import TodoList

todolist_bp = Blueprint("todolist", __name__)


todos = TodoList()

@todolist_bp.route("/todos/getTodosById", methods=["GET"])
def get_todo_by_id():
    list_id = request.args.get("list_id")
    id = request.args.get("id")
    got_todo = todos.get_todo_by_id(list_id, id)
    if not got_todo:
        return jsonify({"error" : "invalid id"})
    return got_todo

@todolist_bp.route("/todos/getTodos", methods=["GET"])
def get_todo():
  list_id = request.args.get("list_id")
  status = request.args.get("status", "all")
  if status in ["open", "done", "all"]:
    return todos.get_todos(list_id, status)
  return jsonify({
    'error': f"invalid list_id {list_id} or status {status}. status must be on of 'open', 'done', or 'all'",
    'message': "invalid request"
  }), 400

@todolist_bp.route("/todos/addTodo", methods=["POST"])
def add_todo():
    data = request.json

    if "list_id" not in data or "todo_item" not in data or "description" not in data:
        return jsonify({ "error": "Bad request. JSON body needs 'list_id', 'todo_item' and 'description'" }), 400
   
    todos.add(data["list_id"], data["todo_item"], data["description"])
    return "Added todo", 201

@todolist_bp.route("/todos/removeTodo", methods=["DELETE"])
def remove_todo():
    data = request.json

    if "list_id" not in data or "todo_id" not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'list_id' and 'todo_id'"}), 400
    
    was_deleted = todos.remove(data["list_id"], data["todo_id"])

    if not was_deleted:
        return jsonify({"error" : "list_id or todo_id doesn't exist"}), 404

    return "deleted todo", 200

@todolist_bp.route("/todos/editTodo", methods=["PATCH"])
def edit_todo():
    data = request.json

    if "list_id" not in data or "todo_id" not in data or "new_name" not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'list_id', 'todo_id' and 'new_name'"}), 400
    
    was_edited = todos.edit(data["list_id"], data["todo_id"], data["new_name"])

    if not was_edited:
        return jsonify({"error" : "list_id or todo_id doesn't exist"}), 404
    
    return "new name updated", 200

@todolist_bp.route("/todos/updateStatusTodo", methods=["PATCH"])
def update_status_todo():
    data = request.json

    if "list_id" not in data or "todo_id" not in data or "status" not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'list_id', 'todo_id' and 'status"}), 400
    
    was_updated = todos.update_status(data["list_id"], data["todo_id"], data["status"])

    if not was_updated:
        return jsonify({"error" : "list_id or todo_id doesn't exist"}), 404

    return "updated status", 200
