#!/usr/bin/env python3
"""
Generador de datos demo para el mapa de congruencia política.

Genera vectores realistas de programas de gobierno (por partido) y
prioridades ciudadanas (por cantón) usando la taxonomía de 10 temas.

Datos de salida:
    - data/demo/themes.json — Taxonomía de temas
    - data/demo/program_vectors.json — Vectores de programas por partido
    - data/demo/priority_vectors.json — Vectores de prioridades por cantón
    - data/demo/congruence_scores.json — Scores de congruencia calculados
    - web/congruencia-demo-data.js — Todos los datos como exports JS

Prioridades realistas por cantón:
    - Guayaquil: seguridad, empleo, movilidad
    - Quito: movilidad, seguridad, ambiente
    - Cuenca: ambiente, educación, transparencia
    - Manabí (Portoviejo, Manta): agua, empleo, vivienda
    - Esmeraldas: salud, empleo, ambiente
    - Loja: educación, agua, empleo
"""
import json
import random
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Importar CANTONES desde build_hybrid_data
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.build_hybrid_data import CANTONES

from src.etl.congruence import (
    calculate_all_congruence,
    aggregate_by_party,
    bootstrap_confidence_interval,
    THEME_IDS,
)

random.seed(20260810)

# ─── Taxonomía de temas ───
THEMES = [
    {"id": "salud", "name": "Salud", "keywords": ["salud", "hospital", "centro de salud", "médico", "medicina", "EPS", "enfermedad", "atención médica", "postas", "dispensario"]},
    {"id": "educacion", "name": "Educación", "keywords": ["educación", "escuela", "colegio", "universidad", "profesor", "docente", "infraestructura escolar", "becas", "alfabetización", "educación inicial"]},
    {"id": "agua", "name": "Agua y Saneamiento", "keywords": ["agua", "alcantarillado", "saneamiento", "potable", "tratamiento de agua", "racionamiento", "acueducto", "sedapal"]},
    {"id": "movilidad", "name": "Movilidad y Transporte", "keywords": ["transporte", "movilidad", "vías", "carreteras", "puentes", "Metro", "BRT", "bus", "transporte público", "tránsito", "semáforos"]},
    {"id": "empleo", "name": "Empleo y Economía", "keywords": ["empleo", "trabajo", "emprendimiento", "pymes", "turismo", "desempleo", "informalidad", "desarrollo económico", "inversión", "productividad"]},
    {"id": "seguridad", "name": "Seguridad Ciudadana", "keywords": ["seguridad", "delincuencia", "crimen", "policía", "cámaras", "vigilancia", "prevención", "extorsión", "sicariato", "10 EC"]},
    {"id": "vivienda", "name": "Vivienda", "keywords": ["vivienda", "barrios", "urbanización", "planes de vivienda", "construcción", "arrendamiento", "bono de vivienda", "mejoramiento barrial"]},
    {"id": "ambiente", "name": "Ambiente", "keywords": ["ambiente", "contaminación", "reciclaje", "áreas protegidas", "deforestación", "cambio climático", "emisiones", "residuos", "arborización"]},
    {"id": "transparencia", "name": "Transparencia", "keywords": ["transparencia", "corrupción", "rendición de cuentas", "participación ciudadana", "ética", "auditoría", "control social", "acceso a información"]},
    {"id": "presupuesto", "name": "Presupuesto", "keywords": ["presupuesto", "gasto público", "inversión", "obras", "tributos", "impuestos", "endeudamiento", "participación", "asignación"]},
]

# ─── Partidos principales ───
PARTIES = [
    "ADN (Accion Democratica Nacional)",
    "Revolucion Ciudadana (RC5)",
    "Partido Social Cristiano (PSC)",
    "Movimiento Construye",
    "Pachakutik",
    "Movimiento CREO",
    "Avanza",
    "Izquierda Democratica (ID)",
]

