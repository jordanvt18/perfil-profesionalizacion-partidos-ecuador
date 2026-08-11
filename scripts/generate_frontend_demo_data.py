#!/usr/bin/env python3
"""
Genera web/congruencia-demo-data.js con los nombres de export correctos
que espera congruencia.js: TEMAS, PARTIDOS, CANDIDATOS, CO_MENTION_MATRIX,
THEME_GAPS, YEARS.
"""
import json, random, sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.build_hybrid_data import CANTONES

random.seed(20260810)

# ─── 10 Temas (nombres cortos para mostrar) ───
TEMAS = [
    "Salud",
    "Educación",
    "Agua y Saneamiento",
    "Movilidad y Transporte",
    "Empleo y Economía",
    "Seguridad Ciudadana",
    "Vivienda",
    "Ambiente",
    "Transparencia",
    "Presupuesto",
]

THEME_IDS = [
    "salud", "educacion", "agua", "movilidad", "empleo",
    "seguridad", "vivienda", "ambiente", "transparencia", "presupuesto",
]

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

# ─── Perfiles de programas por partido (tema_id → score) ───
PARTY_PROFILES = {
    "ADN (Accion Democratica Nacional)": {"seguridad": 0.22, "empleo": 0.16, "educacion": 0.12, "salud": 0.10, "movilidad": 0.10, "presupuesto": 0.08, "transparencia": 0.07, "vivienda": 0.06, "ambiente": 0.05, "agua": 0.04},
    "Revolucion Ciudadana (RC5)": {"salud": 0.16, "educacion": 0.14, "empleo": 0.12, "presupuesto": 0.10, "seguridad": 0.10, "movilidad": 0.08, "vivienda": 0.08, "agua": 0.08, "transparencia": 0.07, "ambiente": 0.07},
    "Partido Social Cristiano (PSC)": {"seguridad": 0.20, "empleo": 0.15, "movilidad": 0.12, "presupuesto": 0.10, "salud": 0.08, "vivienda": 0.08, "educacion": 0.08, "transparencia": 0.07, "ambiente": 0.07, "agua": 0.05},
    "Movimiento Construye": {"transparencia": 0.16, "ambiente": 0.14, "educacion": 0.12, "empleo": 0.10, "salud": 0.10, "seguridad": 0.08, "movilidad": 0.08, "agua": 0.08, "vivienda": 0.07, "presupuesto": 0.07},
    "Pachakutik": {"ambiente": 0.18, "agua": 0.14, "educacion": 0.12, "transparencia": 0.10, "salud": 0.10, "empleo": 0.08, "vivienda": 0.08, "presupuesto": 0.07, "seguridad": 0.07, "movilidad": 0.06},
    "Movimiento CREO": {"empleo": 0.18, "presupuesto": 0.12, "movilidad": 0.12, "seguridad": 0.10, "transparencia": 0.10, "educacion": 0.08, "salud": 0.08, "ambiente": 0.06, "vivienda": 0.06, "agua": 0.10},
    "Avanza": {"empleo": 0.16, "educacion": 0.12, "movilidad": 0.12, "salud": 0.10, "presupuesto": 0.10, "seguridad": 0.10, "agua": 0.08, "transparencia": 0.08, "vivienda": 0.07, "ambiente": 0.07},
    "Izquierda Democratica (ID)": {"transparencia": 0.16, "educacion": 0.14, "salud": 0.12, "ambiente": 0.10, "empleo": 0.10, "presupuesto": 0.08, "seguridad": 0.08, "agua": 0.08, "movilidad": 0.07, "vivienda": 0.07},
}

