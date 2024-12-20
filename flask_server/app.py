from flask import Flask
from flask_cors import CORS
from flask_server.routes.todo import todo_bp
from flask_server.routes.list import list_bp
from flask_server.routes.auth import user_bp
from flask_server.db import db, get_database_uri


app = Flask(__name__)
CORS(app)

database_uri = get_database_uri()

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(todo_bp, url_prefix="/lists")
app.register_blueprint(list_bp, url_prefix="/lists")
app.register_blueprint(user_bp, url_prefix="/users")



@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
