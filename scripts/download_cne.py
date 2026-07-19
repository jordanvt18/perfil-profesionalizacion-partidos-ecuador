from pathlib import Path
from typing import List

import requests

DATA_RAW_CNE = Path("data/raw/cne")


def download_cne_files(urls: List[str], date_tag: str) -> None:
    """Descarga actas y resultados del CNE y guarda en data/raw/cne/<fecha>."""

    target_dir = DATA_RAW_CNE / date_tag
    target_dir.mkdir(parents=True, exist_ok=True)

    for url in urls:
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        filename = url.split("/")[-1] or "cne_file"
        with open(target_dir / filename, "wb") as f:
            f.write(resp.content)


if __name__ == "__main__":
    example_urls = []  # Rellenar manualmente con URLs oficiales del CNE
    download_cne_files(example_urls, date_tag="2026-07-19")
