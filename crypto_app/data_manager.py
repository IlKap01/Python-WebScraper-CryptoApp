# -*- coding: utf-8 -*-
import os
import pandas as pd
import csv

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CSV_FILE = os.path.join(DATA_DIR, "crypto_data.csv")

def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def save_data(df: pd.DataFrame):
    """Append χωρίς να σβήνει τα παλιά."""
    _ensure_dir()
    exists = os.path.exists(CSV_FILE)
    cols = ["Date","Name","Price","Change_24h","Change_7d","MarketCap","Volume_24h"]
    df = df.reindex(columns=cols)
    df.to_csv(CSV_FILE, mode="a", header=not exists, index=False, quoting=csv.QUOTE_MINIMAL)

def load_data() -> pd.DataFrame:
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=["Date","Name","Price","Change_24h","Change_7d","MarketCap","Volume_24h"])
    return pd.read_csv(CSV_FILE)

