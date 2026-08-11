"""Router de FastAPI para endpoints del mapa de congruencia política.

Este módulo implementa los endpoints relacionados con:
- Temas (themes) y sus diccionarios de palabras clave
- Prioridades cantonales (vector de prioridades por cantón)
- Programas de candidatos (scores por tema)
- Cálculo de congruencia entre candidatos y cantones
- Agregados partidarios por provincia
- Mapa de congruencia para un partido
- Ranking de candidatos por congruencia en un cantón
- Grafo de co-mention de temas

Los datos se cargan desde data/processed/ si están disponibles,
con fallback a data/demo/ siguiendo el mismo patrón que main.py.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(
    prefix="/congruencia",
    tags=["congruencia"],
    responses={404: {"description": "Recurso no encontrado"}},
)

# ═══════════════════════════════════════════════════════════════════════════
# Definición de los 10 temas prioritarios con palabras clave
# ═══════════════════════════════════════════════════════════════════════════

THEMES: List[Dict[str, Any]] = [
    {
        "theme_id": "seguridad_ciudadana",
        "label": "Seguridad Ciudadana",
        "keywords": [
            "seguridad", "delincuencia", "criminalidad", "policia", "robos",
            "hurtos", "narcotrafico", "pandillas", "violencia", "convivencia",
        ],
    },
    {
        "theme_id": "empleo_economia",
        "label": "Empleo y Economía",
        "keywords": [
            "empleo", "trabajo", "desempleo", "economia", "emprendimiento",
            "microempresa", "formalizacion", "ingresos", "salarios", "productividad",
        ],
    },
    {
        "theme_id": "educacion",
        "label": "Educación",
        "keywords": [
            "educacion", "escuela", "colegio", "universidad", "docentes",
            "infraestructura educativa", "becas", "alfabetizacion", "tecnologia educativa",
        ],
    },
    {
        "theme_id": "salud",
        "label": "Salud",
        "keywords": [
            "salud", "hospital", "centro de salud", "medicamentos", "atencion medica",
            "enfermedades", "prevencion", "vacunacion", "seguro social", "mortalidad",
        ],
    },
    {
        "theme_id": "infraestructura_vial",
        "label": "Infraestructura Vial",
        "keywords": [
            "vias", "carreteras", "calles", "asfalto", "puentes",
            "infraestructura", "transporte", "movilidad", "pavimentacion", "caminos vecinales",
        ],
    },
    {
        "theme_id": "ambiente_agua",
        "label": "Ambiente y Agua",
        "keywords": [
            "agua", "alcantarillado", "ambiente", "contaminacion", "deforestacion",
            "recursos naturales", "saneamiento", "desechos", " areas verdes", "cambio climatico",
        ],
    },
    {
        "theme_id": "participacion_ciudadana",
        "label": "Participación Ciudadana",
        "keywords": [
            "participacion", "rendicion de cuentas", "transparencia", "control social",
            "asambleas", "cabildos", "consejos", "veeduria", "presupuesto participativo",
        ],
    },
    {
        "theme_id": "cultura_deporte",
        "label": "Cultura y Deporte",
        "keywords": [
            "cultura", "deporte", "patrimonio", "eventos culturales", "escenario deportivo",
            "recreacion", "identidad", "tradiciones", "centros culturales",
        ],
    },
    {
        "theme_id": "desarrollo_rural",
        "label": "Desarrollo Rural y Agricultura",
        "keywords": [
            "agricultura", "rural", "campesino", "riego", "tierras",
            "productividad agricola", "asociaciones", "ganaderia", "soberania alimentaria",
        ],
    },
    {
        "theme_id": "genero_inclusion",
        "label": "Género e Inclusión",
        "keywords": [
            "genero", "mujeres", "inclusion", "discapacidad", "igualdad",
            "violencia de genero", "grupos prioritarios", "diversidad", "equidad",
        ],
    },
]

THEME_IDS: List[str] = [t["theme_id"] for t in THEMES]


# ═══════════════════════════════════════════════════════════════════════════
# Utilidades de carga de datos (mismo patrón que main.py)
# ═══════════════════════════════════════════════════════════════════════════

def _load_json(filename: str) -> Any:
    """Carga un JSON desde data/processed/ o data/demo/ con fallback.

    Busca primero en data/processed/ (datos reales procesados),
    y si no existe, usa data/demo/ (datos de demostración).
    """
    processed_path = Path(f"data/processed/{filename}")
    demo_path = Path(f"data/demo/{filename}")

    path = processed_path if processed_path.exists() else demo_path
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _load_canton_priorities() -> List[Dict[str, Any]]:
    """Carga el vector de prioridades por cantón."""
    data = _load_json("canton_priorities.json")
    if data is not None:
        return data
    # Generar datos sintéticos por defecto si no hay archivo
    return _generate_default_canton_priorities()


def _load_candidate_programs() -> List[Dict[str, Any]]:
    """Carga los programas de candidatos con scores por tema."""
    data = _load_json("candidate_programs.json")
    if data is not None:
        return data
    return _generate_default_candidate_programs()


def _load_co_mentions() -> List[Dict[str, Any]]:
    """Carga datos de co-mention de temas."""
    data = _load_json("theme_co_mentions.json")
    if data is not None:
        return data
    return _generate_default_co_mentions()


# ═══════════════════════════════════════════════════════════════════════════
# Generación de datos sintéticos por defecto
# ═══════════════════════════════════════════════════════════════════════════

def _generate_default_canton_priorities() -> List[Dict[str, Any]]:
    """Genera prioridades sintéticas para todos los cantones conocidos."""
    import random
    random.seed(42)

    # Base de cantones desde candidates.json o aggregates.json
    candidates = _load_json("candidates.json") or []
    cantones_set = set()
    for c in candidates:
        prov = c.get("provincia", "")
        canton = c.get("canton", "")
        if prov and canton:
            cantones_set.add((prov, canton))

    # Fallback si no hay candidates.json
    if not cantones_set:
        cantones_set = {("Pichincha", "Quito"), ("Guayas", "Guayaquil"), ("Azuay", "Cuenca")}

    result: List[Dict[str, Any]] = []
    for i, (provincia, canton) in enumerate(sorted(cantones_set)):
        scores = {tid: round(random.uniform(0.3, 1.0), 2) for tid in THEME_IDS}
        # Normalizar para que sumen 1 (distribución de prioridades)
        total = sum(scores.values())
        scores = {k: round(v / total, 4) for k, v in scores.items()}
        result.append({
            "canton_id": i + 1,
            "provincia": provincia,
            "canton": canton,
            "priorities": scores,
        })
    return result


def _generate_default_candidate_programs() -> List[Dict[str, Any]]:
    """Genera scores sintéticos de programas de candidatos."""
    import random
    random.seed(99)

    candidates = _load_json("candidates.json") or []
    result: List[Dict[str, Any]] = []
    for c in candidates:
        cid = c.get("candidate_id")
        if cid is None:
            continue
        scores = {tid: round(random.uniform(0.0, 1.0), 2) for tid in THEME_IDS}
        result.append({
            "candidate_id": cid,
            "nombre": c.get("nombre", ""),
            "party_normalized": c.get("party_normalized", ""),
            "provincia": c.get("provincia", ""),
            "canton": c.get("canton", ""),
            "program_scores": scores,
        })
    return result


def _generate_default_co_mentions() -> List[Dict[str, Any]]:
    """Genera datos sintéticos de co-mention de temas."""
    import random
    random.seed(7)

    edges: List[Dict[str, Any]] = []
    for i, t1 in enumerate(THEME_IDS):
        for t2 in THEME_IDS[i + 1:]:
            weight = round(random.uniform(0.0, 1.0), 2)
            if weight > 0.15:  # Solo aristas con peso significativo
                edges.append({
                    "source": t1,
                    "target": t2,
                    "weight": weight,
                    "co_mentions": int(weight * 100),
                })
    return edges


# ═══════════════════════════════════════════════════════════════════════════
# Helpers de cálculo
# ═══════════════════════════════════════════════════════════════════════════

def _find_canton_by_id(canton_id: int, priorities: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Busca un cantón por su ID en la lista de prioridades."""
    for c in priorities:
        if c.get("canton_id") == canton_id:
            return c
    return None


