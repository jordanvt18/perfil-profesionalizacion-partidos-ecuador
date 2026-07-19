from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./perfil_profesionalizacion.db")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="Perfil profesionalización partidos Ecuador")


@app.get("/parties")
async def list_parties():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT party_normalized FROM candidates"))
        parties = [row[0] for row in result]
    return {"parties": parties}


@app.get("/candidates")
async def list_candidates(party: str | None = None, province: str | None = None):
    query = "SELECT * FROM candidates WHERE 1=1"
    params = {}
    if party:
        query += " AND party_normalized = :party"
        params["party"] = party
    if province:
        query += " AND province = :province"
        params["province"] = province

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        rows = [dict(row) for row in result.mappings()]
    return {"candidates": rows}


@app.get("/turnout")
async def turnout(year: int, province: str | None = None):
    query = "SELECT * FROM turnout WHERE year = :year"
    params = {"year": year}
    if province:
        query += " AND province = :province"
        params["province"] = province

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        rows = [dict(row) for row in result.mappings()]
    return {"turnout": rows}


@app.get("/aggregates")
async def aggregates(party: str | None = None, province: str | None = None):
    query = "SELECT * FROM agg_party_province WHERE 1=1"
    params = {}
    if party:
        query += " AND party_normalized = :party"
        params["party"] = party
    if province:
        query += " AND province = :province"
        params["province"] = province

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        rows = [dict(row) for row in result.mappings()]
    return {"aggregates": rows}
