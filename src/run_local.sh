#!/usr/bin/env bash
# ---------------------------------------------------------
# Simulate a Hadoop Streaming job on a local machine.
# Pipes CSV → mapper → sort → reducer → output.
# Handy for testing your mapper/reducer before uploading to
# an actual Hadoop / EMR cluster.
# ---------------------------------------------------------
set -euo pipefail

INPUT=${1:-data/ratings.csv}
OUTPUT=${2:-reports/avg_ratings.tsv}

mkdir -p "$(dirname "$OUTPUT")"

python3 src/mapper.py < "$INPUT" \
  | sort -t $'\t' -k1,1 \
  | python3 src/reducer.py \
  > "$OUTPUT"

echo "Wrote $(wc -l < "$OUTPUT") movies → $OUTPUT"