# ─── Perfiles de prioridades por cantón ───
CANTON_PRIORITY_PROFILES = {
    "Guayaquil": {"seguridad": 0.28, "empleo": 0.20, "movilidad": 0.15, "salud": 0.12, "educacion": 0.08, "vivienda": 0.07, "ambiente": 0.04, "transparencia": 0.03, "presupuesto": 0.02, "agua": 0.01},
    "Duran": {"seguridad": 0.25, "empleo": 0.18, "vivienda": 0.15, "movilidad": 0.12, "salud": 0.10, "educacion": 0.08, "agua": 0.05, "ambiente": 0.03, "transparencia": 0.02, "presupuesto": 0.02},
    "Samborondon": {"seguridad": 0.22, "movilidad": 0.18, "ambiente": 0.12, "empleo": 0.10, "presupuesto": 0.08, "transparencia": 0.08, "salud": 0.07, "educacion": 0.07, "vivienda": 0.05, "agua": 0.03},
    "Quito": {"movilidad": 0.22, "seguridad": 0.18, "ambiente": 0.12, "empleo": 0.10, "transparencia": 0.08, "salud": 0.08, "educacion": 0.08, "vivienda": 0.06, "presupuesto": 0.05, "agua": 0.03},
    "Cuenca": {"ambiente": 0.18, "educacion": 0.15, "movilidad": 0.12, "transparencia": 0.10, "salud": 0.10, "seguridad": 0.10, "empleo": 0.08, "agua": 0.07, "vivienda": 0.05, "presupuesto": 0.05},
    "Portoviejo": {"agua": 0.20, "empleo": 0.16, "vivienda": 0.12, "seguridad": 0.10, "salud": 0.10, "educacion": 0.10, "movilidad": 0.08, "ambiente": 0.05, "presupuesto": 0.05, "transparencia": 0.04},
    "Manta": {"empleo": 0.20, "agua": 0.15, "seguridad": 0.12, "movilidad": 0.10, "salud": 0.10, "vivienda": 0.10, "educacion": 0.08, "ambiente": 0.06, "presupuesto": 0.05, "transparencia": 0.04},
    "Ambato": {"empleo": 0.16, "movilidad": 0.14, "educacion": 0.12, "salud": 0.10, "seguridad": 0.10, "ambiente": 0.08, "agua": 0.08, "vivienda": 0.08, "presupuesto": 0.07, "transparencia": 0.07},
    "Loja": {"educacion": 0.18, "agua": 0.14, "empleo": 0.12, "seguridad": 0.10, "salud": 0.10, "movilidad": 0.08, "ambiente": 0.08, "vivienda": 0.08, "presupuesto": 0.06, "transparencia": 0.06},
    "Machala": {"empleo": 0.18, "seguridad": 0.14, "salud": 0.12, "movilidad": 0.10, "agua": 0.10, "educacion": 0.10, "vivienda": 0.06, "ambiente": 0.06, "transparencia": 0.07, "presupuesto": 0.07},
    "Ibarra": {"empleo": 0.16, "movilidad": 0.12, "seguridad": 0.12, "educacion": 0.10, "salud": 0.10, "ambiente": 0.08, "agua": 0.08, "vivienda": 0.08, "presupuesto": 0.08, "transparencia": 0.08},
    "Babahoyo": {"agua": 0.18, "empleo": 0.14, "movilidad": 0.12, "salud": 0.10, "educacion": 0.10, "seguridad": 0.10, "vivienda": 0.06, "ambiente": 0.07, "presupuesto": 0.07, "transparencia": 0.06},
    "Quevedo": {"empleo": 0.18, "seguridad": 0.14, "movilidad": 0.12, "salud": 0.10, "agua": 0.10, "educacion": 0.08, "vivienda": 0.08, "ambiente": 0.05, "presupuesto": 0.08, "transparencia": 0.07},
    "Santo Domingo": {"seguridad": 0.20, "movilidad": 0.15, "empleo": 0.12, "salud": 0.10, "agua": 0.10, "educacion": 0.08, "vivienda": 0.08, "ambiente": 0.05, "presupuesto": 0.07, "transparencia": 0.05},
    "Esmeraldas": {"salud": 0.18, "empleo": 0.16, "ambiente": 0.12, "seguridad": 0.10, "educacion": 0.10, "vivienda": 0.08, "agua": 0.08, "movilidad": 0.06, "presupuesto": 0.06, "transparencia": 0.06},
}


