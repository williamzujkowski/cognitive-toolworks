"""Python FastAPI Example: simple task service.

Demonstrates: FastAPI, Pydantic models, type hints, async endpoints
"""

from collections.abc import Iterator
from contextlib import contextmanager

from fastapi import FastAPI
from pydantic import BaseModel


class TaskCreate(BaseModel):
    """Task creation request."""

    title: str


class Task(BaseModel):
    """Task model."""

    id: int
    title: str
    done: bool = False


app = FastAPI()
tasks: dict[int, Task] = {}


@contextmanager
def id_generator() -> Iterator[int]:
    """Generate sequential IDs."""
    _id = 1
    while True:
        yield _id
        _id += 1


ids = id_generator()


@app.get("/tasks")
async def list_tasks() -> list[Task]:
    """List all tasks."""
    return list(tasks.values())


@app.post("/tasks", status_code=201)
async def create_task(task_input: TaskCreate) -> Task:
    """Create a new task."""
    task_id = next(ids)
    task = Task(id=task_id, title=task_input.title)
    tasks[task_id] = task
    return task
