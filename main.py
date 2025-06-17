from flask import Flask, redirect, url_for, render_template, flash, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Boolean
from forms import AddTaskForm
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
bootstrap = Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///tasks.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CONFIGURE TABLES
class Task(db.Model):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task: Mapped[str] = mapped_column(String(100), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    le_tasks = Task.query.all()
    column_titles = Task.__table__.columns.keys()
    title_case_titles = [title.title() for title in column_titles[:-1]]
    return render_template('tasks.html', tasks=le_tasks, titles=title_case_titles)

@app.route('/add-task', methods=['GET', 'POST'])
def add_task():
    form = AddTaskForm()
    if form.validate_on_submit(): # Post request made
        task = form.task.data
        new_task = Task(
            task=task
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Successfully added task to to-do list!")
        return redirect(url_for('tasks'))
    else:
        if request.method == 'POST':
            flash("Something went wrong while adding your task.")

    return render_template('add-task.html', form=form)

@app.route('/delete-task/<int:task_id>')
def delete_task(task_id):
    selected_task = db.get_or_404(Task, task_id)
    db.session.delete(selected_task)
    db.session.commit()
    flash("Task successfully deleted.", 'danger')
    return redirect(url_for('tasks'))

@app.route('/check-off-task/<int:task_id>')
def check_off_task(task_id):
    selected_task = db.get_or_404(Task, task_id)
    selected_task.completed = True
    db.session.commit()
    flash("Task has been checked off!", 'success')
    return redirect(url_for('tasks'))

@app.route('/uncheck-task/<int:task_id>')
def uncheck_task(task_id):
    selected_task = db.get_or_404(Task, task_id)
    selected_task.completed = False
    db.session.commit()
    flash("Task has been unchecked.", 'info')
    return redirect(url_for('tasks'))

if __name__ == "__main__":
    # Ensure the GitHub user has a db to use by creating one automatically
    with app.app_context():
        db.create_all()
    app.run(debug=True)