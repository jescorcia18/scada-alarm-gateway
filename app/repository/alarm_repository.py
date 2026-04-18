from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.alarm import Alarm


def get_alarms_query(db: Session):
    return db.query(Alarm)


def get_top_tags(db: Session, limit: int):
    return (
        db.query(
            Alarm.tag,
            func.count(Alarm.id).label("total")
        )
        .group_by(Alarm.tag)
        .order_by(func.count(Alarm.id).desc())
        .limit(limit)
        .all()
    )


def get_alarms_by_severity(db: Session):
    return (
        db.query(
            Alarm.severity,
            func.count(Alarm.id).label("total")
        )
        .group_by(Alarm.severity)
        .all()
    )