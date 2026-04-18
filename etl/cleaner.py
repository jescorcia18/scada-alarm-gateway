import pandas as pd

df = pd.read_csv("data/raw/alarms_dirty.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["value"] = pd.to_numeric(df["value"], errors="coerce")

df = df.dropna(subset=["timestamp", "tag"])

df.to_csv("data/processed/clean.csv", index=False)