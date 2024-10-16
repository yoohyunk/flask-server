from flask_server.db import db
from sqlalchemy.orm import Mapped, mapped_column

class TodoModel(db.Model):
    __tablename__ = 'todos'

    todo_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    is_done: Mapped[bool]