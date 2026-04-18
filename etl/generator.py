import pandas as pd
import random

data = []

for i in range(1000):
    data.append({
        "id": i,
        "timestamp": random.choice([
            "2025-04-15 10:30:00",
            "15/04/2025",
            None
        ]),
        "tag": random.choice(["PUMP", "VALVE", None]),
        "severity": random.choice(["HIGH", "LOW", None]),
        "value": random.choice([10, "error", None])
    })

df = pd.DataFrame(data)
df.to_csv("data/raw/alarms_dirty.csv", index=False)