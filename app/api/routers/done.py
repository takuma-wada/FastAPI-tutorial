from fastapi import APIRouter
from app.db import db
import app.api.schemas.task as task_schema

router = APIRouter()


@router.put("/tasks/{task_id}/done", response_model=task_schema.TaskDoneResponse)
async def mark_task_as_done(task_id: int):
    updated_task = await db.task.update(
        where={"id": task_id},
        data={"done": True},
    )
    return task_schema.TaskDoneResponse(**updated_task.dict())


@router.patch("/tasks/{task_id}/done", response_model=task_schema.TaskDoneResponse)
async def unmark_task_as_done(task_id: int):
    unmark_task = await db.task.update(
        where={"id": task_id},
        data={"done": False},
    )
    return task_schema.TaskDoneResponse(**unmark_task.dict())
