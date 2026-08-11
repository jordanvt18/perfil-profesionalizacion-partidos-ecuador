#!/usr/bin/env python3
"""
Cálculo de congruencia entre programas de gobierno y prioridades ciudadanas.

Mide la alineación entre lo que proponen los candidatos (program_vectors)
y lo que necesitan los ciudadanos (priority_vectors) usando similitud coseno.

Funciones principales:
    - cosine_similarity: Similitud coseno entre dos vectores
    - calculate_congruence: Congruencia 0-100 entre programa y prioridades
    - aggregate_by_party: Agregación por partido (media, mediana, top/bottom)
    - bootstrap_confidence_interval: Intervalos de confianza por bootstrap
    - correlation_with_indicators: Correlación con indicadores socioeconómicos
"""
import logging
from collections import defaultdict
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

# Temas en orden canónico (debe coincidir con config/themes.yml)
THEME_IDS = [
    "salud", "educacion", "agua", "movilidad", "empleo",
    "seguridad", "vivienda", "ambiente", "transparencia", "presupuesto",
]


def vector_to_array(vec: dict[str, float], theme_ids: list[str] = None) -> np.ndarray:
    """
    Convierte un diccionario de scores a array numpy en orden canónico.

    Args:
        vec: Diccionario {tema_id: score}.
        theme_ids: Orden de temas (default: THEME_IDS).

    Returns:
        Array numpy de scores.
    """
    if theme_ids is None:
        theme_ids = THEME_IDS
    return np.array([vec.get(tid, 0.0) for tid in theme_ids], dtype=np.float64)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calcula la similitud coseno entre dos vectores.

    cos(a, b) = (a · b) / (||a|| * ||b||)

    Args:
        a: Primer vector.
        b: Segundo vector.

    Returns:
        Similitud coseno entre 0 y 1.
    """
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(np.dot(a, b) / (norm_a * norm_b))


def calculate_congruence(
    program_vector: dict[str, float],
    priority_vector: dict[str, float],
    theme_ids: list[str] = None,
) -> float:
    """
    Calcula la congruencia entre un programa de gobierno y prioridades ciudadanas.

    Usa similitud coseno y normaliza a escala 0-100.

    Args:
        program_vector: Scores de temas del programa {tema_id: score 0-1}.
        priority_vector: Scores de prioridades del cantón {tema_id: score 0-1}.
        theme_ids: Orden de temas (default: THEME_IDS).

    Returns:
        Score de congruencia entre 0 y 100.
    """
    if theme_ids is None:
        theme_ids = THEME_IDS

    prog_arr = vector_to_array(program_vector, theme_ids)
    prio_arr = vector_to_array(priority_vector, theme_ids)

    cos_sim = cosine_similarity(prog_arr, prio_arr)

    # Normalizar a 0-100
    # La similitud coseno está entre 0 y 1 para vectores no negativos
    congruence = round(max(0.0, min(100.0, cos_sim * 100)), 2)

    return congruence


def aggregate_by_party(
    congruence_scores: list[dict],
) -> dict[str, dict]:
    """
    Agrega scores de congruencia por partido político.

    Args:
        congruence_scores: Lista de diccionarios con:
            - party: nombre del partido
            - canton: nombre del cantón
            - congruence: score 0-100

    Returns:
        Diccionario {party: {mean, median, std, min, max, n, top_cantones, bottom_cantones}}.
    """
    party_data: dict[str, list[tuple[str, float]]] = defaultdict(list)

    for entry in congruence_scores:
        party = entry.get("party", "Unknown")
        canton = entry.get("canton", "Unknown")
        score = float(entry.get("congruence", 0))
        party_data[party].append((canton, score))

    result = {}
    for party, scores in party_data.items():
        values = [s for _, s in scores]
        arr = np.array(values)

        # Ordenar por score para top/bottom
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        result[party] = {
            "mean": round(float(np.mean(arr)), 2),
            "median": round(float(np.median(arr)), 2),
            "std": round(float(np.std(arr)), 2) if len(values) > 1 else 0.0,
            "min": round(float(np.min(arr)), 2),
            "max": round(float(np.max(arr)), 2),
            "n": len(values),
            "top_cantones": [
                {"canton": c, "congruence": s} for c, s in sorted_scores[:5]
            ],
            "bottom_cantones": [
                {"canton": c, "congruence": s} for c, s in sorted_scores[-5:]
            ],
        }

    return result


def bootstrap_confidence_interval(
    scores: list[float],
    n_bootstrap: int = 1000,
    confidence: float = 0.95,
    random_seed: int = 42,
) -> tuple[float, float]:
    """
    Calcula un intervalo de confianza por bootstrap para la media.

    Args:
        scores: Lista de scores de congruencia.
        n_bootstrap: Número de muestras bootstrap.
        confidence: Nivel de confianza (0-1).
        random_seed: Semilla aleatoria para reproducibilidad.

    Returns:
        Tupla (lower_bound, upper_bound) del intervalo de confianza.
    """
    if not scores:
        return (0.0, 0.0)

    rng = np.random.default_rng(random_seed)
    arr = np.array(scores)

    bootstrap_means = []
    for _ in range(n_bootstrap):
        sample = rng.choice(arr, size=len(arr), replace=True)
        bootstrap_means.append(np.mean(sample))

    alpha = (1 - confidence) / 2
    lower = float(np.percentile(bootstrap_means, alpha * 100))
    upper = float(np.percentile(bootstrap_means, (1 - alpha) * 100))

    return (round(lower, 2), round(upper, 2))


def correlation_with_indicators(
    congruence_scores: list[dict],
    indicators: list[dict],
    indicator_key: str = "pobreza",
) -> dict:
    """
    Analiza correlación entre congruencia e indicadores socioeconómicos.

    Args:
        congruence_scores: Lista con {canton, congruence}.
        indicators: Lista con {canton, indicador: valor}.
        indicator_key: Nombre del indicador a correlacionar.

    Returns:
        Diccionario con correlación de Pearson, Spearman y interpretación.
    """
    from scipy import stats as sp_stats

    # Construir mapeo cantón -> indicador
    indicator_map = {
        item["canton"]: float(item.get(indicator_key, 0))
        for item in indicators
        if "canton" in item and indicator_key in item
    }

    # Emparejar datos
    congruence_values = []
    indicator_values = []
    for entry in congruence_scores:
        canton = entry.get("canton", "")
        if canton in indicator_map:
            congruence_values.append(float(entry["congruence"]))
            indicator_values.append(indicator_map[canton])

    if len(congruence_values) < 3:
        logger.warning(
            f"Solo {len(congruence_values)} cantones con datos de {indicator_key}. "
            "Se necesitan al menos 3 para correlación."
        )
        return {"pearson_r": 0, "spearman_r": 0, "n": len(congruence_values)}

    # Pearson
    pearson_r, pearson_p = sp_stats.pearsonr(congruence_values, indicator_values)

    # Spearman
    spearman_r, spearman_p = sp_stats.spearmanr(congruence_values, indicator_values)

    # Interpretación
    if abs(pearson_r) < 0.1:
        interpretation = "Sin correlación"
    elif abs(pearson_r) < 0.3:
        interpretation = "Correlación débil"
    elif abs(pearson_r) < 0.5:
        interpretation = "Correlación moderada"
    elif abs(pearson_r) < 0.7:
        interpretation = "Correlación fuerte"
    else:
        interpretation = "Correlación muy fuerte"

    return {
        "pearson_r": round(float(pearson_r), 4),
        "pearson_p": round(float(pearson_p), 4),
        "spearman_r": round(float(spearman_r), 4),
        "spearman_p": round(float(spearman_p), 4),
        "n": len(congruence_values),
        "indicator": indicator_key,
        "interpretation": interpretation,
        "direction": "positiva" if pearson_r > 0 else "negativa",
    }


def calculate_all_congruence(
    program_vectors: dict[str, dict[str, float]],
    priority_vectors: dict[str, dict[str, float]],
    theme_ids: list[str] = None,
) -> list[dict]:
    """
    Calcula la congruencia para todos los pares partido-cantón.

    Args:
        program_vectors: {partido: {tema_id: score}}.
        priority_vectors: {canton: {tema_id: score}}.
        theme_ids: Orden de temas.

    Returns:
        Lista de diccionarios con {party, canton, congruence, program_vector, priority_vector}.
    """
    if theme_ids is None:
        theme_ids = THEME_IDS

    results = []
    for party, prog_vec in program_vectors.items():
        for canton, prio_vec in priority_vectors.items():
            congruence = calculate_congruence(prog_vec, prio_vec, theme_ids)
            results.append({
                "party": party,
                "canton": canton,
                "congruence": congruence,
                "program_vector": prog_vec,
                "priority_vector": prio_vec,
            })

    logger.info(
        f"Calculados {len(results)} scores de congruencia "
        f"({len(program_vectors)} partidos × {len(priority_vectors)} cantones)"
    )

    return results
