from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.train_models import train_and_save


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default=None, help="Optional dataset path. Defaults to data/raw/sample_reviews.csv")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit for large datasets")
    parser.add_argument("--no-db", action="store_true", help="Skip SQL database loading")
    args = parser.parse_args()
    summary = train_and_save(dataset_path=args.dataset, limit=args.limit, load_db=not args.no_db)
    print(summary)


if __name__ == "__main__":
    main()
