from pathlib import Path
from typing import List

import pandas as pd
from rapidfuzz import fuzz, process

DATA_RAW_CNE = Path("data/raw/cne")
DATA_RAW_CVS = Path("data/raw/cvs")
DATA_PROCESSED = Path("data/processed")


def normalize_party_names(df: pd.DataFrame, party_column: str, canonical_parties: List[str]) -> pd.DataFrame:
    """Normaliza nombres de partidos usando fuzzy matching contra una lista canónica."""

    def match_party(name: str) -> str:
        if pd.isna(name) or not str(name).strip():
            return None
        match, score, _ = process.extractOne(name, canonical_parties, scorer=fuzz.WRatio)
        return match if score >= 80 else name

    df[party_column + "_normalized"] = df[party_column].apply(match_party)
    return df


def compute_professionalization_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula score_academico, score_experiencia e índice de profesionalización por candidato."""

    degree_map = {
        "primaria": 10,
        "secundaria": 30,
        "tecnico": 50,
        "tecnologo": 50,
        "universitario": 70,
        "licenciatura": 70,
        "ingenieria": 70,
        "posgrado": 90,
        "maestria": 90,
        "phd": 90,
    }

    def map_degree(degree: str) -> int:
        if pd.isna(degree):
            return 0
        key = str(degree).strip().lower()
        return degree_map.get(key, 0)

    df["score_academico"] = df["max_degree"].apply(map_degree).clip(lower=0, upper=100)
    df["score_experiencia"] = (df["years_public_service"] * 2).clip(lower=0, upper=40)
    df["profesionalizacion"] = 0.6 * df["score_academico"] + 0.4 * df["score_experiencia"]
    df["profesionalizacion"] = df["profesionalizacion"].clip(lower=0, upper=100)
    return df


def aggregate_by_party_province(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega profesionalización media por partido y provincia."""

    group_cols = ["party_normalized", "province"]
    agg_df = (
        df.groupby(group_cols)
        .agg(
            profesionalizacion_media=("profesionalizacion", "mean"),
            n_candidates=("candidate_id", "count"),
        )
        .reset_index()
    )
    return agg_df


if __name__ == "__main__":
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    # Placeholder: carga de candidatos ya unificada
    candidates_path = DATA_PROCESSED / "candidates.parquet"
    if candidates_path.exists():
        df_candidates = pd.read_parquet(candidates_path)
        df_candidates = compute_professionalization_scores(df_candidates)
        df_candidates.to_parquet(DATA_PROCESSED / "candidates_with_scores.parquet", index=False)

        agg = aggregate_by_party_province(df_candidates)
        agg.to_parquet(DATA_PROCESSED / "agg_party_province.parquet", index=False)
