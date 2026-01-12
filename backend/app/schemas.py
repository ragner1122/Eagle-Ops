from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    role: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    created_at: datetime
    assignee_id: int | None

    class Config:
        from_attributes = True


class RunbookOut(BaseModel):
    id: int
    title: str
    steps: str
    owner: str

    class Config:
        from_attributes = True


class KnowledgeArticleOut(BaseModel):
    id: int
    title: str
    summary: str
    tags: str

    class Config:
        from_attributes = True


class TelemetryMetricOut(BaseModel):
    id: int
    name: str
    value: str
    status: str
    captured_at: datetime

    class Config:
        from_attributes = True
