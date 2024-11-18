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
    
    was_added = lists.add(user, data['list_name'])
    if not was_added:
        return 404
    
    return jsonify(was_added), 201

@list_bp.route("/<list_id>", methods=["DELETE"])
def delete_list(list_id):
    jwtoken = request.headers.get("Authorization")
    user = get_user(jwtoken)
    if user is None:
        return jsonify({'error' : 'user not found'}), 401

    was_deleted = lists.delete(user,list_id)

    if not was_deleted:
        return jsonify({"error" : "list_id doesn't exist"}), 404
    
    return "deleted list", 200

@list_bp.route("/<list_id>", methods=["PATCH"])
def edit_list(list_id):
    data = request.json
    jwtoken = request.headers.get("Authorization")
    user = get_user(jwtoken)
    if user is None:
        return jsonify({'error' : 'user not found'}), 401

    if 'new_name' not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'new_name'"}), 400
    
    was_edited = lists.edit(user, list_id, data["new_name"])

    if not was_edited:
        return jsonify({"error" : "list_id doesn't exist"}), 404
    
    return "new name updated", 200


@list_bp.route("/", methods=["GET"])
def get_lists():
    jwtoken = request.headers.get("Authorization")
    user = get_user(jwtoken)
    if user is None:
        return jsonify({'error' : 'user not found'}), 401

    got_all_lists = lists.get_all_lists(user)
    if not got_all_lists:
        return jsonify({'error' : 'there is no list'}), 404
    
    return jsonify(got_all_lists), 200

@list_bp.route("/<list_id>/collaborator", methods=["POST"])
def add_collaborator(list_id):
    data = request.json
    jwtoken = request.headers.get("Authorization")
    user = get_user(jwtoken)
    if user is None:
        return jsonify({'error' : 'user not found'}), 401

    if "collaborator_id" not in data:
        return jsonify({ "error": "Bad request. JSON body needs 'collaborator_id'" }), 400
    
    was_added = lists.add_collaborator(user, data["collaborator_id"], list_id)
    print(data["collaborator_id"])
    if not was_added:
        return jsonify({"error" : "list_id or collaborator_id doesn't exist"}), 404
    
    return "Added collaborator", 201

@list_bp.route("/<list_id>/collaborator", methods=["GET"])
def get_collaborators(list_id):
    jwtoken = request.headers.get("Authorization")
    user = get_user(jwtoken)
    if user is None:
        return jsonify({'error' : 'user not found'}), 401

    got_collaborators = lists.get_all_collaborators(user, list_id)
    if not got_collaborators:
        return jsonify({'error' : 'there is no collaborator'}), 404
    print("this is", got_collaborators)
    
    return jsonify(got_collaborators), 200

@list_bp.route("/<list_id>/admin", methods=["GET"])
def get_admin(list_id):
    jwtoken = request.headers.get("Authorization")
    user = get_user(jwtoken)
    if user is None:
        return jsonify({'error' : 'user not found'}), 401

    got_admin = lists.get_admin(user, list_id)
    if not got_admin:
        return jsonify({'error' : 'there is no admin'}), 404
    print("this is", got_admin)
    
    return jsonify(got_admin), 200

@list_bp.route("/<list_id>/admin", methods=["POST"])
def add_admin(list_id):
    data = request.json
    jwtoken = request.headers.get("Authorization")
    user = get_user(jwtoken)
    if user is None:
        return jsonify({'error' : 'user not found'}), 401

    if "new_admin_id" not in data:
        return jsonify({ "error": "Bad request. JSON body needs 'new_admin_id'" }), 400
    
    was_added = lists.add_admin(data["new_admin_id"], user, list_id)
    print(data["new_admin_id"])
    if not was_added:
        return jsonify({"error" : "list_id or new_admin_id doesn't exist"}), 404
    
    return "Added admin", 201