from fastapi import FastAPI, Depends, HTTPException, Query
from app.db.database import engine, Base, SessionLocal

from sqlalchemy import func
from sqlalchemy.orm import Session

from datetime import datetime
from app.models.alarm import Alarm

app = FastAPI(title="SCADA Alarm Gateway API")

# Crea las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "SCADA API funcionando"}

# ---------------------------
# Endpoint 1: Consulta avanzada
# ---------------------------
@app.get("/alarms")
def get_alarms(
    start_date: str | None = Query(None, description="Formato ISO: 2025-04-15T00:00:00"),
    end_date: str | None = Query(None, description="Formato ISO: 2025-04-16T00:00:00"),
    severity: str | None = Query(None),
    tag: str | None = Query(None),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Alarm)

    # 🔹 Validación y filtros de fecha
    try:
        if start_date:
            start = datetime.fromisoformat(start_date)
            query = query.filter(Alarm.timestamp >= start)

        if end_date:
            end = datetime.fromisoformat(end_date)
            query = query.filter(Alarm.timestamp <= end)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato de fecha inválido. Use ISO: YYYY-MM-DDTHH:MM:SS"
        )

    # 🔹 Filtros adicionales
    if severity:
        query = query.filter(Alarm.severity == severity.upper())

    if tag:
        query = query.filter(Alarm.tag == tag)

    # 🔹 Orden recomendado
    query = query.order_by(Alarm.timestamp.desc())

    # 🔹 Paginación
    results = query.offset(offset).limit(limit).all()

    return {
        "count": len(results),
        "limit": limit,
        "offset": offset,
        "data": results
    }

# ---------------------------
# Endpoint 2: Agregación (Top Tags)
# ---------------------------
@app.get("/alarms/top-tags")
def top_tags(
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Alarm.tag,
            func.count(Alarm.id).label("total")
        )
        .group_by(Alarm.tag)
        .order_by(func.count(Alarm.id).desc())
        .limit(limit)
        .all()
    )

    return [
        {"tag": tag, "total": total}
        for tag, total in results
    ]

# ---------------------------
# Endpoint 3: Conteo por severidad
# ---------------------------
@app.get("/alarms/by-severity")
def alarms_by_severity(db: Session = Depends(get_db)):
    results = (
        db.query(
            Alarm.severity,
            func.count(Alarm.id).label("total")
        )
        .group_by(Alarm.severity)
        .all()
    )

    return [
        {"severity": severity, "total": total}
        for severity, total in results
    ]