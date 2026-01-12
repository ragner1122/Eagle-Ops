from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Runbook
from ..schemas import RunbookOut
from ..auth import get_current_user

router = APIRouter(prefix="/runbooks", tags=["runbooks"])


@router.get("/", response_model=list[RunbookOut])
def list_runbooks(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return db.query(Runbook).all()
