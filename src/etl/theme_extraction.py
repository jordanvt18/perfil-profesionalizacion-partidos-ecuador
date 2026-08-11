#!/usr/bin/env python3
"""
Extracción de temas (theme extraction) mediante NLP.

Carga la taxonomía de temas desde config/themes.yml y aplica:
    - Coincidencia de palabras clave (keyword matching)
    - NER con spaCy para detectar entidades relevantes
    - Scoring ponderado por frecuencia y posición
    - LDA opcional para detección de temas emergentes

Produce vectores de scores por tema para cada documento:
    theme_scores = {tema_id: score 0-1}

Para encuestas: mapea preguntas/respuestas a la misma taxonomía
y calcula priority_scores por cantón.
"""
import logging
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional

import numpy as np

from src.etl.text_preprocessing import tokenize, extract_entities, _get_nlp

logger = logging.getLogger(__name__)

# Cache de taxonomía
_themes_cache: Optional[list[dict]] = None


def load_themes(config_path: str = "config/themes.yml") -> list[dict]:
    """
    Carga la taxonomía de temas desde el archivo YAML.

    Args:
        config_path: Ruta a config/themes.yml.

    Returns:
        Lista de diccionarios con id, name y keywords por tema.
    """
    global _themes_cache
    if _themes_cache is not None:
        return _themes_cache

    import yaml

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    _themes_cache = config.get("themes", [])
    logger.info(f"Cargados {len(_themes_cache)} temas desde {config_path}")
    return _themes_cache


def _normalize_keyword(kw: str) -> str:
    """Normaliza un keyword para matching (lowercase, sin acentos extra)."""
    return kw.lower().strip()


def _build_keyword_index(themes: list[dict]) -> dict[str, str]:
    """
    Construye un índice keyword -> tema_id para búsqueda rápida.

    Args:
        themes: Lista de temas con keywords.

    Returns:
        Diccionario mapeando keyword normalizado -> tema_id.
    """
    index = {}
    for theme in themes:
        for kw in theme.get("keywords", []):
            normalized = _normalize_keyword(kw)
            index[normalized] = theme["id"]
    return index


def keyword_matching(
    text: str,
    themes: list[dict],
    use_lemmatization: bool = True,
) -> dict[str, float]:
    """
    Realiza coincidencia de palabras clave en el texto.

    Args:
        text: Texto del documento.
        themes: Lista de temas con keywords.
        use_lemmatization: Si True, usa lemas de spaCy para matching.

    Returns:
        Diccionario {tema_id: score} con scores entre 0 y 1.
    """
    if not text:
        return {theme["id"]: 0.0 for theme in themes}

    text_lower = text.lower()
    keyword_index = _build_keyword_index(themes)

    # Contar coincidencias por tema
    theme_matches: dict[str, int] = defaultdict(int)
    theme_keywords_found: dict[str, set] = defaultdict(set)

    # Matching por keyword (búsqueda de substring)
    for kw, theme_id in keyword_index.items():
        # Para keywords de múltiples palabras, usar regex
        if " " in kw:
            pattern = re.escape(kw)
            matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
        else:
            matches = text_lower.count(kw)

        if matches > 0:
            theme_matches[theme_id] += matches
            theme_keywords_found[theme_id].add(kw)

    # Matching con lematización si está habilitado
    if use_lemmatization:
        try:
            tokens = tokenize(text, remove_stopwords=True)
            for token in tokens:
                if token in keyword_index:
                    theme_id = keyword_index[token]
                    theme_matches[theme_id] += 1
                    theme_keywords_found[theme_id].add(token)
        except Exception as e:
            logger.warning(f"Error en lematización: {e}")

    # Calcular scores normalizados (0-1)
    # Score = combinación de frecuencia y diversidad de keywords
    scores = {}
    total_matches = sum(theme_matches.values())

    for theme in themes:
        tid = theme["id"]
        freq = theme_matches.get(tid, 0)
        n_keywords_found = len(theme_keywords_found.get(tid, set()))
        n_keywords_total = len(theme.get("keywords", []))

        if total_matches > 0 and freq > 0:
            # Score combina frecuencia relativa y cobertura de keywords
            freq_score = freq / total_matches
            coverage_score = n_keywords_found / max(n_keywords_total, 1)
            # Ponderar: 60% frecuencia, 40% cobertura
            score = 0.6 * freq_score + 0.4 * coverage_score
        else:
            score = 0.0

        scores[tid] = round(min(score, 1.0), 4)

    return scores


