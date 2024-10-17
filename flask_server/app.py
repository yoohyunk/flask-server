from flask import Flask
from flask_server.routes.todolist import todolist_bp
from flask_server.db import db, get_database_uri


app = Flask(__name__)

database_uri = get_database_uri()

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(todolist_bp, url_prefix="/")


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
