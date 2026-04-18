from sqlalchemy import Column, Integer, String, DateTime, Float
from app.db.database import Base

class Alarm(Base):
    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    tag = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    message = Column(String)
    value = Column(Float)