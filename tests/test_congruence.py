#!/usr/bin/env python3
"""
Tests para el pipeline de congruencia política.

Cubre:
    - Extracción de temas: scores válidos 0-1
    - Cálculo de congruencia: escala 0-100
    - Similitud coseno: correctitud matemática
    - Agregación por partido: funciones estadísticas
    - Intervalos de confianza bootstrap
"""
import numpy as np
import pytest

from src.etl.congruence import (
    cosine_similarity,
    calculate_congruence,
    aggregate_by_party,
    bootstrap_confidence_interval,
    calculate_all_congruence,
    vector_to_array,
    THEME_IDS,
)
from src.etl.theme_extraction import (
    load_themes,
    keyword_matching,
    extract_theme_scores,
    build_program_vector,
    build_priority_vector,
)


# ─── Fixtures ───

@pytest.fixture
def themes():
    """Carga la taxonomía de temas."""
    return load_themes("config/themes.yml")


@pytest.fixture
def sample_program_text():
    """Texto de ejemplo de un programa de gobierno."""
    return (
        "Nuestro plan de gobierno prioriza la salud y la educación. "
        "Construiremos nuevos hospitales y centros de salud en cada cantón. "
        "Mejoraremos la infraestructura escolar y daremos becas a estudiantes. "
        "La seguridad ciudadana es fundamental: más policías y cámaras de vigilancia. "
        "Promoveremos el empleo y el emprendimiento con apoyo a pymes. "
        "Garantizaremos agua potable y saneamiento para todos. "
        "Mejoraremos la movilidad con nuevas vías y transporte público. "
        "Protegeremos el ambiente y las áreas protegidas. "
        "Lucharemos contra la corrupción con transparencia y rendición de cuentas. "
        "Optimizaremos el presupuesto y el gasto público."
    )


@pytest.fixture
def sample_survey_data():
    """Datos de encuesta de ejemplo."""
    return [
        {"canton": "Quito", "tema": "transporte y movilidad", "porcentaje": 25, "fuente": "INEC"},
        {"canton": "Quito", "tema": "seguridad y delincuencia", "porcentaje": 20, "fuente": "INEC"},
        {"canton": "Quito", "tema": "ambiente y contaminación", "porcentaje": 15, "fuente": "INEC"},
        {"canton": "Quito", "tema": "empleo y trabajo", "porcentaje": 15, "fuente": "INEC"},
        {"canton": "Quito", "tema": "educación y escuelas", "porcentaje": 10, "fuente": "INEC"},
        {"canton": "Quito", "tema": "salud y hospitales", "porcentaje": 10, "fuente": "INEC"},
        {"canton": "Quito", "tema": "transparencia y corrupción", "porcentaje": 5, "fuente": "INEC"},
        {"canton": "Guayaquil", "tema": "seguridad ciudadana", "porcentaje": 30, "fuente": "INEC"},
        {"canton": "Guayaquil", "tema": "empleo y desempleo", "porcentaje": 20, "fuente": "INEC"},
        {"canton": "Guayaquil", "tema": "transporte público", "porcentaje": 15, "fuente": "INEC"},
        {"canton": "Guayaquil", "tema": "salud y atención médica", "porcentaje": 12, "fuente": "INEC"},
        {"canton": "Guayaquil", "tema": "vivienda y barrios", "porcentaje": 10, "fuente": "INEC"},
        {"canton": "Guayaquil", "tema": "educación", "porcentaje": 8, "fuente": "INEC"},
        {"canton": "Guayaquil", "tema": "agua y alcantarillado", "porcentaje": 5, "fuente": "INEC"},
    ]


@pytest.fixture
def sample_program_vector():
    """Vector de programa de ejemplo."""
    return {
        "salud": 0.15,
        "educacion": 0.12,
        "agua": 0.08,
        "movilidad": 0.10,
        "empleo": 0.14,
        "seguridad": 0.16,
        "vivienda": 0.06,
        "ambiente": 0.07,
        "transparencia": 0.06,
        "presupuesto": 0.06,
    }


@pytest.fixture
def sample_priority_vector():
    """Vector de prioridades de ejemplo."""
    return {
        "salud": 0.10,
        "educacion": 0.10,
        "agua": 0.05,
        "movilidad": 0.20,
        "empleo": 0.15,
        "seguridad": 0.20,
        "vivienda": 0.05,
        "ambiente": 0.10,
        "transparencia": 0.03,
        "presupuesto": 0.02,
    }


