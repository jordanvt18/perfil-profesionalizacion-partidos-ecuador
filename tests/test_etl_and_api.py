import os
from pathlib import Path

import pytest

from src.etl.professionalization import compute_professionalization_scores
from src.api.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def sample_candidates_df():
  import pandas as pd

  return pd.DataFrame(
      {
          "candidate_id": [1, 2],
          "max_degree": ["universitario", "posgrado"],
          "years_public_service": [5, 10],
          "party_normalized": ["PARTIDO A", "PARTIDO B"],
          "province": ["Guayas", "Pichincha"],
      }
  )


def test_compute_professionalization_scores(sample_candidates_df):
    df = compute_professionalization_scores(sample_candidates_df)
    assert "profesionalizacion" in df.columns
    assert df["profesionalizacion"].between(0, 100).all()


client = TestClient(app)


def test_parties_endpoint(monkeypatch, tmp_path):
    # Crear DB temporal SQLite para pruebas
    db_path = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    from sqlalchemy import create_engine, text

    engine = create_engine(os.environ["DATABASE_URL"], future=True)
    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE TABLE candidates (candidate_id INTEGER, party_normalized TEXT, province TEXT)"
            )
        )
        conn.execute(
            text("INSERT INTO candidates VALUES (1, 'PARTIDO A', 'Guayas'), (2, 'PARTIDO B', 'Pichincha')")
        )

    response = client.get("/parties")
    assert response.status_code == 200
    assert "parties" in response.json()
