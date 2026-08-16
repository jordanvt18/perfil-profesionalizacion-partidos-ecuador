# Índice de profesionalización de candidatos – Elecciones Ecuador 2026 🇪🇨

Repositorio reproducible para calcular y analizar el **índice de profesionalización** de candidatos/as a Prefecturas, Alcaldías y Concejalías en las **Elecciones Seccionales Ecuador – Noviembre 2026**.

**Metodología**: 60% formación académica + 40% experiencia en servicio público → índice 0–100 por candidato/a, agregado por partido, provincia y dignidad.

> 🎯 **Objetivo**: Transparentar ante la ciudadanía la formación académica y experiencia pública de cada precandidato/a, por partido político, provincia y cantón, fomentando el debate informado previo a las elecciones seccionales de Noviembre 2026.

## ⚠️ Estado de los datos

**El CNE aún NO ha publicado el listado oficial de candidatos inscritos** para las Elecciones Seccionales de Noviembre 2026. Los datos en este repositorio son **sintéticos y representativos** — generados con base en:
- Partidos y movimientos políticos **habilitados por el CNE** para el periodo electoral 2025-2026
- **Movimientos locales reales documentados** (ej: Península Positiva L.69, Únete L.100, Amigo L.62 en Santa Elena)
- **Distribuciones educativas calibradas** según perfiles históricos de cada partido
- **Cantones y provincias oficiales** del Ecuador

