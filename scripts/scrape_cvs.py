from pathlib import Path
from time import sleep
from typing import List

import requests
from bs4 import BeautifulSoup

DATA_RAW_CVS = Path("data/raw/cvs")


def polite_get(url: str, user_agent: str = "Mozilla/5.0 (compatible; PerfilProfesionalizacionBot/1.0)") -> str:
    headers = {"User-Agent": user_agent}
    resp = requests.get(url, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.text


def scrape_cvs(urls: List[str], delay_seconds: float = 5.0) -> None:
    """Scraper sencillo para CVs públicos con politeness y rate limiting."""

    DATA_RAW_CVS.mkdir(parents=True, exist_ok=True)

    for idx, url in enumerate(urls, start=1):
        html = polite_get(url)
        soup = BeautifulSoup(html, "html.parser")
        filename = f"cv_{idx}.html"
        with open(DATA_RAW_CVS / filename, "w", encoding="utf-8") as f:
            f.write(str(soup))
        sleep(delay_seconds)


if __name__ == "__main__":
    example_urls = []  # Rellenar manualmente con URLs oficiales de CVs
    scrape_cvs(example_urls)
