import os
# os is a package allowing you to interact with the OS

from flask import Flask, render_template, request, redirect, url_for, g
# flask is the package allowing you to create a web application
# render_template is a function to allow you to render an HTML file
# request is a package allowing you to handle requests from the user
# redirect and url_for are packages to allow you to redirect the user to a different page and get the final URL for the given relative path

from database import db, Todo
from recommendation_engine import RecommendationEngine

app = Flask(__name__)
# __name__ is a special variable in Python representing the name of the currently-running module
basedir = os.path.abspath(os.path.dirname(__file__))
# __file__ is another special variable that represents the current file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "todos.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.before_request
def load_data_to_g():
    todos = Todo.query.all()
    g.todos = todos
    g.todo = None
# The db.init_app(app) function initializes the database with the Flask app instance.
# The with app.app_context(): block creates a context for the application, which is required to interact with the database.
# The db.create_all() function creates the database tables based on the database models defined in the database module.
# The load_data_to_g() function is a before_request handler that runs before each request to the application. It retrieves all of the to-do items from the database and stores them in the g object, which is shared between different parts of the application during a single request.

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_todo():
    # get the data from the form
    todo = Todo(
        name=request.form["todo"],
    )
    # add the new ToDo to the list
    db.session.add(todo)
    db.session.commit()    
    # add the new ToDo to the list
    return redirect(url_for("index"))

@app.route("/remove/<int:id>", methods=["GET", "POST"])
def remove_todo(id):
    db.session.delete(Todo.query.filter_by(id=id).first())
    db.session.commit()
    return redirect(url_for("index"))

# show AI recommendations
@app.route("/recommend/<int:id>", methods=["GET"])
async def recommend(id):
    recommendation_engine = RecommendationEngine()
    g.todo = db.session.query(Todo).filter_by(id=id).first()
    g.todo.recommendations = await recommendation_engine.get_recommendations(g.todo.name)
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)