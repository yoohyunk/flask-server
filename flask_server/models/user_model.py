import hashlib
import time
from flask_server.db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class UserModel(db.Model):
    __table_name__ = 'users'

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  
    name: Mapped[str]

    def __init__(self, name: str):
        self.id = self.generate_user_id(name)
        self.name = name 

    def generate_user_id(self, name: str) -> str:
        hash_input = f"{name}{time.time()}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest() 