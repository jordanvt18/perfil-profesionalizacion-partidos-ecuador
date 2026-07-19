# Perfil profesionalización de partidos en Ecuador

Repositorio reproducible para calcular y analizar un índice de profesionalización de candidatos y partidos políticos en Ecuador, con ETL en Python, API REST en FastAPI, frontend interactivo y despliegue automatizado.

## Estructura del proyecto

- `src/etl/`: pipelines de ingesta, limpieza y cálculo del índice de profesionalización.
- `src/api/`: API REST con FastAPI para exponer datos de partidos, candidatos y participación.
- `web/`: frontend estático con HTML/CSS/JS, D3.js, Plotly.js y Leaflet.
- `scripts/`: scripts de descarga de datos del CNE y scraping de CVs públicos.
- `data/raw/`: datos crudos descargados (CNE, CVs).
- `data/processed/`: tablas normalizadas, índices y agregados en formato Parquet.
- `notebooks/analysis.ipynb`: análisis estadístico y visualizaciones de diagnóstico.
- `METHODOLOGY.md`: detalle metodológico del índice y supuestos.
- `docker-compose.yml` y `Dockerfile`: entorno reproducible para API y ETL.
- `.github/workflows/`: configuración de CI para lint, tests y deploy.

## Objetivo

- Calcular un índice de profesionalización por candidato (0-100) basado en grado académico y experiencia pública.
- Agregar el índice por partido y provincia.
- Visualizar interactivamente la relación entre profesionalización por partido y participación histórica por recinto/cantón/provincia.
