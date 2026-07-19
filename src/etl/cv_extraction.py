from pathlib import Path
from typing import List, Tuple

import spacy

from bs4 import BeautifulSoup

DATA_RAW_CVS = Path("data/raw/cvs")

nlp = spacy.load("es_core_news_md")


def extract_degree_and_experience_from_html(html_text: str) -> Tuple[str, int]:
    """Extrae grado académico y años de experiencia pública usando spaCy y reglas simples."""

    doc = nlp(html_text)

    degree = None
    years_public = 0

    text_lower = html_text.lower()
    if "primaria" in text_lower:
        degree = "primaria"
    elif "secundaria" in text_lower:
        degree = "secundaria"
    elif "tecnico" in text_lower or "tecnologo" in text_lower:
        degree = "tecnico"
    elif "licenciado" in text_lower or "ingeniero" in text_lower or "universidad" in text_lower:
        degree = "universitario"
    elif "maestria" in text_lower or "magister" in text_lower or "phd" in text_lower or "doctorado" in text_lower:
        degree = "posgrado"

    for ent in doc.ents:
        if ent.label_ == "DATE":
            # Placeholder: reglas más sofisticadas para convertir periodos en años
            pass

    return degree or "", years_public


def process_all_cvs() -> None:
    html_files = list(DATA_RAW_CVS.glob("*.html"))
    records = []
    for html_path in html_files:
        with open(html_path, encoding="utf-8") as f:
            html_text = f.read()
        degree, years_public = extract_degree_and_experience_from_html(html_text)
        records.append(
            {
                "source_file": html_path.name,
                "max_degree": degree,
                "years_public_service": years_public,
            }
        )

    # Aquí se podrían unir estos registros con una tabla de candidatos


if __name__ == "__main__":
    process_all_cvs()
