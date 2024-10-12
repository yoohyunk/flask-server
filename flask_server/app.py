from flask import Flask
from flask_server.routes.todolist import todolist_bp


app = Flask(__name__)
app.register_blueprint(todolist_bp, url_prefix="/todolist")


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
