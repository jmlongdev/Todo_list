from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Creates the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo-list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# this is the class that each creates object
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)


db.create_all()


@app.route('/', methods=['GET'])
def home():
    all_todos = db.session.query(Todo).all()
    return render_template('index.html', todos=all_todos)


# Adds a task to the database
@app.route('/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_todo = Todo(title=request.form['title'])
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('index.html')


# Edits the tasks time to complete
@app.route('/edit', methods=['GET', 'POST'])
def edit_todo():
    if request.method == 'POST':
        todo_id = request.form['id']
        todo_to_update = Todo.query.get(todo_id)
        todo_to_update.title = request.form['title']
        db.session.commit()
        return redirect(url_for('home'))
    todo_id = request.args.get('id')
    todo_selected = Todo.query.get(todo_id)
    return render_template('edit.html', selected_todo=todo_selected)


# Deletes the task
@app.route('/delete')
def delete_todo():
    if request.method == 'GET':
        todo_id = request.args.get('id')
        todo_to_delete = Todo.query.get(todo_id)
        db.session.delete(todo_to_delete)
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)


# <!--{% block scripts %}-->
# <!--<script src="static/scripts/scripts.js"></script>-->
# <!--{% endblock %}-->

