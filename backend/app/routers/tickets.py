from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Ticket, TicketNote, TicketAiAssist
from ..schemas import (
    TicketOut,
    TicketCreate,
    TicketUpdate,
    TicketDetailOut,
    TicketNoteCreate,
    TicketNoteOut,
    TicketAiAssistOut,
)
from ..auth import get_current_user

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/", response_model=list[TicketOut])
def list_tickets(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return db.query(Ticket).order_by(Ticket.created_at.desc()).all()


@router.post("/", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    ticket = Ticket(**payload.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/{ticket_id}", response_model=TicketDetailOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    payload: TicketUpdate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(ticket, key, value)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(ticket)
    db.commit()


@router.post("/{ticket_id}/notes", response_model=TicketNoteOut, status_code=201)
def add_ticket_note(
    ticket_id: int,
    payload: TicketNoteCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    note = TicketNote(ticket_id=ticket.id, body=payload.body, author=user.email)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.post("/{ticket_id}/ai-assist", response_model=TicketAiAssistOut, status_code=201)
def generate_ticket_ai_assist(
    ticket_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    summary = (
        f"{ticket.title} is currently {ticket.status.lower()} with {ticket.severity.lower()} "
        f"severity. {ticket.description}"
    )
    likely_causes = "\n".join(
        [
            "Recent configuration changes or deployments affecting impacted region.",
            "Upstream dependency instability or degraded infrastructure capacity.",
            "Authentication or network policy changes causing access failures.",
        ]
    )
    next_actions = "\n".join(
        [
            "Confirm scope of impact and affected user segments with the customer.",
            "Pull logs/metrics from the last 2 hours and compare against baseline.",
            "Engage relevant service owners and provide ETA update in the ticket.",
        ]
    )
    resolution_note = (
        "Resolution summary: Stabilized the service, validated access from impacted "
        "regions, and monitored metrics for 30 minutes with no regressions. "
        "Customer notified of mitigation and next monitoring steps."
    )
    assist = TicketAiAssist(
        ticket_id=ticket.id,
        summary=summary,
        likely_causes=likely_causes,
        next_actions=next_actions,
        resolution_note=resolution_note,
        generated_by_ai=True,
    )
    db.add(assist)
    db.commit()
    db.refresh(assist)
    return assist


@router.get("/{ticket_id}/ai-assist/latest", response_model=TicketAiAssistOut)
def get_latest_ticket_ai_assist(
    ticket_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    assist = (
        db.query(TicketAiAssist)
        .filter(TicketAiAssist.ticket_id == ticket_id)
        .order_by(TicketAiAssist.created_at.desc())
        .first()
    )
    if not assist:
        raise HTTPException(status_code=404, detail="AI assist not found")
    return assist
