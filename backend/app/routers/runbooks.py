from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Runbook, RunbookAiAssist
from ..schemas import RunbookOut, RunbookCreate, RunbookAiAssistOut
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


@router.post("/{runbook_id}/ai-assist", response_model=RunbookAiAssistOut, status_code=201)
def generate_runbook_ai_assist(
    runbook_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    runbook = db.query(Runbook).filter(Runbook.id == runbook_id).first()
    if not runbook:
        raise HTTPException(status_code=404, detail="Runbook not found")
    pre_check = "\n".join(
        [
            f"Confirm change approvals for {runbook.client} at {runbook.site}.",
            f"Verify backups and rollback artifacts for {runbook.version}.",
            "Notify stakeholders and ensure monitoring dashboards are ready.",
        ]
    )
    steps = "\n".join(
        [
            f"Announce the {runbook.window} window and begin deployment.",
            f"Deploy {runbook.version} to {runbook.site} and validate smoke tests.",
            "Monitor error rates and latency for at least 15 minutes.",
        ]
    )
    rollback = "\n".join(
        [
            "Trigger rollback if validation fails or error rates exceed thresholds.",
            "Restore previous version and confirm critical workflows recover.",
            "Document rollback timing and notify stakeholders.",
        ]
    )
    validation = "\n".join(
        [
            "Confirm key dashboards are green and alerting is stable.",
            "Validate customer-facing workflows with a test account.",
            "Capture post-change metrics for the runbook record.",
        ]
    )
    client_email = (
        f"Subject: {runbook.project_type} update for {runbook.client}\n\n"
        "Hi team,\n\n"
        f"We completed the {runbook.project_type.lower()} for {runbook.site} "
        f"({runbook.version}) within the {runbook.window} window. "
        "All validation checks are passing and monitoring looks stable. "
        "Please let us know if you notice any issues.\n\n"
        "Regards,\nEAGLE SupportOps"
    )
    assist = RunbookAiAssist(
        runbook_id=runbook.id,
        pre_check=pre_check,
        steps=steps,
        rollback=rollback,
        validation=validation,
        client_email=client_email,
        generated_by_ai=True,
    )
    db.add(assist)
    db.commit()
    db.refresh(assist)
    return assist


@router.get("/{runbook_id}/ai-assist/latest", response_model=RunbookAiAssistOut)
def get_latest_runbook_ai_assist(
    runbook_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    assist = (
        db.query(RunbookAiAssist)
        .filter(RunbookAiAssist.runbook_id == runbook_id)
        .order_by(RunbookAiAssist.created_at.desc())
        .first()
    )
    if not assist:
        raise HTTPException(status_code=404, detail="AI assist not found")
    return assist
