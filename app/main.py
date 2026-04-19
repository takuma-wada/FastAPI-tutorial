from fastapi import FastAPI
from app.api.routers import task, done
from contextlib import asynccontextmanager
from app.db import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(task.router)
app.include_router(done.router)


@app.get("/hello")
async def hello():
    return {"message": "hello world!"}
