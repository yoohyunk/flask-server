from flask_server.models.user_model import UserModel
from flask_server.db import db


class User:
    def add_user(self, new_user_name: str):
        new_user = UserModel(
            name = new_user_name
        )
        db.session.add(new_user)
        db.session.commit()
        return True

    def delete_user(self, user_id: str):
        user_to_delete = db.session.get(UserModel, user_id)

        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            return True
        
        return False
    
    def edit_user_name(self, user_id: str, new_name: str):
        user_to_edit = db.session.get(UserModel, user_id)

        if user_to_edit:
            user_to_edit.name = new_name
            db.session.commit()
            return True
        
        return False
    
    def get_all_users(self):
        users = UserModel.query.all()
        if users:
            all_users=[{
                    "Id" : user.id,
                    "Name" : user.name
                } for user in users]
        
            return all_users
        return False