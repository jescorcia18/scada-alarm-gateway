from fastapi import FastAPI
from app.db.database import engine, Base
from app.api.routes.alarms import router as alarms_router

app = FastAPI(title="SCADA Alarm Gateway API")

Base.metadata.create_all(bind=engine)

app.include_router(alarms_router)


@app.get("/")
def home():
    return {"message": "SCADA API funcionando"}