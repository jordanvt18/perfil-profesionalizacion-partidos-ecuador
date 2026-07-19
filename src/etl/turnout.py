from pathlib import Path
from typing import List

import pandas as pd

DATA_PROCESSED = Path("data/processed")


def compute_turnout_delta(turnout_df: pd.DataFrame) -> pd.DataFrame:
    """Calcula delta de participación entre último año y promedio histórico por provincia/cantón."""

    last_year = turnout_df["year"].max()
    historical = turnout_df[turnout_df["year"] < last_year]

    hist_mean = (
        historical.groupby(["province", "canton"])["turnout"].mean().reset_index(name="turnout_mean_hist")
    )
    last = turnout_df[turnout_df["year"] == last_year][["province", "canton", "turnout"]]
    merged = last.merge(hist_mean, on=["province", "canton"], how="left")
    merged["delta_participacion"] = merged["turnout"] - merged["turnout_mean_hist"]
    return merged


def merge_professionalization_with_turnout(
    agg_prof_df: pd.DataFrame, turnout_delta_df: pd.DataFrame
) -> pd.DataFrame:
    """Une profesionalización media por partido/provincia con delta de participación."""

    merged = agg_prof_df.merge(
        turnout_delta_df,
        on="province",
        how="left",
    )
    return merged


if __name__ == "__main__":
    agg_path = DATA_PROCESSED / "agg_party_province.parquet"
    turnout_path = DATA_PROCESSED / "turnout.parquet"
    if agg_path.exists() and turnout_path.exists():
        agg_df = pd.read_parquet(agg_path)
        turnout_df = pd.read_parquet(turnout_path)
        turnout_delta_df = compute_turnout_delta(turnout_df)
        merged = merge_professionalization_with_turnout(agg_df, turnout_delta_df)
        merged.to_parquet(DATA_PROCESSED / "agg_prof_turnout.parquet", index=False)
