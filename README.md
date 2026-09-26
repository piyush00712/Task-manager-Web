# Task Manager CLI

A command-line task management tool built in Python, with persistent local storage and a clean object-oriented design separating task data, task management, and the CLI itself.

## Features
- Add, list, update, complete, and delete tasks
- Filter listing by pending or completed
- Tasks persist between runs in a local JSON file
- Clean error handling for invalid task IDs (fails with a clear message, doesn't crash)

## Tech Stack
- Python (standard library only — `argparse`, `dataclasses`, `json`)

## Project Structure
```
.
├── taskcli/
│   ├── __init__.py
│   ├── task.py       # Task dataclass + IdGenerator (OOP model)
│   ├── manager.py     # TaskManager: the collection + JSON persistence
│   └── cli.py          # argparse-based command-line interface
└── test_cli.py         # Automated tests covering every command
```

## Design
- **`Task`** (in `task.py`) is a small, self-contained dataclass — it knows how to represent and format itself, and nothing about storage or the CLI.
- **`TaskManager`** (in `manager.py`) owns the collection of tasks and handles loading/saving them to a JSON file. It's the only place that touches the filesystem.
- **`cli.py`** wires up `argparse` subcommands and translates them into `TaskManager` calls. This separation means the core logic (`Task`/`TaskManager`) could be reused behind a different interface (a web API, a GUI) without changes.

## Getting Started

### Run
No installation needed beyond Python 3.
```bash
python -m taskcli.cli add "Write project README"
python -m taskcli.cli list
python -m taskcli.cli complete 1
python -m taskcli.cli list --pending
python -m taskcli.cli update 2 "New title"
python -m taskcli.cli delete 2
```

By default tasks are stored in `~/.taskcli_tasks.json`. Use `--file path/to/file.json` to use a different location.

### Run the automated tests
```bash
python test_cli.py
```
This runs the real CLI as a subprocess (exactly as a user would invoke it) and verifies every command, including edge cases like acting on a non-existent task ID and confirming the JSON storage file's structure is correct after each operation.

## Possible Next Steps
- Add due dates and priority levels
- Add tags/categories and filtering by tag
- Swap JSON storage for SQLite as the task list grows
- Add a `--sort` option (by date created, by status)
