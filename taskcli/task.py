"""
Task: a small, self-contained dataclass. It knows how to represent and
format itself, and nothing about storage or the CLI.
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            done=data["done"],
            created_at=data["created_at"],
        )

    def format_line(self):
        status = "x" if self.done else " "
        return f"#{self.id} [{status}] {self.title}"


class IdGenerator:
    """Hands out the next integer id given the current set of tasks."""

    @staticmethod
    def next_id(tasks):
        if not tasks:
            return 1
        return max(t.id for t in tasks) + 1
