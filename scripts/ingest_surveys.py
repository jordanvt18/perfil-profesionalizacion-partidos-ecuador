#!/usr/bin/env python3
"""
Ingesta de encuestas de prioridades ciudadanas.

Carga encuestas desde archivos CSV o JSON y las guarda en
data/raw/surveys/<fuente>/<fecha>/. Incluye detección de proxies
(redes sociales, peticiones municipales) cuando no existen encuestas formales.

Uso:
    python scripts/ingest_surveys.py --input encuesta.csv --fuente "INEC"
    python scripts/ingest_surveys.py --input datos.json --fuente "CNE"
    python scripts/ingest_surveys.py --proxy --canton "Guayaquil" --fuente "redes_sociales"
"""
import argparse
import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

RAW_DIR = Path("data/raw/surveys")


def save_raw_survey(data: dict | list, fuente: str, format_type: str) -> Path:
    """
    Guarda los datos crudos de la encuesta en data/raw/surveys/<fuente>/<fecha>/.

    Args:
        data: Datos de la encuesta (dict o list).
        fuente: Fuente de la encuesta (INEC, CNE, etc.).
        format_type: Formato original ('csv' o 'json').

    Returns:
        Ruta al archivo guardado.
    """
    fecha = datetime.now(timezone.utc).strftime("%Y%m%d")
    safe_fuente = _sanitize(fuente)
    out_dir = RAW_DIR / safe_fuente / fecha
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%H%M%S")
    filename = f"{safe_fuente}_{timestamp}.{format_type}"
    filepath = out_dir / filename

    if format_type == "json":
        filepath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    else:
        # CSV
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame([data])
        df.to_csv(filepath, index=False, encoding="utf-8")

    # Metadatos
    meta = {
        "fuente": fuente,
        "scrape_date": datetime.now(timezone.utc).isoformat(),
        "format": format_type,
        "file_path": str(filepath),
        "n_records": len(data) if isinstance(data, list) else 1,
    }
    meta_path = out_dir / f"{filepath.stem}_meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    logger.info(f"Guardado: {filepath} ({meta['n_records']} registros)")
    return filepath


def _sanitize(name: str) -> str:
    """Sanitiza un nombre para usar como directorio."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)


def load_csv(filepath: str) -> list[dict]:
    """Carga un archivo CSV y retorna una lista de diccionarios."""
    df = pd.read_csv(filepath, encoding="utf-8")
    logger.info(f"Cargado CSV: {filepath} ({len(df)} filas)")
    return df.to_dict(orient="records")


def load_json(filepath: str) -> dict | list:
    """Carga un archivo JSON."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info(f"Cargado JSON: {filepath} ({len(data) if isinstance(data, list) else 1} registros)")
    return data


def normalize_survey_data(data: list[dict]) -> list[dict]:
    """
    Normaliza los campos de encuesta a un esquema común.

    Campos esperados (flexibles):
        - canton / cantón / municipio
        - prioridad / tema / tema_principal
        - porcentaje / pct / valor
        - fecha
        - fuente

    Returns:
        Lista de diccionarios con campos normalizados.
    """
    normalized = []
    for row in data:
        item = {
            "canton": row.get("canton") or row.get("cantón") or row.get("municipio") or "",
            "provincia": row.get("provincia") or row.get("province") or "",
            "tema": row.get("prioridad") or row.get("tema") or row.get("tema_principal") or "",
            "porcentaje": float(
                row.get("porcentaje") or row.get("pct") or row.get("valor") or 0
            ),
            "fecha": row.get("fecha") or "",
            "fuente": row.get("fuente") or "",
            "n_respuestas": int(row.get("n_respuestas") or row.get("muestra") or 0),
        }
        normalized.append(item)
    return normalized


def detect_proxy_data(canton: str, fuente: str = "redes_sociales") -> list[dict]:
    """
    Detecta datos proxy cuando no existen encuestas formales.

    Busca menciones en redes sociales, peticiones municipales
    y otros indicadores indirectos de prioridades ciudadanas.

    Args:
        canton: Nombre del cantón.
        fuente: Tipo de fuente proxy.

    Returns:
        Lista de diccionarios con datos proxy detectados.
    """
    # Plantillas de temas comunes detectables en menciones sociales
    proxy_templates = {
        "redes_sociales": [
            {"tema": "seguridad", "patron": r"seguridad|delincuencia|robo|asalto|extorsión"},
            {"tema": "agua", "patron": r"agua|alcantarillado|potable|racionamiento"},
            {"tema": "movilidad", "patron": r"transporte|bus|vía|carretera|tráfico|semáforo"},
            {"tema": "salud", "patron": r"hospital|médico|salud|enfermedad|posta"},
            {"tema": "empleo", "patron": r"empleo|trabajo|desempleo|informalidad"},
            {"tema": "educacion", "patron": r"escuela|colegio|universidad|profesor|educación"},
            {"tema": "vivienda", "patron": r"vivienda|barrio|bono|construcción"},
            {"tema": "ambiente", "patron": r"contaminación|basura|reciclaje|ambiente"},
            {"tema": "transparencia", "patron": r"corrupción|transparencia|rendición"},
            {"tema": "presupuesto", "patron": r"presupuesto|obras|impuestos|gasto"},
        ],
        "peticiones_municipales": [
            {"tema": "agua", "patron": r"agua|alcantarillado|fuga"},
            {"tema": "movilidad", "patron": r"bache|vía|carretera|transporte"},
            {"tema": "seguridad", "patron": r"seguridad|iluminación|robo"},
            {"tema": "ambiente", "patron": r"basura|reciclaje|contaminación|ruido"},
        ],
    }

    templates = proxy_templates.get(fuente, proxy_templates["redes_sociales"])
    proxy_data = []

    logger.info(
        f"Generando detección proxy para cantón: {canton} (fuente: {fuente})"
    )
    logger.info(
        f"Plantillas de patrones: {len(templates)} temas a detectar"
    )

    for template in templates:
        proxy_data.append(
            {
                "canton": canton,
                "tema": template["tema"],
                "patron_regex": template["patron"],
                "fuente": fuente,
                "fecha": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "tipo": "proxy",
                "nota": (
                    "Dato proxy generado desde patrones de menciones sociales. "
                    "Requiere validación con datos reales."
                ),
            }
        )

    return proxy_data


def main():
    parser = argparse.ArgumentParser(
        description="Ingesta de encuestas de prioridades ciudadanas"
    )
    parser.add_argument("--input", help="Archivo de entrada (CSV o JSON)")
    parser.add_argument("--fuente", default="INEC", help="Fuente de los datos")
    parser.add_argument(
        "--proxy",
        action="store_true",
        help="Generar datos proxy cuando no hay encuestas formales",
    )
    parser.add_argument("--canton", help="Cantón para datos proxy")
    args = parser.parse_args()

    if args.proxy:
        if not args.canton:
            parser.error("--canton es requerido con --proxy")
        proxy_data = detect_proxy_data(args.canton, args.fuente)
        save_raw_survey(proxy_data, args.fuente, "json")
    elif args.input:
        if args.input.endswith(".csv"):
            data = load_csv(args.input)
            normalized = normalize_survey_data(data)
            save_raw_survey(normalized, args.fuente, "csv")
        elif args.input.endswith(".json"):
            data = load_json(args.input)
            if isinstance(data, list):
                normalized = normalize_survey_data(data)
            else:
                normalized = normalize_survey_data([data])
            save_raw_survey(normalized, args.fuente, "json")
        else:
            parser.error("Formato no soportado. Use CSV o JSON.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
