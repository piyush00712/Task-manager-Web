"""
argparse-based command-line interface. Wires up subcommands and
translates them into TaskManager calls. Kept thin on purpose so the
core logic (Task/TaskManager) could be reused behind a different
interface (a web API, a GUI) without changes.
"""
import argparse
import sys

from .manager import TaskManager, TaskNotFoundError


def build_parser():
    parser = argparse.ArgumentParser(prog="taskcli", description="A simple command-line task manager.")
    parser.add_argument("--file", dest="file", default=None, help="Path to the JSON storage file (default: ~/.taskcli_tasks.json)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    p_add = subparsers.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task title")

    p_list = subparsers.add_parser("list", help="List tasks")
    group = p_list.add_mutually_exclusive_group()
    group.add_argument("--pending", action="store_true", help="Show only pending tasks")
    group.add_argument("--done", action="store_true", help="Show only completed tasks")

    p_complete = subparsers.add_parser("complete", help="Mark a task as complete")
    p_complete.add_argument("id", type=int, help="Task id")

    p_update = subparsers.add_parser("update", help="Update a task's title")
    p_update.add_argument("id", type=int, help="Task id")
    p_update.add_argument("title", help="New task title")

    p_delete = subparsers.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int, help="Task id")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    manager = TaskManager(storage_path=args.file)

    try:
        if args.command == "add":
            task = manager.add(args.title)
            print(f"Added: {task.format_line()}")

        elif args.command == "list":
            tasks = manager.list(pending_only=args.pending, done_only=args.done)
            if not tasks:
                print("No tasks found.")
            for t in tasks:
                print(t.format_line())

        elif args.command == "complete":
            task = manager.complete(args.id)
            print(f"Completed: {task.format_line()}")

        elif args.command == "update":
            task = manager.update(args.id, args.title)
            print(f"Updated: {task.format_line()}")

        elif args.command == "delete":
            task = manager.delete(args.id)
            print(f"Deleted: {task.format_line()}")

    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
