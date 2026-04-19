from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlarmResponse(BaseModel):
    id: int
    timestamp: datetime
    tag: str
    severity: str
    message: Optional[str] = None
    value: Optional[float] = None

    class Config:
        from_attributes = True  # equivalente moderno de orm_mode


class AlarmListResponse(BaseModel):
    count: int
    limit: int
    offset: int
    data: list[AlarmResponse]


class TagCountResponse(BaseModel):
    tag: str
    total: int


class SeverityCountResponse(BaseModel):
    severity: str
    total: int