def vec_to_array(vec):
    """Convierte dict {tema_id: score} → array de 10 valores en orden de THEME_IDS"""
    return [round(vec.get(tid, 0.0), 4) for tid in THEME_IDS]


def add_noise(vec, amt=0.02):
    """Añade ruido aleatorio a un vector"""
    return {k: max(0.01, min(1.0, v + random.uniform(-amt, amt))) for k, v in vec.items()}


def cosine_sim(a, b):
    import math
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return round(dot / (na * nb) * 100, 1)


# ─── Generar candidatos ───
CANDIDATOS = []
cid = 0

# Nombres realistas
from scripts.build_hybrid_data import REAL as REAL_CANDS

for prov, cantones in CANTONES.items():
    for canton, (lat, lon) in cantones.items():
        # Perfil de prioridad del cantón
        if canton in CANTON_PRIORITY_PROFILES:
            prio = add_noise(CANTON_PRIORITY_PROFILES[canton], 0.015)
        else:
            # Genérico con variación
            base_vals = [random.uniform(0.05, 0.15) for _ in range(10)]
            # Resaltar 3 temas
            for idx in random.sample(range(10), 3):
                base_vals[idx] = random.uniform(0.15, 0.25)
            prio = {THEME_IDS[i]: round(base_vals[i], 4) for i in range(10)}

        prio_array = vec_to_array(prio)

        # 2-4 candidatos por cantón (de partidos diferentes)
        n_cands = random.randint(2, 4)
        selected_parties = random.sample(PARTIES, min(n_cands, len(PARTIES)))

        for party in selected_parties:
            cid += 1
            prog = add_noise(PARTY_PROFILES[party], 0.02)
            prog_array = vec_to_array(prog)
            congruence = cosine_sim(prog_array, prio_array)

            # Buscar nombre real si existe
            real_cand = None
            for rc in REAL_CANDS:
                if rc["provincia"] == prov and rc["canton"] == canton and rc["party"] == party:
                    real_cand = rc
                    break

            if real_cand:
                nombre = real_cand["nombre"]
                dignidad = real_cand["dignidad"]
            else:
                nombres_m = ["Carlos", "Andrés", "Juan", "Luis", "Pedro", "José", "Fernando", "Javier", "Diego", "Roberto", "Marcelo", "Wilson", "Byron", "Gustavo", "Santiago", "César", "Patricio", "Esteban", "Lenin", "Rafael"]
                nombres_f = ["María", "Rosa", "Ana", "Carmen", "Isabel", "Patricia", "Gabriela", "Andrea", "Verónica", "Mónica", "Lorena", "Paola", "Cristina", "Diana", "Marcela", "Ximena", "Cecilia", "Viviana", "Mariana", "Daniela"]
                apellidos = ["Moreno", "Zambrano", "Vera", "Torres", "García", "López", "Pérez", "Sánchez", "Salazar", "Reyes", "Cevallos", "Mendoza", "Jaramillo", "Alvarado", "Castro", "Guerrero", "Espinoza", "Ortega", "León", "Valencia", "Lara", "Muñoz", "Flores", "Molina", "Ortiz", "Herrera", "Andrade", "Suárez", "Pazmiño", "Cedeño"]
                n = random.choice(nombres_f) if random.random() < 0.4 else random.choice(nombres_m)
                nombre = f"{n} {random.choice(apellidos)} {random.choice(apellidos)}"
                dignidad = random.choice(["Alcalde/sa", "Prefecto/a"])

            CANDIDATOS.append({
                "id": cid,
                "nombre": nombre,
                "partido": party,
                "provincia": prov,
                "canton": canton,
                "lat": round(lat + random.uniform(-0.015, 0.015), 4),
                "lon": round(lon + random.uniform(-0.015, 0.015), 4),
                "dignidad": dignidad,
                "congruence": congruence,
                "priority_vector": prio_array,
                "program_vector": prog_array,
                "year": 2026,
            })

