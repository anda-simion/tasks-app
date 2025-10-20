from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any
from uuid import uuid4
from datetime import datetime, timezone
from models.task import Task, TaskStatus
from schemas.task import TaskCreate, TaskUpdate


async def get_tasks_crud(
    session: AsyncSession,
    query: Optional[str],
    offset: int,
    limit: int,
) -> Dict[str, Any]:
    stmt = select(Task).where(Task.status != TaskStatus.deleted)
    if query:
        stmt = stmt.where(Task.text.ilike(f"%{query}%"))

    stmt_total = stmt.order_by(desc(Task.created_at))
    all_tasks_result = await session.execute(stmt_total)
    total = len(all_tasks_result.scalars().all())
    stmt_paginated = stmt_total.offset(offset).limit(limit)
    result = await session.execute(stmt_paginated)
    tasks = result.scalars().all()

    return {"tasks": tasks, "total": total, "offset": offset, "limit": limit}


async def create_task_crud(session: AsyncSession, task_data: TaskCreate) -> Task:
    new_task = Task(id=uuid4(), text=task_data.text, status=task_data.status)

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return new_task


async def update_task_crud(
    session: AsyncSession,
    task_id: str,
    update_data: TaskUpdate,
) -> Optional[Task]:
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        return None

    if update_data.text is not None:
        task.text = update_data.text.strip()

    if update_data.status is not None:
        task.status = update_data.status

    task.updated_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(task)

    return task


async def delete_task_crud(session: AsyncSession, task_id: str) -> Optional[Task]:
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        return None

    task.status = TaskStatus.deleted
    await session.commit()
    await session.refresh(task)

    return task
