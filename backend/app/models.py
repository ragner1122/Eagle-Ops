from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="Analyst")

    tickets = relationship("Ticket", back_populates="assignee")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="New")
    severity = Column(String(50), default="Medium")
    sla_status = Column(String(50), default="On Track")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    assignee = relationship("User", back_populates="tickets")
    notes = relationship(
        "TicketNote",
        back_populates="ticket",
        cascade="all, delete-orphan",
        order_by="TicketNote.created_at.desc()",
    )


class TicketNote(Base):
    __tablename__ = "ticket_notes"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False, index=True)
    body = Column(Text, nullable=False)
    author = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="notes")


class Runbook(Base):
    __tablename__ = "runbooks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    steps = Column(Text, nullable=False)
    owner = Column(String(255), nullable=False)


class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(255), nullable=False)
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TelemetryMetric(Base):
    __tablename__ = "telemetry_metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    captured_at = Column(DateTime, default=datetime.utcnow)
