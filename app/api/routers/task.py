from typing import List
from fastapi import APIRouter
import app.api.schemas.task as task_schema
from app.db import db

router = APIRouter()


@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks():
    return await db.task.find_many(order={"createdAt": "desc"})


@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate):
    new_task = await db.task.create(
        data={
            "title": task_body.title,
            "done": False,
        }
    )
    return task_schema.TaskCreateResponse(**new_task.dict())


@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate):
    updated_task = await db.task.update(
        where={"id": task_id},
        data={
            "title": task_body.title,
        },
    )
    return task_schema.TaskCreateResponse(**updated_task.dict())


@router.delete("/tasks/{task_id}", response_model=str)
async def delete_task(task_id: int):
    await db.task.delete(where={"id": task_id})

    return f"Task number {task_id} was deleted successfully"
