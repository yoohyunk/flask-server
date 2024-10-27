from flask_server.db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Enum


class UserListAssociationModel(db.Model):
    __tablename__ = 'user_list_associtaion'

    user_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    list_id: Mapped[str] = mapped_column(String(64), ForeignKey('list.id'), primary_key=True)
    permission: Mapped[str] = mapped_column(Enum('collaborator', 'admin', name="permission_enum"), nullable=False)

    def __init__(self, user_id: str, list_id: str, permission: str):
        self.user_id = user_id
        self.list_id = list_id
        self.permission = permission 

    