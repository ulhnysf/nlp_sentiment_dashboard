from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.database import init_db

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
