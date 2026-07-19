from pathlib import Path

import pandas as pd
import statsmodels.api as sm
from scipy.stats import pearsonr, spearmanr

DATA_PROCESSED = Path("data/processed")


def run_correlations(df: pd.DataFrame):
    x = df["profesionalizacion_media"].values
    y = df["delta_participacion"].values
    pearson_corr, pearson_p = pearsonr(x, y)
    spearman_corr, spearman_p = spearmanr(x, y)
    return {
        "pearson_corr": pearson_corr,
        "pearson_p": pearson_p,
        "spearman_corr": spearman_corr,
        "spearman_p": spearman_p,
    }


def run_regression(df: pd.DataFrame):
    y = df["delta_participacion"]
    X = df[["profesionalizacion_media", "gdp_per_capita", "poverty_rate"]]
    X = sm.add_constant(X)
    model = sm.OLS(y, X, missing="drop").fit()
    return model


if __name__ == "__main__":
    merged_path = DATA_PROCESSED / "agg_prof_turnout_with_inec.parquet"
    if merged_path.exists():
        df = pd.read_parquet(merged_path)
        corr = run_correlations(df)
        print("Correlaciones:", corr)
        model = run_regression(df)
        print(model.summary())
