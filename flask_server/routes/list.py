from flask import Blueprint, jsonify,request
from flask_server.services.list_service import ListService
from flask_server.utils.get_user import get_user

list_bp = Blueprint("list", __name__)

lists = ListService()

@list_bp.route("/", methods=["POST"])
def add_list():
    data = request.json
    jwtoken = request.headers.get("Authorization")
    user = get_user(jwtoken)
    
    if user is None:
        return jsonify({'error' : 'user not found'}), 401

    if "list_name" not in data:
        return jsonify({ "error": "Bad request. JSON body needs 'list_name'" }), 400
    
    was_added = lists.add(user['user_id'], data['list_name'])
    if not was_added:
        return 404
    
    return "Added list", 201

@list_bp.route("/<list_id>", methods=["DELETE"])
def delete_list(list_id):
    user = get_user()
    if user is None:
        return jsonify({'error' : 'user not found'}), 401

    was_deleted = lists.delete(user['user_id'],list_id)

    if not was_deleted:
        return jsonify({"error" : "list_id doesn't exist"}), 404
    
    return "deleted list", 200

@list_bp.route("/<list_id>", methods=["PATCH"])
def edit_list(list_id):
    data = request.json
    user = get_user()
    if user is None:
        return jsonify({'error' : 'user not found'}), 401

    if 'new_name' not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'new_name'"}), 400
    
    was_edited = lists.edit(user['user_id'], list_id, data["new_name"])

    if not was_edited:
        return jsonify({"error" : "list_id doesn't exist"}), 404
    
    return "new name updated", 200


@list_bp.route("/", methods=["GET"])
def get_lists():
    user = get_user()
    if user is None:
        return jsonify({'error' : 'user not found'}), 401

    got_all_lists = lists.get_all_lists(user['user_id'])
    if not got_all_lists:
        return jsonify({'error' : 'there is no list'}), 404
    
    return jsonify(got_all_lists), 200