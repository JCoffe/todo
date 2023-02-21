import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


#Table configuration
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Integer, nullable=True)

    with app.app_context():
        db.create_all()



@app.route("/")
def home():
    todo_list = Todo.query.filter_by(completed=None).all()
    todo_list_completed = Todo.query.filter_by(completed=1).all()

    return render_template("index2.html", todo_list=todo_list, todo_list_completed=todo_list_completed)


@app.route("/add", methods=["GET", "POST"])
def todo_create():
    if request.method == "POST":
        todo = Todo(
            headline=request.form["headline"],
        )
        db.session.add(todo)
        db.session.commit()
        todo_list = ""
        print(todo.headline)
        return redirect(url_for("home"))

    return render_template("index2.html")


@app.route("/complete", methods=["GET", "POST"])
def todo_completed():
    if request.method == "POST":
        print(request.args.get("submit_button"))


        return redirect(url_for("home"))
    todo = db.session.execute(db.select(Todo).where(Todo.id == request.args.get("submit_button"))).first()
    print(todo[0].headline)
    todo[0].completed = 1
    db.session.commit()
    request.args.get("submit_button")
    return redirect(url_for("home"))


@app.route("/clear_completed", methods=["GET", "POST"])
def todo_completed_clear():

    todo_list_completed = Todo.query.filter_by(completed=1).all()
    for todo in todo_list_completed:
        db.session.delete(todo)
        db.session.commit()

    return redirect(url_for("home"))



if __name__ == '__main__':
    app.run(debug=True)