# ─── Perfiles de prioridades por cantón ───
# Basado en características socioeconómicas reales de Ecuador
CANTON_PRIORITY_PROFILES = {
    # Guayas — seguridad y empleo son prioritarios
    "Guayaquil": {"seguridad": 0.28, "empleo": 0.20, "movilidad": 0.15, "salud": 0.12, "educacion": 0.08, "vivienda": 0.07, "ambiente": 0.04, "transparencia": 0.03, "presupuesto": 0.02, "agua": 0.01},
    "Duran": {"seguridad": 0.25, "empleo": 0.18, "vivienda": 0.15, "movilidad": 0.12, "salud": 0.10, "educacion": 0.08, "agua": 0.05, "ambiente": 0.03, "transparencia": 0.02, "presupuesto": 0.02},
    "Samborondon": {"seguridad": 0.22, "movilidad": 0.18, "ambiente": 0.12, "empleo": 0.10, "presupuesto": 0.08, "transparencia": 0.08, "salud": 0.07, "educacion": 0.07, "vivienda": 0.05, "agua": 0.03},
    "Milagro": {"empleo": 0.20, "seguridad": 0.18, "salud": 0.12, "educacion": 0.10, "movilidad": 0.10, "agua": 0.08, "vivienda": 0.08, "ambiente": 0.05, "presupuesto": 0.05, "transparencia": 0.04},
    "Daule": {"empleo": 0.22, "agua": 0.15, "movilidad": 0.12, "educacion": 0.10, "salud": 0.10, "seguridad": 0.10, "vivienda": 0.08, "presupuesto": 0.05, "ambiente": 0.05, "transparencia": 0.03},

    # Pichincha — movilidad y ambiente
    "Quito": {"movilidad": 0.22, "seguridad": 0.18, "ambiente": 0.12, "empleo": 0.10, "transparencia": 0.08, "salud": 0.08, "educacion": 0.08, "vivienda": 0.06, "presupuesto": 0.05, "agua": 0.03},
    "Cayambe": {"educacion": 0.18, "agua": 0.15, "empleo": 0.12, "salud": 0.12, "movilidad": 0.10, "seguridad": 0.08, "vivienda": 0.08, "ambiente": 0.07, "presupuesto": 0.05, "transparencia": 0.05},
    "Machachi": {"agua": 0.15, "movilidad": 0.14, "empleo": 0.12, "educacion": 0.10, "salud": 0.10, "seguridad": 0.10, "ambiente": 0.08, "vivienda": 0.07, "presupuesto": 0.07, "transparencia": 0.07},

    # Azuay — ambiente y educación
    "Cuenca": {"ambiente": 0.18, "educacion": 0.15, "movilidad": 0.12, "transparencia": 0.10, "salud": 0.10, "seguridad": 0.10, "empleo": 0.08, "agua": 0.07, "vivienda": 0.05, "presupuesto": 0.05},
    "Gualaceo": {"agua": 0.16, "educacion": 0.14, "salud": 0.12, "empleo": 0.10, "movilidad": 0.10, "ambiente": 0.08, "seguridad": 0.08, "vivienda": 0.08, "presupuesto": 0.07, "transparencia": 0.07},
    "Paute": {"agua": 0.18, "educacion": 0.14, "salud": 0.12, "empleo": 0.10, "movilidad": 0.10, "ambiente": 0.08, "seguridad": 0.08, "presupuesto": 0.07, "vivienda": 0.07, "transparencia": 0.06},

    # Manabí — agua y vivienda
    "Portoviejo": {"agua": 0.20, "empleo": 0.16, "vivienda": 0.12, "seguridad": 0.10, "salud": 0.10, "educacion": 0.10, "movilidad": 0.08, "ambiente": 0.05, "presupuesto": 0.05, "transparencia": 0.04},
    "Manta": {"empleo": 0.20, "agua": 0.15, "seguridad": 0.12, "movilidad": 0.10, "salud": 0.10, "vivienda": 0.10, "educacion": 0.08, "ambiente": 0.06, "presupuesto": 0.05, "transparencia": 0.04},
    "Chone": {"agua": 0.22, "salud": 0.14, "empleo": 0.12, "vivienda": 0.10, "educacion": 0.10, "seguridad": 0.08, "movilidad": 0.08, "ambiente": 0.06, "presupuesto": 0.05, "transparencia": 0.05},
    "Montecristi": {"agua": 0.18, "empleo": 0.14, "vivienda": 0.12, "movilidad": 0.10, "educacion": 0.10, "salud": 0.10, "seguridad": 0.08, "ambiente": 0.06, "presupuesto": 0.07, "transparencia": 0.05},

    # Esmeraldas — salud y empleo
    "Esmeraldas": {"salud": 0.18, "empleo": 0.16, "ambiente": 0.12, "seguridad": 0.10, "educacion": 0.10, "vivienda": 0.08, "agua": 0.08, "movilidad": 0.06, "presupuesto": 0.06, "transparencia": 0.06},
    "Atacames": {"empleo": 0.18, "ambiente": 0.14, "seguridad": 0.12, "salud": 0.10, "movilidad": 0.10, "agua": 0.08, "educacion": 0.08, "vivienda": 0.08, "presupuesto": 0.06, "transparencia": 0.06},

    # Tungurahua
    "Ambato": {"empleo": 0.16, "movilidad": 0.14, "educacion": 0.12, "salud": 0.10, "seguridad": 0.10, "ambiente": 0.08, "agua": 0.08, "vivienda": 0.08, "presupuesto": 0.07, "transparencia": 0.07},
    "Banos de Agua Santa": {"ambiente": 0.20, "turismo": 0.15, "movilidad": 0.12, "empleo": 0.10, "agua": 0.10, "salud": 0.08, "seguridad": 0.08, "educacion": 0.07, "presupuesto": 0.05, "transparencia": 0.05},

    # Loja
    "Loja": {"educacion": 0.18, "agua": 0.14, "empleo": 0.12, "seguridad": 0.10, "salud": 0.10, "movilidad": 0.08, "ambiente": 0.08, "vivienda": 0.08, "presupuesto": 0.06, "transparencia": 0.06},

    # El Oro
    "Machala": {"empleo": 0.18, "seguridad": 0.14, "salud": 0.12, "movilidad": 0.10, "agua": 0.10, "educacion": 0.10, "vivienda": 0.06, "ambiente": 0.06, "transparencia": 0.07, "presupuesto": 0.07},

    # Imbabura
    "Ibarra": {"empleo": 0.16, "movilidad": 0.12, "seguridad": 0.12, "educacion": 0.10, "salud": 0.10, "ambiente": 0.08, "agua": 0.08, "vivienda": 0.08, "presupuesto": 0.08, "transparencia": 0.08},
    "Otavalo": {"empleo": 0.18, "educacion": 0.14, "ambiente": 0.10, "salud": 0.10, "movilidad": 0.08, "agua": 0.08, "seguridad": 0.08, "vivienda": 0.08, "presupuesto": 0.08, "transparencia": 0.08},

    # Los Ríos
    "Babahoyo": {"agua": 0.18, "empleo": 0.14, "movilidad": 0.12, "salud": 0.10, "educacion": 0.10, "seguridad": 0.10, "vivienda": 0.06, "ambiente": 0.07, "presupuesto": 0.07, "transparencia": 0.06},
    "Quevedo": {"empleo": 0.18, "seguridad": 0.14, "movilidad": 0.12, "salud": 0.10, "agua": 0.10, "educacion": 0.08, "vivienda": 0.08, "ambiente": 0.05, "presupuesto": 0.08, "transparencia": 0.07},

    # Santo Domingo
    "Santo Domingo": {"seguridad": 0.20, "movilidad": 0.15, "empleo": 0.12, "salud": 0.10, "agua": 0.10, "educacion": 0.08, "vivienda": 0.08, "ambiente": 0.05, "presupuesto": 0.07, "transparencia": 0.05},
}

