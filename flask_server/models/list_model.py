import hashlib
import time
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from flask_server.db import db

class ListModel(db.Model):
    __tablename__ = 'lists'

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str]
    todos = db.relationship('TodoModel', back_populates='todo_list', cascade='all, delete-orphan')
    owners: Mapped[List['UserListAssociationModel']] = relationship()

    def __init__(self, name: str):
        self.id = self.generate_list_id(name)
        self.name = name
     
    def generate_list_id(self, name: str) -> str:
        hash_input = f"{name}{time.time()}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest() 