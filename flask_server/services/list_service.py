from flask_server.models.list_model import ListModel
from flask_server.models.user_list_model import UserListAssociationModel
from flask_server.db import db

class ListService:
    def add(self, userId: str, list_name: str):
        new_list = ListModel(name=list_name)
        association = UserListAssociationModel(user_id=userId, list_id=new_list.id, permission='owner')
        db.session.bulk_save_objects([new_list, association])
        db.session.commit()

        return True
    
    def delete(self, userId: str, id: str):
        list_to_delete = db.session.get(ListModel, id)
        permission = UserListAssociationModel.query.filter_by(user_id=userId, list_id=id).first()
        if permission is None or permission.permission == "collaborator":
            return False
        
        if list_to_delete:
            associations = UserListAssociationModel.query.filter_by(list_id=id).all()
            for association in associations:
                db.session.delete(association)
            db.session.delete(list_to_delete)
            db.session.commit()
            return True
        
        return False
        
    def edit(self, userId: str, id: str, new_name: str):
        list_to_edit = db.session.get(ListModel, id)
        permission = UserListAssociationModel.query.filter_by(user_id=userId, list_id=id).first()
        if permission is None or permission.permission == "collaborator":
            return False

        if list_to_edit:
            list_to_edit.name = new_name
            db.session.commit()
            return True
        
        return False
    
    def get_all_lists(self, userId):
        lists = UserListAssociationModel.query.filter_by(user_id=userId).all()

        if lists:
            all_lists=[{
                    "Id" : list.list_id,
                    "Name" : db.session.get(ListModel, list.list_id).name
                } for list in lists]
        
            return all_lists
        return False
    
    # def add_collaborator(self, userId: str, collaborator_id: str, id: str):
    #     list_to_add_collaborator = db.session.get(ListModel, id)
    #     permission = UserListAssociationModel.query.filter_by(user_id=userId, list_id=id).first
    #     if permission is None or permission.permission == "collaborator":
    #         return False
    #     new_collaborator = UserListAssociationModel(user_id=collaborator_id, list_id=id)
    #     db.session.add(new_collaborator)
    #     db.session.commit()
    #     return True
