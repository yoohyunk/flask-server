import hashlib
import time
from flask_server.db import db
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime


class TodoModel(db.Model):
    __tablename__ = 'todos'
    
    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # 64 chars for a SHA-256 hash
    name: Mapped[str]
    description: Mapped[str]
    is_done: Mapped[bool]
    list_id: Mapped[str] = mapped_column(ForeignKey('lists.id'), nullable=False)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    


    todo_list = db.relationship('ListModel', back_populates = 'todos')

    def __init__(self, name: str, list_id: str, description: str = None, is_done: bool = False, due_date: Optional[datetime] = None, start_date: Optional[datetime] = None):
        self.id = self.generate_todo_id(name)
        self.name = name
        self.description = description
        self.is_done = is_done
        self.list_id = list_id
        self.start_date = start_date
        self.due_date = due_date
     
    def generate_todo_id(self, name: str) -> str:
        hash_input = f"{name}{time.time()}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()  # SHA-256 for a 64-char hex hash