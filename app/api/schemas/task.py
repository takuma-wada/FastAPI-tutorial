from pydantic import BaseModel, Field
from datetime import datetime


class TaskBase(BaseModel):
    title: str | None = Field(default=None, example="クリーニングを取りに行く")


class Task(TaskBase):
    id: int
    done: bool = Field(default=False, description="完了フラグ")
    createdAt: datetime

    model_config = {"from_attributes": True}


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskCreate):
    id: int

    model_config = {"from_attributes": True}


class TaskDoneResponse(TaskCreate):
    id: int
    done: bool = Field(default=True, description="完了フラグ")
    createdAt: datetime

    model_config = {"from_attributes": True}
