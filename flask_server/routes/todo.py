from flask import Blueprint, jsonify,request
from  ..services.todo_service import TodoList

todo_bp = Blueprint("todolist", __name__)


todos = TodoList()

@todo_bp.route("/<list_id>/<todo_id>", methods=["GET"])
def get_todo_by_id(list_id, todo_id):
    got_todo = todos.get_todo_by_id(list_id, todo_id)
    if not got_todo:
        return jsonify({"error" : "invalid id"})
    return got_todo

@todo_bp.route("/<list_id>", methods=["GET"])
def get_todos(list_id):
  status = request.args.get("status", "all")
  if status in ["open", "done", "all"]:
    return todos.get_todos(list_id, status)
  return jsonify({
    'message' : f"invalid list_id {list_id} or status {status}. status must be one of 'open', 'done', or 'all'",
    'error' : "invalid request"
  }), 400

@todo_bp.route("/<list_id>", methods=["POST"])
def add_todo(list_id):
    data = request.json

    if "todo_item" not in data or "description" not in data:
        return jsonify({ "error": "Bad request. JSON body needs 'todo_item' and 'description'" }), 400
   
    was_added = todos.add(list_id, data["todo_item"], data["description"])
    if not was_added:
        return jsonify({
            'error' : 'list id not found'
        }), 404
    
    return "Added todo", 201

    

@todo_bp.route("/<list_id>/<todo_id>", methods=["DELETE"])
def remove_todo(list_id, todo_id):
    was_deleted = todos.remove(list_id, todo_id)

    if not was_deleted:
        return jsonify({"error" : "list_id or todo_id doesn't exist"}), 404

    return "deleted todo", 200

@todo_bp.route("/<list_id>/<todo_id>/name", methods=["PATCH"])
def edit_todo(list_id, todo_id):
    data = request.json

    if "new_name" not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'new_name'"}), 400
    
    was_edited = todos.edit(list_id, todo_id, data["new_name"])

    if not was_edited:
        return jsonify({"error" : "list_id or todo_id doesn't exist"}), 404
    
    return "new name updated", 200

@todo_bp.route("/<list_id>/<todo_id>/status", methods=["PATCH"])
def update_status_todo(list_id, todo_id):
    data = request.json

    if "status" not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'list_id', 'todo_id' and 'status"}), 400
    
    was_updated = todos.update_status(list_id, todo_id, data["status"])

    if not was_updated:
        return jsonify({"error" : "list_id or todo_id doesn't exist"}), 404

    return "updated status", 200
