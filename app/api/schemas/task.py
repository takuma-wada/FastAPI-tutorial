from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str | None = Field(default=None, example="クリーニングを取りに行く")


class Task(TaskBase):
    id: int
    done: bool = Field(default=False, description="完了フラグ")

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskCreate):
    id: int

    model_config = {"from_attributes": True}
