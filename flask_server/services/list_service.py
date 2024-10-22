from flask_server.models.list_model import ListModel
from flask_server.db import db

class List:
    def add(self, list_name: str):
        
        new_list = ListModel(
            name = list_name
        )

        db.session.add(new_list)
        db.session.commit()

        return True
    
    def delete(self, id: str):
        list_to_delete = db.session.get(ListModel, id)

        if list_to_delete:
            db.session.delete(list_to_delete)
            db.session.commit()
            return True
        
        return False
        
    def edit(self, id: str, new_name: str):
        list_to_edit = db.session.get(ListModel, id)

        if list_to_edit:
            list_to_edit.name = new_name
            db.session.commit()
            return True
        
        return False
    
    def get_all_lists(self):
        lists = ListModel.query.all()
        if lists:
            all_lists=[{
                    "Id" : list.id,
                    "Name" : list.name
                } for list in lists]
        
            return all_lists
        return False