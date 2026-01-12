from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Ticket
from ..schemas import TicketOut
from ..auth import get_current_user

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/", response_model=list[TicketOut])
def list_tickets(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return db.query(Ticket).order_by(Ticket.created_at.desc()).all()
