import hashlib
import time
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from flask_server.db import db

class ListModel(db.Model):
    __tablename__ = 'lists'

    list_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str]
    # todoModel = relationship('TodoModel', back_populates='listModel', cascade='all, delete-orphan')

    def __init__(self, name):
        self.list_id = self.generate_list_id(name)
        self.name = name
     
    def generate_list_id(self, name: str) -> str:
        hash_input = f"{name}{time.time()}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest() 