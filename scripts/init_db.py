from flask_server.app import app
from flask_server.db import db
from flask_server.models.todo_model import TodoModel

with app.app_context():
    db.create_all()