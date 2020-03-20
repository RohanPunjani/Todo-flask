from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":

        task_content = request.form['content']
        newTask = Todo(content=task_content)
        if task_content is not "":
            try:
                db.session.add(newTask)
                db.session.commit()
                return redirect('/')
            except:
                return "There was an issue adding a task"
        else:
            return redirect('/')
    else:
        taskspending = Todo.query.filter(Todo.completed == 0).order_by(Todo.date_created).all()
        taskscompleted = Todo.query.filter(Todo.completed == 1).order_by(Todo.date_created).all()
        return render_template('index.html', taskspending=taskspending , taskscompleted=taskscompleted)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Cant delete, got some issues"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Cant update, got some issues"
    else:
        return render_template('update.html', task=task_to_update)

@app.route('/markasdone/<int:id>')
def markasdone(id):
    task_to_update = Todo.query.get_or_404(id)
    task_to_update.completed = 1
    try:
        db.session.commit()
        return redirect('/')
    except:
        return "Cant update, got some issues"

@app.route('/markasundone/<int:id>')
def markasundone(id):
    task_to_update = Todo.query.get_or_404(id)
    task_to_update.completed = 0
    try:
        db.session.commit()
        return redirect('/')
    except:
        return "Cant update, got some issues"

if __name__ == "__main__":
    app.run(debug=True)
