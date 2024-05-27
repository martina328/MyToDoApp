import json
import os
# os is a package allowing you to interact with the OS

from flask import Flask, render_template, request, redirect, url_for, g
# flask is the package allowing you to create a web application
# render_template is a function to allow you to render an HTML file
# request is a package allowing you to handle requests from the user
# redirect and url_for are packages to allow you to redirect the user to a different page and get the final URL for the given relative path

from database import db, Todo
from recommendation_engine import RecommendationEngine
from tab import Tab
from priority import Priority
from context_processors import inject_current_date

app = Flask(__name__)
# __name__ is a special variable in Python representing the name of the currently-running module
basedir = os.path.abspath(os.path.dirname(__file__))   # Get the directory of the this file
todo_file = os.path.join(basedir, 'todo_list.txt')     # Create the path to the to-do list file using the directory
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'todos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.context_processor
def inject_common_variables():
    return inject_current_date()

with app.app_context():
    db.create_all()

@app.before_request
def load_data_to_g():
    todos = Todo.query.all()
    g.todos = todos 
    g.todo = None
    g.TabEnum = Tab
    g.PriorityEnum = Priority
    g.selectedTab = Tab.NONE
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

# Details of ToDo Item
@app.route('/details/<int:id>', methods=['GET'])
def details(id):
    g.selectedTab = Tab.DETAILS
    g.todos = Todo.query.all()
    g.todo = Todo.query.filter_by(id=id).first()
    
    return render_template('index.html')

# Edit a new ToDo
@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    g.selectedTab = Tab.EDIT
    g.todos = Todo.query.all()
    g.todo = Todo.query.filter_by(id=id).first()

    return render_template('index.html')

# Save existing To Do Item
@app.route('/update/<int:id>', methods=['POST'])
def update_todo(id):
    g.selectedTab = Tab.DETAILS

    if request.form.get('cancel') != None:
        return redirect(url_for('index'))

    # Get the data from the form
    name = request.form['name']
    due_date = request.form.get('duedate')
    notes=request.form.get('notes')
    priority=request.form.get('priority')
    completed=request.form.get('completed')

    todo = db.session.query(Todo).filter_by(id=id).first()
    if todo != None:
        todo.name = name

        if due_date != "None":
            todo.due_date = due_date

        if notes != None:
            todo.notes = notes

        if priority != None:
            todo.priority = int(priority) 

        if completed == None:
            todo.completed = False
        elif completed == "on":
            todo.completed = True
    #
    db.session.add(todo)
    db.session.commit()
    #
    return redirect(url_for('index'))


# Delete a ToDo
@app.route('/remove/<int:id>', methods=["POST"])
def remove_todo(id):
    g.selectedTab = Tab.NONE
    db.session.delete(Todo.query.filter_by(id=id).first())
    db.session.commit()
    return redirect(url_for('index'))

# Show AI recommendations
@app.route('/recommend/<int:id>', methods=['GET'])
@app.route('/recommend/<int:id>/<refresh>', methods=['GET'])
async def recommend(id, refresh=False):
    g.selectedTab = Tab.RECOMMENDATIONS
    recommendation_engine = RecommendationEngine()
    g.todo = db.session.query(Todo).filter_by(id=id).first()

    if g.todo and not refresh:
        try:
            #attempt to load any saved recommendation from the DB
            if g.todo.recommendations_json is not None:
                g.todo.recommendations = json.loads(g.todo.recommendations_json)
                return render_template('index.html')
        except ValueError as e:
            print("Error:", e)

    previous_links_str = None
    if refresh:
        g.todo.recommendations = json.loads(g.todo.recommendations_json)
        # Extract links
        links = [item["link"] for item in g.todo.recommendations]
        # Convert list of links to a single string
        previous_links_str = ", ".join(links)

    g.todo.recommendations = await recommendation_engine.get_recommendations(g.todo.name, previous_links_str)
    
    # Save the recommendations to the database
    try:
        g.todo.recommendations_json = json.dumps(g.todo.recommendations)
        db.session.add(g.todo)
        db.session.commit()
    except Exception as e:
        print(f"Error adding and committing todo: {e}")
        return

    return render_template('index.html')

@app.route('/completed/<int:id>/<complete>', methods=['GET'])
def completed(id, complete):
    g.selectedTab = Tab.NONE
    g.todo = Todo.query.filter_by(id=id).first()
    if (g.todo != None and complete == "true"):
        g.todo.completed = True
    elif (g.todo != None and complete == "false"):
        g.todo.completed = False
    #update todo in the database
    db.session.add(g.todo)
    db.session.commit()
    #
    return redirect(url_for('index'))    

if __name__ == "__main__":
    app.run(debug=True)