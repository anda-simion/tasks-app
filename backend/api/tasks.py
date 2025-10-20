from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, Dict, List, Union
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from crud.tasks import (
    get_tasks_crud,
    create_task_crud,
    update_task_crud,
    delete_task_crud,
)
from schemas.task import Task as TaskSchema, TaskCreate, TaskUpdate

router = APIRouter()


@router.get(
    "/tasks", response_model=Dict[str, Union[List[TaskSchema], int, Optional[str]]]
)
async def get_tasks(
    session: AsyncSession = Depends(get_db),
    query: Optional[str] = Query(None, min_length=1, max_length=50),
    offset: int = Query(0, ge=0),
    limit: int = Query(5, ge=1, le=50),
):
    return await get_tasks_crud(session, query, offset, limit)


@router.post("/tasks", response_model=Dict[str, Union[str, TaskSchema]])
async def create_task(
    task: TaskCreate,
    session: AsyncSession = Depends(get_db),
):
    new_task = await create_task_crud(session, task)
    return {"message": "Task created", "task": new_task}


@router.patch("/tasks/{task_id}", response_model=Dict[str, Union[str, TaskSchema]])
async def update_task(
    task_id: str,
    update_task_data: TaskUpdate,
    session: AsyncSession = Depends(get_db),
):
    task = await update_task_crud(session, task_id, update_task_data)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task updated", "task": task}


@router.delete("/tasks/{task_id}", response_model=Dict[str, Union[str, TaskSchema]])
async def delete_task(
    task_id: str,
    session: AsyncSession = Depends(get_db),
):
    task = await delete_task_crud(session, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task marked as deleted", "task": task}
