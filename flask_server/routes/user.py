from flask import Blueprint, jsonify,request
from  ..services.user_service import User

user_bp = Blueprint("user", __name__)

users = User()

@user_bp.route("/", methods=["POST"])
def add_user():
    data = request.json
    if "user_name" not in data:
        return jsonify({ "error": "Bad request. JSON body needs 'user_name'" }), 400
    
    was_added = users.add_user(data['user_name'])
    if not was_added:
        return 404
    
    return "Added list", 201

@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    was_deleted = users.delete_user(user_id)

    if not was_deleted:
        return jsonify({"error" : "user_id doesn't exist"}), 404
    
    return "deleted user", 200


@user_bp.route("/<user_id>", methods=["PATCH"])
def edit_user(user_id):
    data = request.json
    if 'new_name' not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'new_name'"}), 400
    
    was_edited = users.edit_user_name(user_id, data["new_name"])

    if not was_edited:
        return jsonify({"error" : "user_id doesn't exist"}), 404
    
    return "new name updated", 200

@user_bp.route("/", methods=["GET"])
def get_users():
    got_all_users = users.get_all_users()
    if not got_all_users:
        return jsonify({'error' : 'there is no user'}), 404
    
    return got_all_users, 200