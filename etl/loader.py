import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:pass@localhost:5432/scada")

df = pd.read_csv("data/processed/clean.csv")

df.to_sql("alarms", engine, if_exists="append", index=False)