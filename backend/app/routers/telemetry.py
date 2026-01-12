from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import TelemetryMetric
from ..schemas import TelemetryMetricOut
from ..auth import get_current_user

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.get("/", response_model=list[TelemetryMetricOut])
def list_metrics(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return db.query(TelemetryMetric).order_by(TelemetryMetric.captured_at.desc()).all()
