from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from flask_server.db import db



class UserModel(db.Model):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(primary_key=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    def __init__(self, email: str, password_hash: str):
        self.email = email
        self.password_hash = password_hash

   