# ─── Tests de extracción de temas ───

class TestThemeExtraction:
    """Tests para extracción de temas vía NLP."""

    def test_load_themes_returns_list(self, themes):
        """La taxonomía se carga como lista con 10 temas."""
        assert isinstance(themes, list)
        assert len(themes) == 10

    def test_themes_have_required_fields(self, themes):
        """Cada tema tiene id, name y keywords."""
        for theme in themes:
            assert "id" in theme
            assert "name" in theme
            assert "keywords" in theme
            assert len(theme["keywords"]) >= 8

    def test_keyword_matching_returns_scores_0_1(self, themes, sample_program_text):
        """Los scores de keyword matching están entre 0 y 1."""
        scores = keyword_matching(sample_program_text, themes)
        for theme_id, score in scores.items():
            assert 0.0 <= score <= 1.0, f"Score {score} fuera de rango para tema {theme_id}"

    def test_keyword_matching_detects_all_themes(self, themes, sample_program_text):
        """El texto de ejemplo activa todos los temas."""
        scores = keyword_matching(sample_program_text, themes)
        # Al menos 8 de 10 temas deberían tener score > 0
        active = sum(1 for s in scores.values() if s > 0)
        assert active >= 8, f"Solo {active} temas detectados, esperado ≥ 8"

    def test_extract_theme_scores_returns_valid_dict(self, sample_program_text):
        """extract_theme_scores retorna dict con todos los tema_ids."""
        scores = extract_theme_scores(sample_program_text, use_ner=False)
        assert isinstance(scores, dict)
        for tid in THEME_IDS:
            assert tid in scores, f"Tema {tid} no encontrado en scores"
            assert 0.0 <= scores[tid] <= 1.0

    def test_empty_text_returns_zero_scores(self, themes):
        """Texto vacío retorna scores de 0."""
        scores = keyword_matching("", themes)
        for score in scores.values():
            assert score == 0.0

    def test_build_program_vector(self, sample_program_text):
        """build_program_vector produce un vector válido."""
        vec = build_program_vector(sample_program_text, use_ner=False)
        assert isinstance(vec, dict)
        assert len(vec) == 10
        for v in vec.values():
            assert 0.0 <= v <= 1.0

    def test_build_priority_vector(self, sample_survey_data):
        """build_priority_vector produce un vector por cantón."""
        vec = build_priority_vector(sample_survey_data, "Quito")
        assert isinstance(vec, dict)
        assert len(vec) == 10
        for v in vec.values():
            assert 0.0 <= v <= 1.0
        # Quito debería priorizar movilidad
        assert vec["movilidad"] > 0
        assert vec["seguridad"] > 0


# ─── Tests de similitud coseno ───

class TestCosineSimilarity:
    """Tests para el cálculo de similitud coseno."""

    def test_identical_vectors(self):
        """Vectores idénticos tienen similitud 1.0."""
        a = np.array([1.0, 2.0, 3.0])
        sim = cosine_similarity(a, a)
        assert sim == pytest.approx(1.0, abs=1e-6)

    def test_orthogonal_vectors(self):
        """Vectores ortogonales tienen similitud 0.0."""
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        sim = cosine_similarity(a, b)
        assert sim == pytest.approx(0.0, abs=1e-6)

    def test_zero_vector(self):
        """Vector cero tiene similitud 0.0."""
        a = np.array([0.0, 0.0, 0.0])
        b = np.array([1.0, 2.0, 3.0])
        sim = cosine_similarity(a, b)
        assert sim == 0.0

    def test_proportional_vectors(self):
        """Vectores proporcionales tienen similitud 1.0."""
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([2.0, 4.0, 6.0])
        sim = cosine_similarity(a, b)
        assert sim == pytest.approx(1.0, abs=1e-6)

    def test_non_negative_vectors(self):
        """Para vectores no negativos, la similitud está entre 0 y 1."""
        rng = np.random.default_rng(42)
        for _ in range(100):
            a = rng.random(10)
            b = rng.random(10)
            sim = cosine_similarity(a, b)
            assert 0.0 <= sim <= 1.0


