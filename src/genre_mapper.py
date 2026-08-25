#!/usr/bin/env python3
"""
genre_mapper.py
---------------
Second MapReduce job — emits `<genre>\t1` per rating so we can count
occurrences across the full ratings table for the paper's "Top 10 Genres"
figure.
"""
from __future__ import annotations

import csv
import sys


def main() -> None:
    reader = csv.reader(sys.stdin)
    header = next(reader, None)
    if not header:
        return
    lower = [c.lower().strip() for c in header]
    if "genre" not in lower:
        print("ERROR: no genre column", file=sys.stderr)
        return
    idx = lower.index("genre")

    for row in reader:
        if len(row) <= idx:
            continue
        # Movies frequently list multiple genres pipe-separated: "Drama|Romance".
        for g in row[idx].split("|"):
            g = g.strip()
            if g:
                print(f"{g}\t1")


if __name__ == "__main__":
    main()
