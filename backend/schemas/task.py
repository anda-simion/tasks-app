from pydantic import BaseModel, Field, field_validator
from typing import Optional, Annotated
from models.task import TaskStatus

NonEmptyString = Annotated[str, Field(strip_whitespace=True, min_length=1)]


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

    @field_validator("text")
    @classmethod
    def no_empty_text(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Task text cannot be empty")
        return v