def ner_enhanced_scoring(
    text: str,
    theme_scores: dict[str, float],
    themes: list[dict],
) -> dict[str, float]:
    """
    Mejora los scores usando NER de spaCy.

    Detecta entidades nombradas que pueden reforzar temas
    (ej: "Hospital Eugenio Espejo" refuerza el tema "salud").

    Args:
        text: Texto del documento.
        theme_scores: Scores base de keyword matching.
        themes: Lista de temas.

    Returns:
        Scores ajustados con boost de NER.
    """
    try:
        entities = extract_entities(text)
    except Exception as e:
        logger.warning(f"Error en NER: {e}")
        return theme_scores

    # Mapear tipos de entidad a temas
    entity_theme_map = {
        "ORG": ["transparencia", "presupuesto"],
        "LOC": ["ambiente", "agua"],
        "PERSON": ["transparencia"],
        "MONEY": ["presupuesto", "empleo"],
        "LAW": ["transparencia", "seguridad"],
    }

    entity_boosts: dict[str, float] = defaultdict(float)
    for ent in entities:
        ent_text_lower = ent["text"].lower()
        # Verificar si la entidad contiene keywords de algún tema
        for theme in themes:
            for kw in theme.get("keywords", []):
                if _normalize_keyword(kw) in ent_text_lower:
                    entity_boosts[theme["id"]] += 0.05
                    break

        # Boost por tipo de entidad
        for theme_id in entity_theme_map.get(ent["label"], []):
            entity_boosts[theme_id] += 0.02

    # Aplicar boosts (capped a 1.0)
    adjusted = {}
    for tid, base_score in theme_scores.items():
        boost = min(entity_boosts.get(tid, 0), 0.2)  # Máximo boost de 0.2
        adjusted[tid] = round(min(base_score + boost, 1.0), 4)

    return adjusted


def extract_theme_scores(
    text: str,
    config_path: str = "config/themes.yml",
    use_ner: bool = True,
) -> dict[str, float]:
    """
    Extrae scores de temas de un documento de texto.

    Pipeline:
        1. Keyword matching + lematización
        2. NER boost (opcional)
        3. Normalización

    Args:
        text: Texto del documento.
        config_path: Ruta a config/themes.yml.
        use_ner: Si True, aplica boost de NER.

    Returns:
        Diccionario {tema_id: score 0-1}.
    """
    themes = load_themes(config_path)
    scores = keyword_matching(text, themes)
    if use_ner:
        scores = ner_enhanced_scoring(text, scores, themes)
    return scores


