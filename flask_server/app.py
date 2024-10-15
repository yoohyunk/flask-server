from flask import Flask
from flask_server.routes.todolist import todolist_bp
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(todolist_bp, url_prefix="/")


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
