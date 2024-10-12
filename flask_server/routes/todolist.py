from flask import Blueprint, jsonify


todolist_bp = Blueprint("todolist", __name__)


@todolist_bp.route("/get-todos", methods=["GET"])
def get_all_todos():
    return jsonify({"todos": []})