# ─── Perfiles de programas por partido ───
PARTY_PROGRAM_PROFILES = {
    "ADN (Accion Democratica Nacional)": {"seguridad": 0.22, "empleo": 0.16, "educacion": 0.12, "salud": 0.10, "movilidad": 0.10, "presupuesto": 0.08, "transparencia": 0.07, "vivienda": 0.06, "ambiente": 0.05, "agua": 0.04},
    "Revolucion Ciudadana (RC5)": {"salud": 0.16, "educacion": 0.14, "empleo": 0.12, "presupuesto": 0.10, "seguridad": 0.10, "movilidad": 0.08, "vivienda": 0.08, "agua": 0.08, "transparencia": 0.07, "ambiente": 0.07},
    "Partido Social Cristiano (PSC)": {"seguridad": 0.20, "empleo": 0.15, "movilidad": 0.12, "presupuesto": 0.10, "salud": 0.08, "vivienda": 0.08, "educacion": 0.08, "transparencia": 0.07, "ambiente": 0.07, "agua": 0.05},
    "Movimiento Construye": {"transparencia": 0.16, "ambiente": 0.14, "educacion": 0.12, "empleo": 0.10, "salud": 0.10, "seguridad": 0.08, "movilidad": 0.08, "agua": 0.08, "vivienda": 0.07, "presupuesto": 0.07},
    "Pachakutik": {"ambiente": 0.18, "agua": 0.14, "educacion": 0.12, "transparencia": 0.10, "salud": 0.10, "empleo": 0.08, "vivienda": 0.08, "presupuesto": 0.07, "seguridad": 0.07, "movilidad": 0.06},
    "Movimiento CREO": {"empleo": 0.18, "presupuesto": 0.12, "movilidad": 0.12, "seguridad": 0.10, "transparencia": 0.10, "educacion": 0.08, "salud": 0.08, "ambiente": 0.06, "vivienda": 0.06, "agua": 0.10},
    "Avanza": {"empleo": 0.16, "educacion": 0.12, "movilidad": 0.12, "salud": 0.10, "presupuesto": 0.10, "seguridad": 0.10, "agua": 0.08, "transparencia": 0.08, "vivienda": 0.07, "ambiente": 0.07},
    "Izquierda Democratica (ID)": {"transparencia": 0.16, "educacion": 0.14, "salud": 0.12, "ambiente": 0.10, "empleo": 0.10, "presupuesto": 0.08, "seguridad": 0.08, "agua": 0.08, "movilidad": 0.07, "vivienda": 0.07},
}


