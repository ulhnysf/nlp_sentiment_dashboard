from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data_loader import load_reviews, save_processed_dataset
from src.database import load_reviews_to_db


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean the review dataset and load it into SQL.")
    parser.add_argument("--dataset", type=str, default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--no-db", action="store_true")
    args = parser.parse_args()
    df = load_reviews(args.dataset, limit=args.limit)
    path = save_processed_dataset(df)
    print(f"Processed dataset saved to {path} ({len(df)} rows).")
    if not args.no_db:
        count = load_reviews_to_db(df)
        print(f"Loaded {count} rows into SQL reviews table.")


if __name__ == "__main__":
    main()
