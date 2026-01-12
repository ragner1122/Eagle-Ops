from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Runbook
from ..schemas import RunbookOut, RunbookCreate
from ..auth import get_current_user

router = APIRouter(prefix="/runbooks", tags=["runbooks"])


@router.get("/", response_model=list[RunbookOut])
def list_runbooks(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return db.query(Runbook).all()


@router.post("/", response_model=RunbookOut)
def create_runbook(
    payload: RunbookCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    title = payload.title or f"{payload.project_type} rollout - {payload.client} ({payload.site})"
    runbook = Runbook(
        title=title,
        project_type=payload.project_type,
        client=payload.client,
        site=payload.site,
        version=payload.version,
        window=payload.window,
        rollback_plan_required=payload.rollback_plan_required,
        pre_check=payload.pre_check,
        steps=payload.steps,
        rollback=payload.rollback,
        validation=payload.validation,
        comms=payload.comms,
        owner=user.email,
    )
    db.add(runbook)
    db.commit()
    db.refresh(runbook)
    return runbook


@router.get("/{runbook_id}", response_model=RunbookOut)
def get_runbook(
    runbook_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    runbook = db.query(Runbook).filter(Runbook.id == runbook_id).first()
    if not runbook:
        raise HTTPException(status_code=404, detail="Runbook not found")
    return runbook
