from flask import Blueprint, jsonify,request
from  ..services.list_service import List

list_bp = Blueprint("list", __name__)

lists = List()

@list_bp.route("", methods=["POST"])
def add_list():
    data = request.json
    if "list_name" not in data:
        return jsonify({ "error": "Bad request. JSON body needs 'list_name'" }), 400
    
    was_added = lists.add(data['list_name'])
    if not was_added:
        return 404
    
    return "Added list", 201

@list_bp.route("/<list_id>", methods=["DELETE"])
def delete_list(list_id):
    was_deleted = lists.delete(list_id)

    if not was_deleted:
        return jsonify({"error" : "list_id doesn't exist"}), 404
    
    return "deleted list", 200

@list_bp.route("/<list_id>", methods=["PATCH"])
def edit_list(list_id):
    data = request.json
    if 'new_name' not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'new_name'"}), 400
    
    was_edited = lists.edit(list_id, data["new_name"])

    if not was_edited:
        return jsonify({"error" : "list_id doesn't exist"}), 404
    
    return "new name updated", 200


@list_bp.route("", methods=["GET"])
def get_lists():
    got_all_lists = lists.get_all_lists()
    if not got_all_lists:
        return jsonify({'error' : 'there is no list'}), 404
    
    return got_all_lists, 200