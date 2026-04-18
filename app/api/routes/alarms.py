from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

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


@router.get("")
def get_alarms(
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    severity: str | None = Query(None),
    tag: str | None = Query(None),
    limit: int = Query(50),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    return filter_alarms(db, start_date, end_date, severity, tag, limit, offset)


@router.get("/top-tags")
def top_tags(limit: int = Query(5), db: Session = Depends(get_db)):
    return get_top_tags_service(db, limit)


@router.get("/by-severity")
def by_severity(db: Session = Depends(get_db)):
    return get_severity_stats(db)