import os
import json
import sqlite3
import pandas as pd
from typing import Dict, Any


def load_csv(path: str) -> pd.DataFrame:
    if not path or not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


def load_json(path: str) -> Dict[str, Any]:
    if not path or not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def load_sqlite(path: str, query: str) -> pd.DataFrame:
    if not path or not os.path.exists(path):
        return pd.DataFrame()
    conn = sqlite3.connect(path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
