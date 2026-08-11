#!/usr/bin/env python3
"""
Pipeline de preprocesamiento de texto para documentos políticos.

Transforma documentos PDF/HTML en texto plano limpio, normaliza
acentos (ñ, á, é, í, ó, ú, ü), tokeniza y detecta idioma español.

Usa spaCy con el modelo es_core_news_md para NLP en español.

Funciones:
    - extract_text_from_pdf: Extrae texto de PDFs con pdfminer.six
    - extract_text_from_html: Extrae texto de HTML con BeautifulSoup
    - clean_text: Limpia boilerplate y normaliza
    - detect_language: Detecta si el texto está en español
    - tokenize: Tokeniza con spaCy
    - preprocess_document: Pipeline completo de preprocesamiento
"""
import logging
import re
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Carga diferida de spaCy para evitar import cost en tests
_nlp = None


def _get_nlp():
    """Carga el modelo de spaCy de forma diferida."""
    global _nlp
    if _nlp is None:
        import spacy
        try:
            _nlp = spacy.load("es_core_news_md")
        except OSError:
            logger.warning(
                "Modelo es_core_news_md no encontrado. "
                "Instalar con: python -m spacy download es_core_news_md"
            )
            _nlp = spacy.blank("es")
    return _nlp


def extract_text_from_pdf(filepath: str | Path) -> str:
    """
    Extrae texto de un archivo PDF usando pdfminer.six.

    Args:
        filepath: Ruta al archivo PDF.

    Returns:
        Texto extraído del PDF.
    """
    from pdfminer.high_level import extract_text

    try:
        text = extract_text(str(filepath))
        logger.info(f"PDF procesado: {filepath} ({len(text)} caracteres)")
        return text
    except Exception as e:
        logger.error(f"Error procesando PDF {filepath}: {e}")
        return ""


def extract_text_from_html(filepath: str | Path) -> str:
    """
    Extrae texto de un archivo HTML usando BeautifulSoup.

    Elimina scripts, estilos y elementos de navegación (boilerplate).

    Args:
        filepath: Ruta al archivo HTML.

    Returns:
        Texto limpio extraído del HTML.
    """
    content = Path(filepath).read_bytes()
    soup = BeautifulSoup(content, "html.parser")

    # Eliminar elementos no textuales
    for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # Extraer texto
    text = soup.get_text(separator="\n", strip=True)

    logger.info(f"HTML procesado: {filepath} ({len(text)} caracteres)")
    return text


def clean_text(text: str) -> str:
    """
    Limpia texto removiendo boilerplate y normalizando.

    Operaciones:
        - Elimina caracteres de control
        - Normaliza espacios y saltos de línea
        - Preserva acentos (ñ, á, é, í, ó, ú, ü)
        - Elimina URLs y emails
        - Normaliza comillas y guiones

    Args:
        text: Texto crudo.

    Returns:
        Texto limpio.
    """
    if not text:
        return ""

    # Eliminar URLs
    text = re.sub(r"https?://\S+", "", text)
    # Eliminar emails
    text = re.sub(r"\S+@\S+\.\S+", "", text)
    # Eliminar caracteres de control (preserva ñ y acentos)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)
    # Normalizar comillas tipográficas
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    # Normalizar guiones
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    # Normalizar espacios múltiples
    text = re.sub(r"[ \t]+", " ", text)
    # Normalizar saltos de línea múltiples
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip
    text = text.strip()

    return text


def detect_language(text: str) -> str:
    """
    Detecta el idioma del texto.

    Usa heurísticas simples basadas en stopwords españolas.
    Retorna 'es' para español, 'other' para otros idiomas.

    Args:
        text: Texto a analizar.

    Returns:
        Código de idioma ('es' o 'other').
    """
    if not text or len(text.strip()) < 50:
        return "es"  # Asumir español para textos cortos

    # Stopwords comunes en español
    spanish_indicators = {
        "de", "la", "que", "el", "en", "y", "a", "los", "se", "del",
        "las", "un", "por", "con", "no", "una", "su", "para", "es",
        "al", "lo", "como", "más", "o", "pero", "sus", "le", "ya",
        "o", "este", "sí", "porque", "esta", "entre", "cuando", "muy",
        "sin", "sobre", "también", "me", "hasta", "hay", "donde", "quien",
    }

    words = set(text.lower().split())
    overlap = words & spanish_indicators
    ratio = len(overlap) / max(len(spanish_indicators), 1)

    return "es" if ratio > 0.15 else "other"


def tokenize(text: str, remove_stopwords: bool = False, remove_punct: bool = True) -> list[str]:
    """
    Tokeniza texto usando spaCy.

    Args:
        text: Texto a tokenizar.
        remove_stopwords: Si True, remueve stopwords.
        remove_punct: Si True, remueve puntuación.

    Returns:
        Lista de tokens (lemas).
    """
    nlp = _get_nlp()
    doc = nlp(text)

    tokens = []
    for token in doc:
        if remove_punct and token.is_punct:
            continue
        if remove_stopwords and token.is_stop:
            continue
        # Usar lema para normalizar (ej: "hospitales" -> "hospital")
        lemma = token.lemma_.lower().strip()
        if lemma:
            tokens.append(lemma)

    return tokens


def extract_entities(text: str) -> list[dict]:
    """
    Extrae entidades nombradas usando NER de spaCy.

    Args:
        text: Texto a analizar.

    Returns:
        Lista de entidades con texto, etiqueta y posición.
    """
    nlp = _get_nlp()
    doc = nlp(text)

    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
        })

    return entities


def preprocess_document(
    filepath: str | Path,
    filter_spanish: bool = True,
    remove_stopwords: bool = False,
) -> dict:
    """
    Pipeline completo de preprocesamiento de un documento.

    Args:
        filepath: Ruta al archivo (PDF o HTML).
        filter_spanish: Si True, filtra documentos que no estén en español.
        remove_stopwords: Si True, remueve stopwords al tokenizar.

    Returns:
        Diccionario con:
            - text: texto limpio
            - tokens: lista de tokens
            - entities: entidades nombradas
            - language: idioma detectado
            - file_path: ruta del archivo original
    """
    filepath = Path(filepath)

    # 1. Extraer texto según formato
    if filepath.suffix.lower() == ".pdf":
        raw_text = extract_text_from_pdf(filepath)
    elif filepath.suffix.lower() in (".html", ".htm"):
        raw_text = extract_text_from_html(filepath)
    elif filepath.suffix.lower() == ".txt":
        raw_text = filepath.read_text(encoding="utf-8", errors="ignore")
    else:
        logger.warning(f"Formato no soportado: {filepath.suffix}")
        raw_text = ""

    # 2. Limpiar texto
    clean = clean_text(raw_text)

    if not clean:
        return {
            "text": "",
            "tokens": [],
            "entities": [],
            "language": "unknown",
            "file_path": str(filepath),
        }

    # 3. Detectar idioma
    lang = detect_language(clean)

    if filter_spanish and lang != "es":
        logger.info(f"Documento filtrado (no español): {filepath}")
        return {
            "text": clean,
            "tokens": [],
            "entities": [],
            "language": lang,
            "file_path": str(filepath),
        }

    # 4. Tokenizar
    tokens = tokenize(clean, remove_stopwords=remove_stopwords)

    # 5. Extraer entidades
    entities = extract_entities(clean)

    return {
        "text": clean,
        "tokens": tokens,
        "entities": entities,
        "language": lang,
        "file_path": str(filepath),
    }
