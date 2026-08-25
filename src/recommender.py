"""
recommender.py
--------------
Item-item collaborative filtering baseline on the movie ratings table.
Runs locally on a sampled slice so the notebook / research narrative in the
paper can be reproduced without a Hadoop cluster.

Usage:
    python recommender.py --ratings data/ratings.csv \
                          --user 42 --top 10
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def build_matrix(ratings: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    # Keep the analysis tractable: keep films with ≥ 50 ratings and users with ≥ 20.
    movie_counts = ratings["Movie_Name"].value_counts()
    user_counts = ratings["User_Id"].value_counts()
    keep_movies = movie_counts[movie_counts >= 50].index
    keep_users = user_counts[user_counts >= 20].index
    ratings = ratings[
        ratings["Movie_Name"].isin(keep_movies) & ratings["User_Id"].isin(keep_users)
    ]
    pivot = ratings.pivot_table(
        index="User_Id", columns="Movie_Name", values="Rating"
    ).fillna(0.0)
    movie_pop = ratings.groupby("Movie_Name")["Rating"].count()
    return pivot, movie_pop


def recommend(pivot: pd.DataFrame, user_id: int, top: int = 10) -> list[str]:
    if user_id not in pivot.index:
        return []
    sim = cosine_similarity(pivot.T)
    sim_df = pd.DataFrame(sim, index=pivot.columns, columns=pivot.columns)
    watched = pivot.loc[user_id]
    scores = sim_df.dot(watched)
    scores = scores.drop(index=watched[watched > 0].index, errors="ignore")
    return scores.sort_values(ascending=False).head(top).index.tolist()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ratings", type=Path, required=True)
    p.add_argument("--user", type=int, required=True)
    p.add_argument("--top", type=int, default=10)
    args = p.parse_args()

    ratings = pd.read_csv(args.ratings)
    pivot, _ = build_matrix(ratings)
    picks = recommend(pivot, args.user, args.top)

    if not picks:
        print(f"User {args.user} not found in the filtered matrix.")
        return
    print(f"Top {len(picks)} recommendations for user {args.user}:")
    for i, title in enumerate(picks, 1):
        print(f"  {i:2d}. {title}")


if __name__ == "__main__":
    main()
