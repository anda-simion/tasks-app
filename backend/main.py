from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.future import select
from datetime import datetime, timezone
from schemas.task import TaskCreate, TaskUpdate
from models.task import Task, TaskStatus
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://tasks_user:tasks_password@db:5432/tasks_db"
)


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

app = FastAPI(title="Tasks API")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/tasks")
async def get_tasks(
    query: Optional[str] = Query(None, min_length=1, max_length=50),
    offset: int = Query(0, ge=0),
    limit: int = Query(5, ge=1, le=50),
):
    async with async_session() as session:
        stmt = select(Task).where(Task.status != TaskStatus.deleted)
        if query:
            stmt = stmt.where(Task.text.ilike(f"%{query}%"))

        stmt = stmt.order_by(desc(Task.created_at))

        total = len((await session.execute(stmt)).scalars().all())

        stmt = stmt.offset(offset).limit(limit)
        result = await session.execute(stmt)
        tasks = result.scalars().all()
        return {"tasks": tasks, "total": total, "offset": offset, "limit": limit}


@app.post("/tasks")
async def create_task(task: TaskCreate):
    async with async_session() as session:
        new_task = Task(id=uuid4(), text=task.text, status=task.status)
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        return {"message": "Task created", "task": new_task}


@app.patch("/tasks/{task_id}")
async def update_task(task_id: str, update_task: TaskUpdate):
    async with async_session() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if update_task.text is not None:
            task.text = update_task.text.strip()
        if update_task.status is not None:
            task.status = update_task.status
        task.updated_at = datetime.now(timezone.utc)
        await session.commit()
        await session.refresh(task)
        return {"message": "Task updated", "task": task}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    async with async_session() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task.status = TaskStatus.deleted
        await session.commit()
        await session.refresh(task)
        return {"message": "Task marked as deleted", "task": task}
