"""
TaskManager: owns the collection of tasks and handles loading/saving
them to a JSON file. It's the only place that touches the filesystem.
"""
import json
import os
from pathlib import Path

from .task import Task, IdGenerator

DEFAULT_STORAGE = str(Path.home() / ".taskcli_tasks.json")


class TaskNotFoundError(Exception):
    def __init__(self, task_id):
        super().__init__(f"No task with id {task_id}")
        self.task_id = task_id


class TaskManager:
    def __init__(self, storage_path=None):
        self.storage_path = storage_path or DEFAULT_STORAGE
        self.tasks = self._load()

    # ---------- persistence ----------

    def _load(self):
        if not os.path.exists(self.storage_path):
            return []
        with open(self.storage_path, "r") as f:
            raw = json.load(f)
        return [Task.from_dict(item) for item in raw]

    def _save(self):
        with open(self.storage_path, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    # ---------- operations ----------

    def add(self, title):
        task = Task(id=IdGenerator.next_id(self.tasks), title=title)
        self.tasks.append(task)
        self._save()
        return task

    def list(self, pending_only=False, done_only=False):
        tasks = self.tasks
        if pending_only:
            tasks = [t for t in tasks if not t.done]
        elif done_only:
            tasks = [t for t in tasks if t.done]
        return tasks

    def _find(self, task_id):
        for t in self.tasks:
            if t.id == task_id:
                return t
        raise TaskNotFoundError(task_id)

    def complete(self, task_id):
        task = self._find(task_id)
        task.done = True
        self._save()
        return task

    def update(self, task_id, new_title):
        task = self._find(task_id)
        task.title = new_title
        self._save()
        return task

    def delete(self, task_id):
        task = self._find(task_id)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self._save()
        return task
