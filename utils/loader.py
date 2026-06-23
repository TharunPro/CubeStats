import pandas as pd
import io

def load_solves(file) -> pd.DataFrame:
    raw = file if isinstance(file, bytes) else file.read()
    sample = raw[:500].decode("utf-8", errors="ignore")
    sep = ";" if ";" in sample else ","
    df = pd.read_csv(io.BytesIO(raw), sep=sep, skiprows=0)
    df.columns = ["no", "time", "comment", "scramble", "date", "penalty"]
    df = df[~df["time"].str.startswith("DNF")].copy()
    df["seconds"] = df["time"].apply(parse_time)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)

def parse_time(t: str) -> float:
    t = str(t).replace("+", "")
    parts = t.split(":")
    if len(parts) == 2:
        return float(parts[0]) * 60 + float(parts[1])
    return float(parts[0])