# ─── Tests de cálculo de congruencia ───

class TestCongruenceCalculation:
    """Tests para el cálculo de congruencia."""

    def test_congruence_range_0_100(self, sample_program_vector, sample_priority_vector):
        """La congruencia está entre 0 y 100."""
        score = calculate_congruence(sample_program_vector, sample_priority_vector)
        assert 0.0 <= score <= 100.0

    def test_identical_vectors_max_congruence(self):
        """Vectores idénticos producen congruencia cercana a 100."""
        vec = {
            "salud": 0.2, "educacion": 0.15, "agua": 0.1,
            "movilidad": 0.1, "empleo": 0.1, "seguridad": 0.15,
            "vivienda": 0.05, "ambiente": 0.05, "transparencia": 0.05,
            "presupuesto": 0.05,
        }
        score = calculate_congruence(vec, vec)
        assert score == pytest.approx(100.0, abs=0.01)

    def test_zero_vectors_min_congruence(self):
        """Vectores nulos producen congruencia 0."""
        vec = {tid: 0.0 for tid in THEME_IDS}
        score = calculate_congruence(vec, vec)
        assert score == 0.0

    def test_calculate_all_congruence(self, sample_program_vector, sample_priority_vector):
        """calculate_all_congruence genera scores para todos los pares."""
        prog = {"Party A": sample_program_vector}
        prio = {"Canton X": sample_priority_vector}
        results = calculate_all_congruence(prog, prio)
        assert len(results) == 1
        assert results[0]["party"] == "Party A"
        assert results[0]["canton"] == "Canton X"
        assert 0.0 <= results[0]["congruence"] <= 100.0

    def test_vector_to_array(self, sample_program_vector):
        """vector_to_array convierte dict a array en orden correcto."""
        arr = vector_to_array(sample_program_vector)
        assert isinstance(arr, np.ndarray)
        assert len(arr) == 10
        # Verificar orden
        for i, tid in enumerate(THEME_IDS):
            assert arr[i] == pytest.approx(sample_program_vector[tid])


# ─── Tests de agregación ───

class TestAggregation:
    """Tests para agregación por partido."""

    def test_aggregate_by_party(self):
        """aggregate_by_party calcula estadísticas correctas."""
        scores = [
            {"party": "Party A", "canton": "C1", "congruence": 80.0},
            {"party": "Party A", "canton": "C2", "congruence": 60.0},
            {"party": "Party A", "canton": "C3", "congruence": 70.0},
            {"party": "Party B", "canton": "C1", "congruence": 50.0},
            {"party": "Party B", "canton": "C2", "congruence": 90.0},
        ]
        result = aggregate_by_party(scores)

        assert "Party A" in result
        assert "Party B" in result
        assert result["Party A"]["n"] == 3
        assert result["Party B"]["n"] == 2
        assert result["Party A"]["mean"] == pytest.approx(70.0, abs=0.01)
        assert result["Party A"]["median"] == pytest.approx(70.0, abs=0.01)
        assert result["Party A"]["min"] == 60.0
        assert result["Party A"]["max"] == 80.0
        assert len(result["Party A"]["top_cantones"]) <= 5
        assert len(result["Party A"]["bottom_cantones"]) <= 5

    def test_aggregate_top_canton(self):
        """El top cantón tiene el score más alto."""
        scores = [
            {"party": "P", "canton": "C1", "congruence": 50.0},
            {"party": "P", "canton": "C2", "congruence": 90.0},
            {"party": "P", "canton": "C3", "congruence": 70.0},
        ]
        result = aggregate_by_party(scores)
        top = result["P"]["top_cantones"][0]
        assert top["canton"] == "C2"
        assert top["congruence"] == 90.0

    def test_bootstrap_ci(self):
        """Los intervalos de confianza bootstrap contienen la media."""
        scores = [60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0]
        lo, hi = bootstrap_confidence_interval(scores, n_bootstrap=500)
        mean = np.mean(scores)
        assert lo <= mean <= hi
        assert lo < hi

    def test_bootstrap_ci_empty(self):
        """Lista vacía retorna (0, 0)."""
        lo, hi = bootstrap_confidence_interval([])
        assert lo == 0.0
        assert hi == 0.0
