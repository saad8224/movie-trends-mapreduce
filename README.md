# Analyzing Movie Trends and Building Recommendations Using MapReduce

Big-data assignment applying **Hadoop Streaming (MapReduce)** to the Large Movie Dataset to compute average ratings, rank genre popularity, and build an item-item collaborative filtering recommender that runs both locally and on a cluster.

## Dataset

- **Source** — [Kaggle: MovieLens 25M / Large Movie Dataset](https://www.kaggle.com/datasets/prajitdatta/movielens-100k-dataset) (or MovieLens 25M for the full ~25M rating rows)
- **Fields used** — `User_Id`, `Movie_Name`, `Rating`, `Genre`
- **Scale** — millions of ratings across thousands of films

Place the ratings CSV at `data/ratings.csv` before running.

## What the Jobs Do

### Job 1 — Average rating per movie
```
mapper.py         →  <title>\t<rating>
sort              →  keys grouped
reducer.py        →  <title>\t<avg_rating>\t<num_ratings>
```

### Job 2 — Genre frequency
```
genre_mapper.py   →  <genre>\t1
sort              →  keys grouped
genre_reducer.py  →  <genre>\t<count>
```

### Job 3 — Item-item collaborative filtering (local, `recommender.py`)
Filters the ratings matrix (≥ 50 ratings per movie, ≥ 20 ratings per user), builds a cosine-similarity matrix over movies, and returns the top-N recommendations for a given user.

## How to Run

### Local Streaming Simulation (no Hadoop required)

```bash
bash src/run_local.sh data/ratings.csv reports/avg_ratings.tsv
```

The script emulates Hadoop by piping the mapper output through `sort` before feeding the reducer — exactly what Hadoop does between the shuffle and reduce phases.

### On a Hadoop Cluster

```bash
export HADOOP_STREAMING_JAR=/path/to/hadoop-streaming.jar
export INPUT=/user/hadoop/movies/ratings.csv
export OUTPUT=/user/hadoop/movies/output_avg
bash src/run_hadoop.sh
```

### Recommender

```bash
pip install -r requirements.txt
python src/recommender.py --ratings data/ratings.csv --user 42 --top 10
```

## Findings From the Paper

- **Top-rated movies** cluster at 5.0 averages but are typically obscure titles with few ratings — classic long-tail behaviour.
- **Most-rated titles** are the cultural staples: *Forrest Gump*, *The Shawshank Redemption*, *Pulp Fiction*, *The Silence of the Lambs*, *The Matrix*.
- **Genre popularity** rank order: Drama > Comedy > Action > Thriller > Adventure > Romance > Sci-Fi > Crime > Fantasy > Children.
- **Rating distribution** — most averages fall between 3.0 and 4.0, with a fat tail of niche films at the extremes.
- **Data-quality outcome** — mapper's stderr channel catches malformed rows without failing the job, which is critical at scale.

## Why MapReduce Fits Here

- **Scalability** — the same script runs unchanged on a laptop or on a 100-node cluster.
- **Fault tolerance** — Hadoop re-executes failed tasks automatically.
- **Data locality** — computation moves to the block; large ratings CSVs don't fly across the network.
- **Simplicity** — mapper and reducer are pure Python stdin/stdout scripts; nothing framework-specific to learn.

## Repository Layout

```
06-movie-trends-mapreduce/
├── README.md
├── requirements.txt
├── src/
│   ├── mapper.py          / reducer.py       ← Job 1: average rating
│   ├── genre_mapper.py    / genre_reducer.py ← Job 2: genre frequency
│   ├── recommender.py                        ← Item-item CF baseline
│   ├── run_local.sh                          ← test without Hadoop
│   └── run_hadoop.sh                         ← real cluster
├── data/                     (gitignored; ratings CSV goes here)
└── reports/
    └── Saad_Salman_Big_Data_Assignment.docx
```

---

*Course:* Big Data (MapReduce / Hadoop)
*Tools:* Python 3, Hadoop Streaming
*Author:* Saad Salman