# ─── Co-mention matrix (10×10) ───
CO_MENTION_MATRIX = []
for i in range(10):
    row = []
    for j in range(10):
        if i == j:
            row.append(0)
        else:
            # Temas relacionados: salud-educacion, agua-ambiente, seguridad-empleo, etc.
            base = random.uniform(15, 60)
            if (i, j) in [(0, 1), (1, 0), (2, 7), (7, 2), (4, 5), (5, 4), (3, 9), (9, 3)]:
                base = random.uniform(50, 80)
            row.append(int(base))
    CO_MENTION_MATRIX.append(row)

# ─── Theme gaps (demanda - oferta promedio) ───
# Calcular oferta promedio y demanda promedio por tema
oferta_prom = [0.0] * 10
demanda_prom = [0.0] * 10
for c in CANDIDATOS:
    for i in range(10):
        oferta_prom[i] += c["program_vector"][i]
        demanda_prom[i] += c["priority_vector"][i]

n = len(CANDIDATOS)
oferta_prom = [round(v / n, 4) for v in oferta_prom]
demanda_prom = [round(v / n, 4) for v in demanda_prom]

THEME_GAPS = []
for i in range(10):
    THEME_GAPS.append({
        "tema": TEMAS[i],
        "oferta": oferta_prom[i],
        "demanda": demanda_prom[i],
        "gap": round(demanda_prom[i] - oferta_prom[i], 4),
    })

YEARS = [2019, 2023, 2026]

# ─── Escribir JS ───
repo_root = Path(__file__).parent.parent
js_path = repo_root / "web" / "congruencia-demo-data.js"

with open(js_path, "w", encoding="utf-8") as f:
    f.write("// Mapa de Congruencia Política — Datos Demo\n")
    f.write(f"// Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"// {len(PARTIES)} partidos × {len(CANTONES)} provincias\n")
    f.write(f"// {len(CANDIDATOS)} candidatos con scores de congruencia\n\n")

    f.write("// Los 10 temas prioritarios (dimensiones de los vectores)\n")
    f.write("export const TEMAS = ")
    json.dump(TEMAS, f, ensure_ascii=False)
    f.write(";\n\n")

    f.write("// Partidos políticos\n")
    f.write("export const PARTIDOS = ")
    json.dump(PARTIES, f, ensure_ascii=False)
    f.write(";\n\n")

    f.write("// Candidatos con vectores y scores de congruencia\n")
    f.write("export const CANDIDATOS = ")
    json.dump(CANDIDATOS, f, ensure_ascii=False)
    f.write(";\n\n")

    f.write("// Matriz de co-mentions de temas (10×10)\n")
    f.write("export const CO_MENTION_MATRIX = ")
    json.dump(CO_MENTION_MATRIX, f, ensure_ascii=False)
    f.write(";\n\n")

    f.write("// Brecha entre oferta (programas) y demanda (prioridades ciudadanas) por tema\n")
    f.write("export const THEME_GAPS = ")
    json.dump(THEME_GAPS, f, ensure_ascii=False)
    f.write(";\n\n")

    f.write("// Años electorales disponibles\n")
    f.write("export const YEARS = ")
    json.dump(YEARS, f, ensure_ascii=False)
    f.write(";\n")

print(f"Guardado: {js_path}")
print(f"  Temas: {len(TEMAS)}")
print(f"  Partidos: {len(PARTIES)}")
print(f"  Candidatos: {len(CANDIDATOS)}")
print(f"  Congruencia promedio: {sum(c['congruence'] for c in CANDIDATOS)/len(CANDIDATOS):.1f}")
print(f"  Congruencia min: {min(c['congruence'] for c in CANDIDATOS):.1f}")
print(f"  Congruencia max: {max(c['congruence'] for c in CANDIDATOS):.1f}")
