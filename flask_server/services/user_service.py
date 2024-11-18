from flask_server.db import db
from flask_server.models.user_model import UserModel
from flask_server.utils.hash_user_password import hash_password, check_password
from flask_server.utils.jwt import create_jwt


class UserService:
    def add_user(self, user_email: str, user_password: str):
        email_exist = db.session.get(UserModel, user_email)

        if email_exist:
            return False
        
        new_user = UserModel(email = user_email, password_hash = hash_password(user_password))
        db.session.add(new_user)
        db.session.commit()
        return create_jwt(user_email)

    def find_user(self, user_email: str, user_password: str):
        user_matches_email = db.session.get(UserModel, user_email)
        if user_matches_email is None:
            return False
        
        hash_password = user_matches_email.password_hash
        password_matches = check_password(hash_password, user_password)
        if not password_matches:
            return False
        
        return create_jwt(user_email)

    def get_users(self):
        users = UserModel.query.all()
        return [user.email for user in users]