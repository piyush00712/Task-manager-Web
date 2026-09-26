"""
Exercises the real CLI end-to-end via subprocess calls (the actual
command-line interface a user would run), using a temporary storage
file so it doesn't touch the real ~/.taskcli_tasks.json.

Run: python test_cli.py
"""
import json
import subprocess
import sys
import tempfile
import os

STORAGE = tempfile.mktemp(suffix=".json")


def run(*args):
    result = subprocess.run(
        [sys.executable, "-m", "taskcli.cli", "--file", STORAGE, *args],
        capture_output=True, text=True, cwd=os.path.dirname(__file__),
    )
    return result


checks = []


def check(name, condition):
    checks.append((name, condition))
    print(f"{'PASS' if condition else 'FAIL'}: {name}")


# Add tasks
r1 = run("add", "Write CV bullet points")
check("add task 1 succeeds", "Added:" in r1.stdout)

r2 = run("add", "Push projects to GitHub")
check("add task 2 succeeds", "Added:" in r2.stdout)

r3 = run("add", "Apply to Ericsson")
check("add task 3 succeeds", "Added:" in r3.stdout)

# List all
r_list = run("list")
check("list shows all 3 tasks", r_list.stdout.count("#") == 3)

# Complete task 1
r_complete = run("complete", "1")
check("complete task 1 succeeds", "Completed:" in r_complete.stdout)

# List pending only -> should show 2 (task 1 now done)
r_pending = run("list", "--pending")
check("pending filter excludes completed task", "Write CV" not in r_pending.stdout and r_pending.stdout.count("#") == 2)

# List done only -> should show 1
r_done = run("list", "--done")
check("done filter shows only completed task", "Write CV" in r_done.stdout and r_done.stdout.count("#") == 1)

# Update task 2's title
r_update = run("update", "2", "Push all 3 projects to GitHub")
check("update task title succeeds", "Push all 3 projects" in r_update.stdout)

# Delete task 3
r_delete = run("delete", "3")
check("delete task succeeds", "Deleted:" in r_delete.stdout)

r_list_after = run("list")
check("list reflects deletion (2 tasks remain)", r_list_after.stdout.count("#") == 2)

# Acting on a non-existent id should fail cleanly, not crash
r_bad = run("complete", "999")
check("completing a non-existent id fails cleanly", r_bad.returncode != 0 and "Error" in r_bad.stderr)

# Verify persistence: storage file is valid JSON matching in-memory state
with open(STORAGE) as f:
    data = json.load(f)
check("storage file is valid JSON with correct task count", len(data) == 2)
check("persisted task has expected structure", set(data[0].keys()) == {"id", "title", "done", "created_at"})

os.remove(STORAGE)

failed = [name for name, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("All checks passed.")
