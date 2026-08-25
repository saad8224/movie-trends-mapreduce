#!/usr/bin/env python3
"""
reducer.py
----------
Hadoop Streaming reducer. Consumes the sorted `<title>\t<rating>` stream
from mapper.py and emits `<title>\t<avg_rating>\t<num_ratings>`.

Because Hadoop guarantees keys arrive sorted, we can aggregate on the fly
without buffering the whole dataset in memory.
"""
from __future__ import annotations

import sys


def main() -> None:
    current_title = None
    total = 0.0
    count = 0

    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            continue
        try:
            title, rating_str = line.split("\t", 1)
            rating = float(rating_str)
        except ValueError:
            continue

        if title != current_title:
            if current_title is not None and count > 0:
                print(f"{current_title}\t{total / count:.4f}\t{count}")
            current_title = title
            total = 0.0
            count = 0

        total += rating
        count += 1

    if current_title is not None and count > 0:
        print(f"{current_title}\t{total / count:.4f}\t{count}")


if __name__ == "__main__":
    main()