def generate_program_vectors() -> dict[str, dict[str, float]]:
    """
    Genera vectores de programas de gobierno realistas por partido.

    Añade variación aleatoria a los perfiles base para simular
    diferencias regionales en los planes de campaña.

    Returns:
        Diccionario {partido: {tema_id: score 0-1}}.
    """
    program_vectors = {}
    for party, profile in PARTY_PROGRAM_PROFILES.items():
        vec = {}
        for tid in THEME_IDS:
            base = profile.get(tid, 0.05)
            # Añadir ruido aleatorio ±20%
            noise = random.uniform(-0.04, 0.04)
            score = max(0.01, min(1.0, base + noise))
            vec[tid] = round(score, 4)
        program_vectors[party] = vec

    return program_vectors


def generate_priority_vectors() -> dict[str, dict[str, float]]:
    """
    Genera vectores de prioridades ciudadanas por cantón.

    Usa perfiles realistas basados en características socioeconómicas.
    Para cantones sin perfil específico, genera uno genérico con variación.

    Returns:
        Diccionario {canton: {tema_id: priority_score 0-1}}.
    """
    priority_vectors = {}

    # Cantones con perfiles específicos
    for canton, profile in CANTON_PRIORITY_PROFILES.items():
        vec = {}
        for tid in THEME_IDS:
            base = profile.get(tid, 0.05)
            noise = random.uniform(-0.03, 0.03)
            score = max(0.01, min(1.0, base + noise))
            vec[tid] = round(score, 4)
        priority_vectors[canton] = vec

    # Cantones sin perfil específico: generar genérico
    for prov, cantones in CANTONES.items():
        for canton in cantones:
            if canton not in priority_vectors:
                # Perfil genérico con variación
                vec = {}
                for tid in THEME_IDS:
                    base = random.uniform(0.05, 0.15)
                    vec[tid] = round(base, 4)
                # Resaltar 2-3 temas aleatorios
                highlighted = random.sample(THEME_IDS, k=3)
                for tid in highlighted:
                    vec[tid] = round(random.uniform(0.15, 0.25), 4)
                priority_vectors[canton] = vec

    return priority_vectors


