from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Annotated
from uuid import UUID
from datetime import datetime
from models.task import TaskStatus

NonEmptyString = Annotated[str, Field(strip_whitespace=True, min_length=1)]


class Task(BaseModel):
    id: UUID
    text: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    text: str
    status: Optional[TaskStatus] = TaskStatus.not_done

    @field_validator("text")
    @classmethod
    def no_empty_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Task text cannot be empty")
        return v


class TaskUpdate(BaseModel):
    text: Optional[NonEmptyString] = None
    status: Optional[TaskStatus] = None
    model_config = ConfigDict(from_attributes=True)

    @field_validator("text")
    @classmethod
    def no_empty_text(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Task text cannot be empty")
        return v
