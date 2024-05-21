import os
# os is a package allowing you to interact with the OS

from flask import Flask, render_template, request, redirect, url_for
# flask is the package allowing you to create a web application
# render_template is a function to allow you to render an HTML file
# request is a package allowing you to handle requests from the user
# redirect and url_for are packages to allow you to redirect the user to a different page and get the final URL for the given relative path

app = Flask(__name__)
# __name__ is a special variable in Python representing the name of the currently-running module
basedir = os.path.abspath(os.path.dirname(__file__))
# __file__ is another special variable that represents the current file
todo_file = os.path.join(basedir, "todo_list.txt")

todo_list = []

# load the to-do list from a file
try:
    print("Loading the to-do list from the file")
    with open(todo_file, "r") as file:
        for line in file:
            todo_list.append(line.strip())
except FileNotFoundError:
    pass #simply start with an empty list

@app.route("/")
def index():
    return render_template("index.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add_todo():
    todo = request.form["todo"]
    todo_list.append(todo)
    save_todo_list()
    return redirect(url_for("index"))

@app.route("/remove", methods=["POST"])
def remove_todo():
    item_number = int(request.form["item_number"])
    if 0 < item_number <= len(todo_list):
        todo_list.pop(item_number - 1)
        save_todo_list()
    return redirect(url_for("index"))

def save_todo_list():
    with open(todo_file, "w") as file:
        for todo in todo_list:
            file.write(todo + "\n")

if __name__ == "__main__":
    app.run(debug=True)