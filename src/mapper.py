#!/usr/bin/env python3
"""
mapper.py
---------
Hadoop Streaming mapper. Reads one CSV row per stdin line from the
Large Movie Dataset (Kaggle) and emits `<movie_title>\t<rating>` for the
average-rating job.

Malformed rows (missing title or non-numeric rating) are logged to stderr
and skipped; Hadoop counts stderr as job counters, so this doubles as a
data-quality signal.
"""
from __future__ import annotations

import csv
import sys


def main() -> None:
    reader = csv.reader(sys.stdin)
    header = next(reader, None)
    if not header:
        return

    # Locate the columns we need robustly — the Kaggle CSV has many extras.
    lower = [c.lower().strip() for c in header]
    try:
        title_idx = lower.index("movie_name") if "movie_name" in lower else lower.index("title")
    except ValueError:
        print("ERROR: no title column", file=sys.stderr)
        return
    try:
        rating_idx = lower.index("rating")
    except ValueError:
        print("ERROR: no rating column", file=sys.stderr)
        return

    for row in reader:
        if len(row) <= max(title_idx, rating_idx):
            print("MALFORMED ROW", file=sys.stderr)
            continue
        title = row[title_idx].strip()
        if not title:
            continue
        try:
            rating = float(row[rating_idx])
        except ValueError:
            print(f"BAD RATING\t{row[rating_idx]!r}", file=sys.stderr)
            continue
        # tab-separated for Hadoop Streaming
        print(f"{title}\t{rating}")


if __name__ == "__main__":
    main()
