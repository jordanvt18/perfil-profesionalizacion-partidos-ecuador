#!/usr/bin/env python3
"""
Ingesta de programas de gobierno desde fuentes PDF y HTML.

Descarga documentos de planes de gobierno de partidos políticos,
guarda los archivos crudos en data/raw/programs/<partido>/<fecha>/
y registra metadatos de fuente y fecha de scrape.

Respeta robots.txt y aplica rate-limiting entre peticiones.

Uso:
    python scripts/ingest_programs.py --url https://example.com/plan.pdf --partido "RC5"
    python scripts/ingest_programs.py --config sources.yaml
"""
import argparse
import hashlib
import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Constantes
RAW_DIR = Path("data/raw/programs")
DEFAULT_DELAY = 2.0  # segundos entre peticiones
TIMEOUT = 30
USER_AGENT = (
    "CongruenciaMapBot/1.0 (Ecuador Elections Research; +mailto:research@example.org)"
)
HEADERS = {"User-Agent": USER_AGENT}


def check_robots_txt(url: str) -> bool:
    """Verifica si el bot puede acceder a la URL según robots.txt."""
    parsed = urlparse(url)
    robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        return rp.can_fetch(USER_AGENT, url)
    except Exception as e:
        logger.warning(f"No se pudo leer robots.txt de {robots_url}: {e}")
        return True  # Si no hay robots.txt, se asume permitido


def rate_limit(delay: float, last_request_time: list):
    """Aplica rate-limiting entre peticiones para ser cortés."""
    if last_request_time[0] is not None:
        elapsed = time.time() - last_request_time[0]
        if elapsed < delay:
            time.sleep(delay - elapsed)
    last_request_time[0] = time.time()


def download_content(url: str, delay: float = DEFAULT_DELAY) -> bytes | None:
    """
    Descarga el contenido de una URL respetando rate-limiting y robots.txt.

    Args:
        url: URL del recurso a descargar.
        delay: Segundos de espera entre peticiones.

    Returns:
        Contenido binario del recurso o None si falla.
    """
    if not check_robots_txt(url):
        logger.warning(f"robots.txt prohíbe el acceso a: {url}")
        return None

    last_request_time = [None]
    rate_limit(delay, last_request_time)

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        logger.info(f"Descargado: {url} ({len(resp.content)} bytes)")
        return resp.content
    except requests.RequestException as e:
        logger.error(f"Error descargando {url}: {e}")
        return None


def detect_content_type(content: bytes, url: str) -> str:
    """Detecta si el contenido es PDF o HTML."""
    if content[:4] == b"%PDF":
        return "pdf"
    if url.lower().endswith(".pdf"):
        return "pdf"
    # Intentar parsear como HTML
    try:
        BeautifulSoup(content, "html.parser")
        return "html"
    except Exception:
        return "unknown"


def save_raw(content: bytes, url: str, partido: str, content_type: str) -> Path:
    """
    Guarda el contenido crudo en data/raw/programs/<partido>/<fecha>/.

    Args:
        content: Contenido binario.
        url: URL fuente.
        partido: Nombre del partido político.
        content_type: 'pdf' o 'html'.

    Returns:
        Ruta al archivo guardado.
    """
    fecha = datetime.now(timezone.utc).strftime("%Y%m%d")
    ext = "pdf" if content_type == "pdf" else "html"
    # Generar nombre de archivo basado en hash de URL para evitar duplicados
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    filename = f"{partido}_{url_hash}.{ext}"

    out_dir = RAW_DIR / _sanitize(partido) / fecha
    out_dir.mkdir(parents=True, exist_ok=True)

    filepath = out_dir / filename
    filepath.write_bytes(content)

    # Guardar metadatos
    meta = {
        "source_url": url,
        "scrape_date": datetime.now(timezone.utc).isoformat(),
        "partido": partido,
        "content_type": content_type,
        "file_path": str(filepath),
        "file_size": len(content),
    }
    meta_path = out_dir / f"{filepath.stem}_meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    logger.info(f"Guardado: {filepath}")
    return filepath


def _sanitize(name: str) -> str:
    """Sanitiza un nombre para usar como directorio."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)


def extract_links_from_html(content: bytes, base_url: str) -> list[str]:
    """Extrae enlaces a PDFs desde una página HTML."""
    soup = BeautifulSoup(content, "html.parser")
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(base_url, href)
        if full_url.lower().endswith(".pdf"):
            links.append(full_url)
    return links


def ingest_url(url: str, partido: str, delay: float = DEFAULT_DELAY) -> Path | None:
    """
    Descarga y guarda un documento de programa de gobierno.

    Args:
        url: URL del documento (PDF o HTML).
        partido: Nombre del partido político.
        delay: Segundos entre peticiones.

    Returns:
        Ruta al archivo guardado o None si falla.
    """
    content = download_content(url, delay)
    if content is None:
        return None

    content_type = detect_content_type(content, url)

    if content_type == "unknown":
        logger.warning(f"Tipo de contenido no reconocido para: {url}")
        return None

    filepath = save_raw(content, url, partido, content_type)

    # Si es HTML, buscar PDFs enlazados
    if content_type == "html":
        links = extract_links_from_html(content, url)
        if links:
            logger.info(f"Encontrados {len(links)} PDFs enlazados en {url}")
            for pdf_url in links:
                pdf_content = download_content(pdf_url, delay)
                if pdf_content:
                    save_raw(pdf_content, pdf_url, partido, "pdf")

    return filepath


def ingest_from_config(config_path: str):
    """
    Ingesta múltiples URLs desde un archivo YAML de configuración.

    Formato esperado:
        sources:
          - url: https://...
            partido: "RC5"
          - url: https://...
            partido: "PSC"
    """
    import yaml

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    sources = config.get("sources", [])
    logger.info(f"Procesando {len(sources)} fuentes desde {config_path}")

    for source in sources:
        url = source["url"]
        partido = source.get("partido", "Unknown")
        delay = source.get("delay", DEFAULT_DELAY)
        ingest_url(url, partido, delay)


def main():
    parser = argparse.ArgumentParser(
        description="Ingesta de programas de gobierno desde PDF/HTML"
    )
    parser.add_argument("--url", help="URL del documento a descargar")
    parser.add_argument("--partido", help="Nombre del partido político")
    parser.add_argument("--config", help="Archivo YAML con lista de fuentes")
    parser.add_argument(
        "--delay", type=float, default=DEFAULT_DELAY, help="Delay entre peticiones (s)"
    )
    args = parser.parse_args()

    if args.config:
        ingest_from_config(args.config)
    elif args.url and args.partido:
        ingest_url(args.url, args.partido, args.delay)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