def _find_candidate_program(candidate_id: int, programs: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Busca el programa de un candidato por su ID."""
    for p in programs:
        if p.get("candidate_id") == candidate_id:
            return p
    return None


def _compute_congruence(
    priorities: Dict[str, float],
    program_scores: Dict[str, float],
) -> Dict[str, Any]:
    """Calcula la congruencia entre un vector de prioridades y un programa.

    La congruencia se calcula como el producto punto ponderado:
    score = Σ(prioridad_tema × score_programa_tema) × 100

    Retorna el score global (0-100) y el desglose por tema.
    """
    per_theme: Dict[str, Dict[str, float]] = {}
    raw_sum = 0.0

    for theme in THEMES:
        tid = theme["theme_id"]
        p = priorities.get(tid, 0.0)
        s = program_scores.get(tid, 0.0)
        contribution = p * s
        raw_sum += contribution
        per_theme[tid] = {
            "label": theme["label"],
            "priority": round(p, 4),
            "program_score": round(s, 2),
            "contribution": round(contribution, 4),
        }

    # Normalizar a escala 0-100
    # El valor máximo teórico es Σ(prioridad × 1.0) = Σ(prioridades) = 1.0
    # Por lo tanto raw_sum ya está en escala 0-1 si las prioridades suman 1
    congruence_score = round(raw_sum * 100, 1)

    return {
        "congruence_score": congruence_score,
        "per_theme": per_theme,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════════════

# Nota: los endpoints 1-5 se montan sin el prefix /congruencia porque
# el router tiene prefix="/congruencia" pero estos endpoints tienen rutas
# distintas. Para manejar esto correctamente, definimos un segundo router
# sin prefix para las rutas que no comienzan con /congruencia.

# Router secundario para rutas sin el prefijo /congruencia
flat_router = APIRouter(tags=["congruencia"])


@flat_router.get("/themes")
def list_themes() -> Dict[str, Any]:
    """Lista los 10 temas prioritarios y sus diccionarios de palabras clave.

    Retorna:
        Diccionario con la lista de temas, cada uno con su ID, etiqueta
        y lista de palabras clave asociadas.
    """
    return {
        "count": len(THEMES),
        "themes": THEMES,
    }


@flat_router.get("/canton/{canton_id}/priorities")
def get_canton_priorities(canton_id: int) -> Dict[str, Any]:
    """Obtiene el vector de prioridades de un cantón específico.

    Args:
        canton_id: ID numérico del cantón.

    Returns:
        Vector de prioridades con scores (0-1) para cada uno de los 10 temas.
    """
    priorities = _load_canton_priorities()
    canton = _find_canton_by_id(canton_id, priorities)
    if canton is None:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el cantón con ID {canton_id}",
        )
    return canton


@flat_router.get("/candidate/{candidate_id}/program")
def get_candidate_program(candidate_id: int) -> Dict[str, Any]:
    """Obtiene los scores por tema del programa de un candidato.

    Args:
        candidate_id: ID numérico del candidato.

    Returns:
        Scores (0-1) del programa del candidato para cada uno de los 10 temas.
    """
    programs = _load_candidate_programs()
    program = _find_candidate_program(candidate_id, programs)
    if program is None:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el programa del candidato con ID {candidate_id}",
        )
    return program


@flat_router.get("/match")
def get_match(
    candidate_id: int = Query(..., description="ID del candidato"),
    canton_id: int = Query(..., description="ID del cantón"),
) -> Dict[str, Any]:
    """Calcula la congruencia entre un candidato y un cantón.

    Args:
        candidate_id: ID numérico del candidato.
        canton_id: ID numérico del cantón.

    Returns:
        Score de congruencia (0-100) con desglose por tema.
    """
    priorities_data = _load_canton_priorities()
    programs_data = _load_candidate_programs()

    canton = _find_canton_by_id(canton_id, priorities_data)
    if canton is None:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el cantón con ID {canton_id}",
        )

    program = _find_candidate_program(candidate_id, programs_data)
    if program is None:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el programa del candidato con ID {candidate_id}",
        )

    result = _compute_congruence(canton["priorities"], program["program_scores"])
    return {
        "candidate_id": candidate_id,
        "candidate_name": program.get("nombre", ""),
        "candidate_party": program.get("party_normalized", ""),
        "canton_id": canton_id,
        "canton": canton.get("canton", ""),
        "provincia": canton.get("provincia", ""),
        "congruence_score": result["congruence_score"],
        "per_theme": result["per_theme"],
    }


@flat_router.get("/party/{party_id}/aggregates")
def get_party_aggregates(
    party_id: str,
    province: Optional[str] = Query(None, description="Filtrar por provincia"),
) -> Dict[str, Any]:
    """Obtiene agregados partidarios por provincia.

    Args:
        party_id: Nombre normalizado del partido.
        province: Provincia opcional para filtrar.

    Returns:
        Agregados del partido, filtrados por provincia si se especifica.
    """
    aggregates = _load_json("aggregates.json") or []
    filtered = [a for a in aggregates if a.get("party_normalized") == party_id]
    if province:
        filtered = [a for a in filtered if a.get("province") == province]

    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron agregados para el partido '{party_id}'"
                   + (f" en la provincia '{province}'" if province else ""),
        )

    # Calcular estadísticas resumidas
    scores = [a.get("profesionalizacion_media", 0) for a in filtered]
    n_total = sum(a.get("n_candidatos", 0) for a in filtered)

    return {
        "party": party_id,
        "province": province,
        "n_records": len(filtered),
        "n_candidates_total": n_total,
        "avg_profesionalizacion": round(sum(scores) / len(scores), 1) if scores else 0,
        "aggregates": filtered,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Endpoints bajo /congruencia (usan el router con prefix)
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/map")
def get_congruence_map(
    party: str = Query(..., description="Nombre normalizado del partido"),
) -> Dict[str, Any]:
    """Retorna todos los cantones con sus scores de congruencia para un partido.

    Para cada cantón, calcula la congruencia promedio entre el vector de
    prioridades del cantón y los programas de todos los candidatos del partido
    en ese cantón.

    Args:
        party: Nombre normalizado del partido.

    Returns:
        Lista de cantones con scores de congruencia para el partido especificado.
    """
    priorities_data = _load_canton_priorities()
    programs_data = _load_candidate_programs()

    # Filtrar programas por partido
    party_programs = [p for p in programs_data if p.get("party_normalized") == party]
    if not party_programs:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron programas para el partido '{party}'",
        )

    results: List[Dict[str, Any]] = []
    for canton in priorities_data:
        canton_id = canton["canton_id"]
        canton_priorities = canton["priorities"]

        # Programas de candidatos del partido en este cantón
        canton_programs = [
            p for p in party_programs
            if p.get("provincia") == canton.get("provincia")
            and p.get("canton") == canton.get("canton")
        ]

        if not canton_programs:
            # Buscar candidatos del partido en la provincia si no hay en el cantón
            canton_programs = [
                p for p in party_programs
                if p.get("provincia") == canton.get("provincia")
            ]

        if canton_programs:
            scores = []
            for prog in canton_programs:
                congruence = _compute_congruence(canton_priorities, prog["program_scores"])
                scores.append(congruence["congruence_score"])
            avg_score = round(sum(scores) / len(scores), 1)
            max_score = round(max(scores), 1)
            min_score = round(min(scores), 1)
        else:
            avg_score = 0.0
            max_score = 0.0
            min_score = 0.0

        results.append({
            "canton_id": canton_id,
            "provincia": canton.get("provincia", ""),
            "canton": canton.get("canton", ""),
            "congruence_avg": avg_score,
            "congruence_max": max_score,
            "congruence_min": min_score,
            "n_candidates": len(canton_programs),
        })

    return {
        "party": party,
        "n_cantones": len(results),
        "cantones": results,
    }


@router.get("/ranking")
def get_congruence_ranking(
    canton_id: int = Query(..., description="ID del cantón"),
) -> Dict[str, Any]:
    """Ranking de candidatos por congruencia en un cantón específico.

    Ordena todos los candidatos que tienen programa según su score
    de congruencia con las prioridades del cantón, de mayor a menor.

    Args:
        canton_id: ID numérico del cantón.

    Returns:
        Ranking de candidatos con sus scores de congruencia.
    """
    priorities_data = _load_canton_priorities()
    programs_data = _load_candidate_programs()

    canton = _find_canton_by_id(canton_id, priorities_data)
    if canton is None:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el cantón con ID {canton_id}",
        )

    canton_priorities = canton["priorities"]
    ranking: List[Dict[str, Any]] = []

    for prog in programs_data:
        result = _compute_congruence(canton_priorities, prog["program_scores"])
        ranking.append({
            "candidate_id": prog.get("candidate_id"),
            "nombre": prog.get("nombre", ""),
            "party_normalized": prog.get("party_normalized", ""),
            "congruence_score": result["congruence_score"],
            "per_theme": result["per_theme"],
        })

    # Ordenar por congruencia descendente
    ranking.sort(key=lambda x: x["congruence_score"], reverse=True)

    return {
        "canton_id": canton_id,
        "canton": canton.get("canton", ""),
        "provincia": canton.get("provincia", ""),
        "n_candidates": len(ranking),
        "ranking": ranking,
    }


@router.get("/themes-graph")
def get_themes_graph() -> Dict[str, Any]:
    """Grafo de co-mention de temas.

    Retorna datos de grafo donde los nodos son los 10 temas y las aristas
    representan co-mentions entre temas en programas de candidatos.

    Returns:
        Estructura de grafo con nodos (temas) y aristas (co-mentions).
    """
    co_mentions = _load_co_mentions()

    nodes = [
        {
            "id": t["theme_id"],
            "label": t["label"],
            "keywords_count": len(t["keywords"]),
        }
        for t in THEMES
    ]

    edges = co_mentions

    # Calcular grado de cada nodo
    node_degree: Dict[str, int] = {t["theme_id"]: 0 for t in THEMES}
    for edge in edges:
        node_degree[edge["source"]] = node_degree.get(edge["source"], 0) + 1
        node_degree[edge["target"]] = node_degree.get(edge["target"], 0) + 1

    for node in nodes:
        node["degree"] = node_degree.get(node["id"], 0)

    return {
        "nodes": nodes,
        "edges": edges,
        "n_nodes": len(nodes),
        "n_edges": len(edges),
    }
