from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.alarm import Alarm

from app.repository.alarm_repository import (
    get_alarms_query,
    get_top_tags,
    get_alarms_by_severity
)


def filter_alarms(
    db: Session,
    start_date: str,
    end_date: str,
    severity: str,
    tag: str,
    limit: int,
    offset: int
):
    query = get_alarms_query(db)

    # Fechas
    try:
        if start_date:
            query = query.filter(Alarm.timestamp >= start_date)

        if end_date:
            query = query.filter(Alarm.timestamp <= end_date)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato de fecha inválido"
        )

    # Filtros
    if severity:
        query = query.filter_by(severity=severity.upper())

    if tag:
        query = query.filter_by(tag=tag)

    query = query.order_by(
        get_alarms_query(db).column_descriptions[0]['entity'].timestamp.desc()
    )

    results = query.offset(offset).limit(limit).all()

    return {
        "count": len(results),
        "limit": limit,
        "offset": offset,
        "data": results
    }


def get_top_tags_service(db: Session, limit: int):
    results = get_top_tags(db, limit)
    return [{"tag": tag, "total": total} for tag, total in results]


def get_severity_stats(db: Session):
    results = get_alarms_by_severity(db)
    return [{"severity": s, "total": t} for s, t in results]