from datetime import datetime, timedelta
import random

from app.db.database import SessionLocal
from app.models.alarm import Alarm

db = SessionLocal()

tags = ["PUMP_01", "PUMP_02", "VALVE_01", "MOTOR_01"]
severities = ["LOW", "MEDIUM", "HIGH"]

now = datetime.now()

mock_data = []

for i in range(50):
    alarm = Alarm(
        timestamp=now - timedelta(minutes=random.randint(0, 300)),
        tag=random.choice(tags),
        severity=random.choice(severities),
        message=f"Mock alarm {i}",
        value=round(random.uniform(10, 100), 2)
    )
    mock_data.append(alarm)

db.bulk_save_objects(mock_data)
db.commit()
db.close()

print("Datos mock insertados correctamente")