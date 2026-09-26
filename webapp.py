"""
A small Flask front end for the Task Manager CLI's core logic.
Reuses taskcli.manager.TaskManager directly — no changes to the
CLI package were needed, since it was already designed to be
reusable behind a different interface.
"""
from flask import Flask, render_template, request, redirect, url_for, flash

from taskcli.manager import TaskManager, TaskNotFoundError

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-production"

manager = TaskManager()


@app.route("/")
def index():
    view = request.args.get("view", "all")
    if view == "pending":
        tasks = manager.list(pending_only=True)
    elif view == "done":
        tasks = manager.list(done_only=True)
    else:
        tasks = manager.list()
    counts = {
        "all": len(manager.list()),
        "pending": len(manager.list(pending_only=True)),
        "done": len(manager.list(done_only=True)),
    }
    return render_template("index.html", tasks=tasks, view=view, counts=counts)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        manager.add(title)
    else:
        flash("Task title can't be empty.")
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    try:
        manager.complete(task_id)
    except TaskNotFoundError:
        flash(f"No task with id {task_id}.")
    return redirect(url_for("index", view=request.args.get("view", "all")))


@app.route("/update/<int:task_id>", methods=["POST"])
def update(task_id):
    title = request.form.get("title", "").strip()
    try:
        if title:
            manager.update(task_id, title)
        else:
            flash("Task title can't be empty.")
    except TaskNotFoundError:
        flash(f"No task with id {task_id}.")
    return redirect(url_for("index", view=request.args.get("view", "all")))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    try:
        manager.delete(task_id)
    except TaskNotFoundError:
        flash(f"No task with id {task_id}.")
    return redirect(url_for("index", view=request.args.get("view", "all")))


if __name__ == "__main__":
    app.run(debug=True)
