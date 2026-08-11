"""API REST para consultar datos de profesionalización de candidatos y partidos."""

import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .congruencia import router as congruencia_router
from .congruencia import flat_router as congruencia_flat_router

app = FastAPI(
    title="Índice de Profesionalización – Ecuador",
    description="API para consultar el índice de profesionalización de candidatos y partidos políticos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_json(filename: str):
    """Carga datos desde data/demo/ o data/processed/."""
    demo_path = Path(f"data/demo/{filename}")
    processed_path = Path(f"data/processed/{filename}")

    path = processed_path if processed_path.exists() else demo_path
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def filter_by(data: list, field: str, value: Optional[str]) -> list:
    if not value:
        return data
    return [d for d in data if d.get(field) == value]


@app.get("/parties")
def list_parties():
    candidates = load_json("candidates.json")
    parties = sorted(set(c["party_normalized"] for c in candidates))
    return {"parties": parties}


@app.get("/provinces")
def list_provinces():
    candidates = load_json("candidates.json")
    provinces = sorted(set(c["provincia"] for c in candidates))
    return {"provinces": provinces}


@app.get("/years")
def list_years():
    turnout = load_json("turnout.json")
    years = sorted(set(t["year"] for t in turnout))
    return {"years": years}


@app.get("/aggregates")
def get_aggregates(
    party: Optional[str] = Query(None),
    province: Optional[str] = Query(None),
):
    data = load_json("aggregates.json")
    data = filter_by(data, "party_normalized", party)
    data = filter_by(data, "province", province)
    return {"aggregates": data}


@app.get("/candidates")
def get_candidates(
    party: Optional[str] = Query(None),
    province: Optional[str] = Query(None),
):
    data = load_json("candidates.json")
    data = filter_by(data, "party_normalized", party)
    data = filter_by(data, "provincia", province)
    return {"candidates": data}


@app.get("/turnout")
def get_turnout(
    year: Optional[int] = Query(None),
    province: Optional[str] = Query(None),
):
    data = load_json("turnout.json")
    if year:
        data = [d for d in data if d["year"] == year]
    data = filter_by(data, "province", province)
    return {"turnout": data}


@app.get("/")
def root():
    return {
        "app": "Índice de Profesionalización de Partidos – Ecuador",
        "endpoints": [
            "/parties", "/provinces", "/years", "/aggregates", "/candidates", "/turnout",
            "/themes", "/canton/{canton_id}/priorities", "/candidate/{candidate_id}/program",
            "/match", "/party/{party_id}/aggregates",
            "/congruencia/map", "/congruencia/ranking", "/congruencia/themes-graph",
        ],
        "docs": "/docs",
    }


app.include_router(congruencia_router)
app.include_router(congruencia_flat_router)

# Montar frontend estático si existe
web_dir = Path("web")
if web_dir.exists():
    app.mount("/static", StaticFiles(directory=str(web_dir)), name="static")