> 📅 **Próximo paso:** Cuando el CNE publique el registro oficial de candidatos (estimado 45-60 días antes de las elecciones), los datos serán reemplazados con información real verificada. Consulte [cne.gob.ec](https://www.cne.gob.ec) para información oficial.

## 🗺️ Demo interactiva

[![GitHub Pages](https://img.shields.io/badge/Live_Demo-Ver_en_GitHub_Pages-00D9FF?style=flat-square&logo=github)](https://jordanvt18.github.io/perfil-profesionalizacion-partidos-ecuador/)

**275 precandidatos/as** (79 confirmados por medios + 196 sintéticos) sobre 15 partidos nacionales + movimientos locales, cubriendo las 24 provincias del Ecuador:
- **~111** precandidatos/as a Prefecturas
- **~164** precandidatos/as a Alcaldías
- Datos de Concejalías pendientes de publicación oficial del CNE

Mapa interactivo Leaflet, barras por nivel académico, serie histórica de participación (2017-2026), ranking de candidatos con detalle completo.

## 📂 Estructura

```
├── src/api/main.py                # API REST FastAPI
├── src/etl/                       # Pipelines ETL, cálculo del índice, NLP
├── web/
│   ├── index.html                 # Frontend profesionalización
│   ├── congruencia.html           # Frontend mapa de congruencia
│   ├── main.js                    # Lógica: mapa, gráficos, tabla
│   ├── styles.css                 # Estilos
│   └── demo-data.js               # Datos demo (modo sin backend)
├── scripts/
│   └── generate_realistic_data.py # Generador de datos sintéticos calibrados
├── data/demo/                     # Datos demo (JSON)
├── config/                        # Configuración de taxonomía y pesos
├── METHODOLOGY.md                 # Metodología detallada
├── docs/sources.md                # Fuentes oficiales (profesionalización)
├── docs/congruencia-sources.md    # Fuentes de datos para congruencia
└── README.md                      # Este documento
```

## 🧮 Metodología

| Componente | Peso | Fuente |
|---|---|---|
| **Score académico** | 60% | Grado máximo: Primaria=10, Secundaria=30, Técnico=50, Universitario=70, Posgrado=90 |
| **Score experiencia** | 40% | Años en cargos públicos × 2 (máx. 40 puntos) |

**Índice = 0.6 × score_académico + 0.4 × score_experiencia**

El índice se agrega por partido, provincia y dignidad como media aritmética.

## 🚀 Local

```bash
git clone https://github.com/jordanvt18/perfil-profesionalizacion-partidos-ecuador.git
cd perfil-profesionalizacion-partidos-ecuador

# Generar datos
python scripts/generate_realistic_data.py

# Servir frontend
cd web && python -m http.server 5500
```

Abre `http://localhost:5500/index.html`

---

# Mapa de Congruencia Programa-Votantes 🗳️📊

## Estado de datos (Elecciones Seccionales, 29-nov-2026)

La base de datos del mapa se actualizó el **16 de agosto de 2026** con las **candidaturas reales inscritas/proclamadas** para las elecciones seccionales (2–17 de agosto) y sus **ejes programáticos**, usando **solo fuentes confiables**: CNE, Primicias, El Universo, El Comercio, Expreso, Ecuavisa, El Telégrafo, Vistazo, Diario Correo y El Diario (verificación cruzada High/Medium).

- **Archivo de planes**: `data/plans/planes_trabajo.json` — candidaturas por plaza, partido/alianza, dignidad, ejes seccionales y nivel de confianza de cada registro.
- **Generador**: `scripts/generate_frontend_demo_data.py` integra las candidaturas High/Medium y excluye a los partidos **bloqueados por el CNE** (RC5, SUMA, ID, RETO, Amigo) de la cobertura sintética.
- **Fuentes documentadas**: `docs/congruencia-sources.md` (sección 0: proceso 2026, fuentes verificadas y conflictos pendientes).
- ⚠️ Toda candidatura individual es **preliminar** hasta el listado oficial del CNE del **9 de noviembre de 2026**; los planes seccionales completos no están publicados aún (son requisito CNE de inscripción).

## Objetivo

El **Mapa de Congruencia Programa-Votantes** es una herramienta de análisis político que mide el grado de **alineación entre las propuestas de los partidos políticos y las prioridades de la ciudadanía** en el Ecuador. Para cada partido, se construyen dos vectores — el **vector de programa** (qué propone el partido) y el **vector de prioridades** (qué demanda la ciudadanía) — y se calcula la **similitud coseno** entre ambos, produciendo un **índice de congruencia de 0 a 100**.

> 🎯 **Objetivo**: Cuantificar y visualizar qué tan bien representan los programas de gobierno las prioridades reales de los votantes, por partido, provincia y cantón, permitiendo a la ciudadanía comparar oferencia política vs. demanda ciudadana.

## Cálculo del puntaje de congruencia

### 1. Taxonomía de 10 temas

Se define una taxonomía de **10 dimensiones temáticas** que cubren el espectro de la agenda pública ecuatoriana:

| # | Tema | Descripción |
|---|------|-------------|
| 1 | **Empleo y economía** | Política laboral, crecimiento económico, inversión, emprendimiento |
| 2 | **Educación** | Cobertura, calidad educativa, infraestructura escolar, educación superior |
| 3 | **Salud** | Acceso a servicios médicos, infraestructura hospitalaria, medicamentos |
| 4 | **Seguridad ciudadana** | Delincuencia, políticas de seguridad, justicia, prevención |
| 5 | **Infraestructura y servicios** | Vías, agua potable, alcantarillado, electricidad, conectividad |
| 6 | **Medio ambiente** | Gestión ambiental, áreas protegidas, cambio climático, extracción |
| 7 | **Corrupción y transparencia** | Rendición de cuentas, lucha anti-corrupción, institucionalidad |
| 8 | **Agricultura y desarrollo rural** | Sector agropecuario, riego, crédito rural, soberanía alimentaria |
| 9 | **Turismo y cultura** | Promoción turística, patrimonio cultural, industrias creativas |
| 10 | **Derechos sociales** | Grupos de atención prioritaria, género, inclusión, pueblos y nacionalidades |

### 2. Vectores de programa y prioridades

Cada partido se representa con un **vector de programa** de 10 dimensiones:

```
program_vector = [econo, educ, salud, seguri, infras, ambien, corrup, agri, turis, derech]
```

Cada componente refleja la **proporción de menciones** del tema en el programa de gobierno, normalizada para que la suma del vector sea 1.

La ciudadanía se representa con un **vector de prioridades** de 10 dimensiones:

```
priority_vector = [econo, educ, salud, seguri, infras, ambien, corrup, agri, turis, derech]
```

Cada componente refleja la **proporción de ciudadanos** que identifican el tema como su principal prioridad, extraída de encuestas, sondeos municipales y datos proxy (peticiones ciudadanas, quejas municipales, redes sociales).

### 3. Similitud coseno → Índice 0–100

La congruencia se calcula como la **similitud coseno** entre ambos vectores:

```
congruencia = (program_vector · priority_vector) / (||program_vector|| × ||priority_vector||)
```

El resultado se escala de [-1, 1] a [0, 100]:

```
congruencia_100 = (congruencia + 1) / 2 × 100
```

Una congruencia de **100** indica alineación perfecta entre programa y prioridades; una de **0** indica oposición total.

## Pipeline ETL

El pipeline de extracción, transformación y carga sigue estos pasos:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Programas de    │    │  Encuestas y     │    │  Geo-indices     │
│  gobierno (PDF)  │    │  sondeos (CSV)   │    │  INEC (JSON)     │
└────────┬────────┘    └────────┬─────────┘    └────────┬────────┘
         │                      │                        │
         ▼                      ▼                        │
┌─────────────────┐    ┌──────────────────┐             │
│  NLP Extraction │    │  Prioridades     │             │
│  (spaCy + LDA)  │    │  Ciudadanas      │             │
│  → program_vec  │    │  → priority_vec  │             │
└────────┬────────┘    └────────┬─────────┘             │
         │                      │                        │
         └──────────┬───────────┘                        │
                    ▼                                    │
         ┌──────────────────┐                            │
         │  Cálculo de       │◄───────────────────────────┘
         │  Congruencia      │
         │  (cosine sim)     │
         └────────┬──────────┘
                  ▼
         ┌──────────────────┐
         │  Datos agregados │
         │  por partido,    │
         │  provincia, cantón│
         └──────────────────┘
```

**Pasos detallados:**

1. **Extracción de programas**: Descarga de PDFs de planes de gobierno desde sitios web de partidos. Procesamiento con `pdfminer.six` para extraer texto.
2. **Clasificación temática NLP**: Uso de `spaCy` (modelo `es_core_news_sm`) para tokenización y NER, coincidencia de palabras clave por tema, y refinamiento con LDA (Latent Dirichlet Allocation) vía `scikit-learn`.
3. **Construcción del vector de programa**: Conteo de menciones por tema → normalización a proporciones.
4. **Extracción de prioridades ciudadanas**: Procesamiento de encuestas (INEC, universidades, NGOs) y datos proxy (peticiones en portales municipales, redes sociales) → vector de prioridades.
5. **Cálculo de congruencia**: Similitud coseno entre `program_vector` y `priority_vector` → escala 0–100.
6. **Intervalos de confianza**: Bootstrap con 1000 repeticiones para estimar intervalos al 95%.
7. **Agregación territorial**: Resultados por partido, provincia, cantón y recinto electoral.

## Endpoints de la API para congruencia

La API FastAPI expone los siguientes endpoints para congruencia:

| Endpoint | Método | Parámetros | Descripción |
|----------|--------|------------|-------------|
| `/congruencia/parties` | GET | — | Lista de partidos con datos de congruencia |
| `/congruencia/themes` | GET | — | Taxonomía de 10 temas con descripciones |
| `/congruencia/scores` | GET | `party`, `province`, `canton` | Puntajes de congruencia filtrables |
| `/congruencia/program-vector` | GET | `party` | Vector de programa (10 dimensiones) por partido |
| `/congruencia/priority-vector` | GET | `province`, `canton` | Vector de prioridades ciudadanas territorial |
| `/congruencia/compare` | GET | `party`, `province` | Comparación lado a lado: programa vs. prioridades |
| `/congruencia/geo` | GET | `level` (provincia/cantón) | Datos geográficos para visualización en mapa |

**Ejemplo de uso:**

```bash
# Obtener congruencia de un partido en una provincia
curl "http://localhost:8000/congruencia/scores?party=CREO&province=Pichincha"

# Comparar vectores de programa y prioridades
curl "http://localhost:8000/congruencia/compare?party=CREO&province=Pichincha"
```

## Cómo ejecutar el frontend de congruencia

```bash
# Opción A: Servidor estático (modo demo, sin backend)
cd web && python -m http.server 5500
# Abrir http://localhost:5500/congruencia.html

# Opción B: Con backend FastAPI
pip install -r requirements.txt
uvicorn src.api.main:app --reload --port 8000
# Abrir http://localhost:8000/static/congruencia.html
```

El frontend de congruencia (`congruencia.html`) ofrece:
- 🗺️ **Mapa coroplético** de Ecuador por provincia/cantón mostrando el índice de congruencia
- 📊 **Gráfico de barras** comparando vector de programa vs. vector de prioridades
- 🏛️ **Selector de partido** para comparar múltiples ofertas políticas
- 📋 **Tabla de ranking** de partidos por congruencia

## Fuentes de datos y limitaciones

### Fuentes sugeridas

Las fuentes de datos para el módulo de congruencia se documentan en detalle en [`docs/congruencia-sources.md`](docs/congruencia-sources.md). Incluyen:
- **Programas de gobierno**: Sitios web de partidos, boletines del CNE, PDFs de campaña
- **Prioridades ciudadanas**: Encuestas INEC, sondeos universitarios, ONGs, sondeos municipales
- **Datos proxy**: Peticiones ciudadanas, portales de quejas municipales, redes sociales
- **Indicadores locales**: Pobreza, empleo, acceso a servicios (INEC)
- **Geografía electoral**: GeoJSON del CNE con recintos, cantones y provincias

### Limitaciones

- **Datos proxy**: En ausencia de encuestas directas, se utilizan datos proxy (quejas municipales, redes sociales) que pueden no representar fielmente las prioridades de toda la población.
- **Sesgo de taxonomía**: La taxonomía de 10 temas puede no capturar todas las dimensiones relevantes del debate político ecuatoriano (ej: migración, relaciones internacionales).
- **Extracción NLP**: La clasificación automática de temas puede cometer errores, especialmente con lenguaje político ambiguo o programas poco estructurados.
- **Cobertura desigual**: No todos los partidos publican programas completos; no todas las provincias tienen encuestas de opinión disponibles.
- **Temporalidad**: Las prioridades ciudadanas cambian con el ciclo electoral y eventos coyunturales; los datos deben actualizarse periódicamente.
- **Escalado de coseno**: La transformación de [-1,1] a [0,100] puede comprimir el rango útil; interpretar con cautela.
- **El índice no mide calidad**: Un partido puede ser congruente (mencionar lo que la gente quiere) pero tener propuestas de baja calidad. La congruencia mide alineación temática, no idoneidad de políticas.

## ⚠️ Disclaimer

Proyecto académico y de investigación ciudadana. No constituye recomendación de voto ni evaluación definitiva de personas o partidos. Los datos demo son sintéticos y representativos — diseñados únicamente para fines de análisis y visualización.

## 📝 Licencia

MIT
