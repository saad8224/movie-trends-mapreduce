#!/usr/bin/env bash
# ---------------------------------------------------------
# Submit the average-rating job to Hadoop Streaming.
# Adjust HADOOP_STREAMING_JAR and paths for your cluster.
# ---------------------------------------------------------
set -euo pipefail

HADOOP_STREAMING_JAR=${HADOOP_STREAMING_JAR:-/usr/lib/hadoop-mapreduce/hadoop-streaming.jar}
INPUT=${INPUT:-/user/hadoop/movies/ratings.csv}
OUTPUT=${OUTPUT:-/user/hadoop/movies/output_avg}

hadoop fs -rm -r -f "$OUTPUT"

hadoop jar "$HADOOP_STREAMING_JAR" \
  -files src/mapper.py,src/reducer.py \
  -mapper  "python3 mapper.py"  \
  -reducer "python3 reducer.py" \
  -input   "$INPUT"             \
  -output  "$OUTPUT"

echo "Result written to $OUTPUT"
