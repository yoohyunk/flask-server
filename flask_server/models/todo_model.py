import hashlib
import time
from flask_server.db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class TodoModel(db.Model):
    __tablename__ = 'todos'
    
    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # 64 chars for a SHA-256 hash
    name: Mapped[str]
    description: Mapped[str]
    is_done: Mapped[bool]
    list_id: Mapped[str] = mapped_column(ForeignKey('lists.id'), nullable=False) 

    todo_list = db.relationship('ListModel', back_populates = 'todos')

    def __init__(self, name: str, list_id: str, description: str = None, is_done: bool = False):
        self.id = self.generate_todo_id(name)
        self.name = name
        self.description = description
        self.is_done = is_done
        self.list_id = list_id
     
    def generate_todo_id(self, name: str) -> str:
        hash_input = f"{name}{time.time()}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()  # SHA-256 for a 64-char hex hash