def map_survey_to_themes(
    survey_data: list[dict],
    config_path: str = "config/themes.yml",
) -> dict[str, dict[str, float]]:
    """
    Mapea preguntas/respuestas de encuestas a la taxonomía de temas.

    Args:
        survey_data: Lista de respuestas de encuesta con campos:
            - canton: nombre del cantón
            - tema: tema/prioridad mencionada
            - porcentaje: peso de la respuesta
        config_path: Ruta a config/themes.yml.

    Returns:
        Diccionario {canton: {tema_id: priority_score 0-1}}.
    """
    themes = load_themes(config_path)
    keyword_index = _build_keyword_index(themes)

    # Agrupar por cantón
    canton_data: dict[str, list[dict]] = defaultdict(list)
    for row in survey_data:
        canton = row.get("canton", "Unknown")
        canton_data[canton].append(row)

    # Calcular priority_scores por cantón
    result = {}
    for canton, rows in canton_data.items():
        theme_weights: dict[str, float] = defaultdict(float)
        total_weight = 0.0

        for row in rows:
            tema_text = row.get("tema", "").lower()
            porcentaje = float(row.get("porcentaje", 0))

            # Buscar coincidencia con keywords
            matched_theme = None
            for kw, theme_id in keyword_index.items():
                if kw in tema_text:
                    matched_theme = theme_id
                    break

            if matched_theme is None:
                # Coincidencia difusa simple
                for theme in themes:
                    if theme["name"].lower() in tema_text:
                        matched_theme = theme["id"]
                        break

            if matched_theme:
                theme_weights[matched_theme] += porcentaje
                total_weight += porcentaje

        # Normalizar a 0-1
        if total_weight > 0:
            priority_scores = {
                tid: round(theme_weights.get(tid, 0) / total_weight, 4)
                for tid in [t["id"] for t in themes]
            }
        else:
            priority_scores = {t["id"]: 0.0 for t in themes}

        result[canton] = priority_scores

    return result


def run_lda(
    documents: list[str],
    n_topics: int = 10,
    config_path: str = "config/themes.yml",
) -> list[dict]:
    """
    Ejecuta LDA (Latent Dirichlet Allocation) para detección de temas emergentes.

    Es opcional y se usa para descubrir temas que no están en la taxonomía.

    Args:
        documents: Lista de textos de documentos.
        n_topics: Número de temas a extraer.
        config_path: Ruta a config/themes.yml.

    Returns:
        Lista de temas con palabras clave principales.
    """
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation

    themes = load_themes(config_path)
    existing_keywords = set()
    for theme in themes:
        for kw in theme.get("keywords", []):
            existing_keywords.add(_normalize_keyword(kw))

    # Vectorizar
    vectorizer = CountVectorizer(
        max_features=1000,
        stop_words=["de", "la", "que", "el", "en", "y", "a", "los", "se", "del"],
        lowercase=True,
    )
    doc_term_matrix = vectorizer.fit_transform(documents)

    # LDA
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=200,
    )
    lda.fit(doc_term_matrix)

    # Extraer temas
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[-10:][::-1]
        top_words = [feature_names[i] for i in top_words_idx]

        # Verificar si es un tema emergente (no en taxonomía)
        is_emerging = not any(kw in existing_keywords for kw in top_words[:5])

        topics.append({
            "topic_id": topic_idx,
            "top_words": top_words,
            "is_emerging": is_emerging,
        })

        if is_emerging:
            logger.info(f"Tema emergente detectado #{topic_idx}: {', '.join(top_words[:5])}")

    return topics


def build_program_vector(
    text: str,
    config_path: str = "config/themes.yml",
    use_ner: bool = True,
) -> dict[str, float]:
    """
    Construye el vector de programa de gobierno para un documento.

    Alias de extract_theme_scores para claridad semántica.

    Args:
        text: Texto del plan de gobierno.
        config_path: Ruta a config/themes.yml.
        use_ner: Si True, aplica boost de NER.

    Returns:
        Diccionario {tema_id: score 0-1}.
    """
    return extract_theme_scores(text, config_path, use_ner=use_ner)


def build_priority_vector(
    survey_data: list[dict],
    canton: str,
    config_path: str = "config/themes.yml",
) -> dict[str, float]:
    """
    Construye el vector de prioridades para un cantón específico.

    Args:
        survey_data: Lista de respuestas de encuesta.
        canton: Nombre del cantón.
        config_path: Ruta a config/themes.yml.

    Returns:
        Diccionario {tema_id: priority_score 0-1}.
    """
    canton_scores = map_survey_to_themes(survey_data, config_path)
    return canton_scores.get(canton, {})
