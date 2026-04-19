from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

# Importar  clases
from app.schemas.alarm_schema import AlarmListResponse
from app.schemas.alarm_schema import TagCountResponse
from app.schemas.alarm_schema import SeverityCountResponse

from app.db.database import SessionLocal
from app.services.alarm_service import (
    filter_alarms,
    get_top_tags_service,
    get_severity_stats
)

router = APIRouter(prefix="/alarms", tags=["Alarms"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint Principal
@router.get("", response_model=AlarmListResponse)
def get_alarms(
    start_date: datetime  | None = Query(None),
    end_date: datetime  | None = Query(None),
    severity: str | None = Query(None),
    tag: str | None = Query(None),
    limit: int = Query(50),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    return filter_alarms(db, start_date, end_date, severity, tag, limit, offset)

# Endpoint Top Tags
@router.get("/top-tags", response_model=List[TagCountResponse])
def top_tags(limit: int = Query(5), db: Session = Depends(get_db)):
    return get_top_tags_service(db, limit)


# Endpoint Severity
@router.get("/by-severity", response_model=List[SeverityCountResponse])
def by_severity(db: Session = Depends(get_db)):
    return get_severity_stats(db)