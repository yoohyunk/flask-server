from flask_server.services.user_service import UserService
from flask import Blueprint, jsonify, request

from flask_server.utils.get_user import get_user

user_bp = Blueprint("user", __name__)

users = UserService()

@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if "email" not in data or "password" not in data:
        return jsonify({ "error": "Bad request. JSON body needs 'email' and 'password'" }), 400
    
    jwt_created = users.add_user(data["email"], data["password"])
    if not jwt_created:
        return jsonify({
            'error' : 'email already exists'
        }), 400
    
    return jsonify({
        "jwt" : jwt_created
        }), 201

@user_bp.route("/login", methods=["POST"])  
def signin():
    data = request.json
    if "email" not in data or "password" not in data:
        return jsonify({ "error": "Bad request. JSON body needs 'email' and 'password'" }), 400
    
    jwt_created = users.find_user(data["email"], data["password"])
    if not jwt_created:
        return jsonify({
            'error' : 'email or password incorrect'
        }), 401
    
    return jsonify({
        "jwt" : jwt_created
        }), 200


@user_bp.route("/users", methods=["GET"])
def get_users():
    jwtoken = request.headers.get("Authorization")
    user = get_user(jwtoken)

    
    if user is None:
        return jsonify({'error' : 'user not found'}), 401
    return jsonify(users.get_users()), 200