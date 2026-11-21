from datetime import datetime

from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    filename: str = Field(min_length=1, max_length=255)


class DocumentResponse(BaseModel):
    id: int
    title: str
    filename: str
    status: str
    created_at: datetime