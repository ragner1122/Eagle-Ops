from datetime import datetime
from typing import Literal
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
    severity: str
    sla_status: str
    created_at: datetime
    updated_at: datetime
    assignee_id: int | None
    assignee: UserOut | None

    class Config:
        from_attributes = True


TicketStatus = Literal["New", "In Progress", "Waiting Client", "Resolved"]
TicketSeverity = Literal["Low", "Medium", "High", "Critical"]
SlaStatus = Literal["On Track", "At Risk", "Breached"]


class TicketCreate(BaseModel):
    title: str
    description: str
    status: TicketStatus = "New"
    severity: TicketSeverity = "Medium"
    sla_status: SlaStatus = "On Track"
    assignee_id: int | None = None


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TicketStatus | None = None
    severity: TicketSeverity | None = None
    sla_status: SlaStatus | None = None
    assignee_id: int | None = None


class TicketNoteCreate(BaseModel):
    body: str


class TicketNoteOut(BaseModel):
    id: int
    body: str
    author: str
    created_at: datetime

    class Config:
        from_attributes = True


class TicketDetailOut(TicketOut):
    notes: list[TicketNoteOut]


class RunbookCreate(BaseModel):
    title: str | None = None
    project_type: str
    client: str
    site: str
    version: str
    window: str
    rollback_plan_required: bool = False
    pre_check: str
    steps: str
    rollback: str
    validation: str
    comms: str


class RunbookOut(BaseModel):
    id: int
    title: str
    project_type: str
    client: str
    site: str
    version: str
    window: str
    rollback_plan_required: bool
    pre_check: str
    steps: str
    rollback: str
    validation: str
    comms: str
    owner: str

    class Config:
        from_attributes = True


class KnowledgeArticleCreate(BaseModel):
    title: str
    content: str
    tags: list[str]


class KnowledgeArticleOut(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str]
    created_by: str
    created_at: datetime
    updated_at: datetime


class TelemetryMetricOut(BaseModel):
    id: int
    name: str
    value: str
    status: str
    captured_at: datetime

    class Config:
        from_attributes = True