def main():
    """Genera todos los datos demo y los guarda en archivos.

    IMPORTANTE: este script NO sobrescribe web/congruencia-demo-data.js.
    El contrato de exports que espera congruencia.js (TEMAS, PARTIDOS,
    CANDIDATOS, CO_MENTION_MATRIX, THEME_GAPS, YEARS) lo mantiene
    scripts/generate_frontend_demo_data.py. Este script genera únicamente
    JSON de respaldo (data/demo/) y un JS con prefijo congruencia* que
    ninguna página importa.
    """
    repo_root = Path(__file__).parent.parent
    web_dir = repo_root / "web"

    # 1. Generar vectores
    program_vectors = generate_program_vectors()
    priority_vectors = generate_priority_vectors()

    # 2. Calcular congruencia
    congruence_scores = calculate_all_congruence(
        program_vectors, priority_vectors, THEME_IDS
    )

    # 3. Agregar por partido
    party_aggregates = aggregate_by_party(congruence_scores)

    # 4. Bootstrap CIs por partido
    party_cis = {}
    for party, scores_list in defaultdict(list, {k: [] for k in party_aggregates}).items():
        pass  # Inicializar

    party_ci_data = {}
    for party in party_aggregates:
        party_scores = [
            entry["congruence"]
            for entry in congruence_scores
            if entry["party"] == party
        ]
        if party_scores:
            lo, hi = bootstrap_confidence_interval(party_scores)
            party_ci_data[party] = {"ci_lower": lo, "ci_upper": hi}

    # 5. Guardar JSON
    demo_dir = repo_root / "data" / "demo"
    demo_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "themes.json": THEMES,
        "program_vectors.json": program_vectors,
        "priority_vectors.json": priority_vectors,
        "congruence_scores.json": {
            "scores": congruence_scores,
            "party_aggregates": party_aggregates,
            "confidence_intervals": party_ci_data,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "n_parties": len(program_vectors),
            "n_cantones": len(priority_vectors),
            "n_scores": len(congruence_scores),
        },
    }

    for filename, data in outputs.items():
        filepath = demo_dir / filename
        filepath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        logger_fn = print
        logger_fn(f"Guardado: {filepath}")

    # 6. Generar JS para web (formato compatible con congruencia.js)
    # NOTA: congruencia.js importa: TEMAS, PARTIDOS, CANDIDATOS, CO_MENTION_MATRIX, THEME_GAPS, YEARS
    # El frontend worker ya creó congruencia-demo-data.js con el formato correcto.
    # Este script genera datos JSON para la API, no sobrescribe el JS del frontend.
    js_path = web_dir / "congruencia-api-data.js"

    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// Mapa de Congruencia Política - Datos generados por pipeline ETL\n")
        f.write(f"// Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"// {len(program_vectors)} partidos × {len(priority_vectors)} cantones\n")
        f.write(f"// {len(congruence_scores)} scores de congruencia calculados\n\n")

        f.write("export const congruenciaThemes = ")
        json.dump(THEMES, f, ensure_ascii=False)
        f.write(";\n\n")

        f.write("export const congruenciaProgramVectors = ")
        json.dump(program_vectors, f, ensure_ascii=False)
        f.write(";\n\n")

        f.write("export const congruenciaPriorityVectors = ")
        json.dump(priority_vectors, f, ensure_ascii=False)
        f.write(";\n\n")

        f.write("export const congruenciaScores = ")
        json.dump(congruence_scores, f, ensure_ascii=False)
        f.write(";\n\n")

        f.write("export const congruenciaPartyAggregates = ")
        json.dump(party_aggregates, f, ensure_ascii=False)
        f.write(";\n\n")

        f.write("export const congruenciaConfidenceIntervals = ")
        json.dump(party_ci_data, f, ensure_ascii=False)
        f.write(";\n\n")

    print(f"Guardado: {js_path}")

    # Resumen
    print(f"\n{'='*60}")
    print(f"RESUMEN DE DATOS DEMO GENERADOS")
    print(f"{'='*60}")
    print(f"  Temas: {len(THEMES)}")
    print(f"  Partidos: {len(program_vectors)}")
    print(f"  Cantones: {len(priority_vectors)}")
    print(f"  Scores de congruencia: {len(congruence_scores)}")
    print(f"  Congruencia promedio: {sum(s['congruence'] for s in congruence_scores)/len(congruence_scores):.2f}")
    print(f"  Congruencia mínima: {min(s['congruence'] for s in congruence_scores):.2f}")
    print(f"  Congruencia máxima: {max(s['congruence'] for s in congruence_scores):.2f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
