#!/usr/bin/env python3
"""
genre_reducer.py
----------------
Sums genre counts emitted by genre_mapper.py.
"""
from __future__ import annotations

import sys


def main() -> None:
    current = None
    count = 0
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            continue
        try:
            genre, one = line.split("\t", 1)
            count_in = int(one)
        except ValueError:
            continue
        if genre != current:
            if current is not None:
                print(f"{current}\t{count}")
            current = genre
            count = 0
        count += count_in
    if current is not None:
        print(f"{current}\t{count}")


if __name__ == "__main__":
    main()
