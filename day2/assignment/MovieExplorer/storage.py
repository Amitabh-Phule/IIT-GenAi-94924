import json
import pandas as pd
from pathlib import Path

def save_json(data, filename):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved JSON to {filename}")

def save_csv(data, filename):
    df = pd.DataFrame(data)
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved CSV to {filename}")
