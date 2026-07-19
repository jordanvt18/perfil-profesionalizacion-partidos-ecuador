# Perfil profesionalización de partidos en Ecuador

Repositorio reproducible para calcular y analizar un índice de profesionalización de candidatos y partidos políticos en Ecuador, con ETL en Python, API REST en FastAPI, frontend interactivo y despliegue automatizado.

## Estructura del proyecto

- `src/etl/`: pipelines de ingesta, limpieza y cálculo del índice de profesionalización.
- `src/api/`: API REST con FastAPI para exponer datos de partidos, candidatos y participación.
- `web/`: frontend estático con HTML/CSS/JS, D3.js, Plotly.js y Leaflet.
- `web/demo-data.js`: datos de ejemplo para la demo pública en GitHub Pages (sin necesidad de API real).
- `scripts/`: scripts de descarga de datos del CNE y scraping de CVs públicos.
- `data/raw/`: datos crudos descargados (CNE, CVs).
- `data/processed/`: tablas normalizadas, índices y agregados en formato Parquet.
- `notebooks/analysis.ipynb`: análisis estadístico y visualizaciones de diagnóstico.
- `METHODOLOGY.md`: detalle metodológico del índice y supuestos.
- `docs/sources.md`: registro de fuentes oficiales, fechas de descarga y licencias.
- `SECURITY.md`: guía de buenas prácticas de seguridad y privacidad.
- `.env.example`: ejemplo de configuración de entorno sin credenciales sensibles.
- `docker-compose.yml` y `Dockerfile`: entorno reproducible para API y ETL.
- `.github/workflows/`: configuración de CI para lint, tests y deploy.

## Objetivo

- Calcular un índice de profesionalización por candidato (0-100) basado en grado académico y experiencia pública.
- Agregar el índice por partido y provincia.
- Visualizar interactivamente la relación entre profesionalización por partido y participación histórica por recinto/cantón/provincia.

## Demo pública en GitHub Pages (modo seguro)

La demo pública en GitHub Pages utiliza datos de ejemplo definidos en `web/demo-data.js`. De esta forma:

- No se exponen credenciales ni servicios internos.
- Se puede mostrar la interacción completa (mapa, selectores, gráficos) sin depender de la API real.

Cuando el sitio se despliegue en GitHub Pages (dominio `github.io`):

- El frontend detectará que no está en `localhost` y funcionará en **modo demo** usando `demoAggregates`, `demoCandidates` y `demoTurnout`.

## Demo local con API real

Para ver la demo interactiva con la API real en tu máquina:

1. Clona el repositorio:

   ```bash
   git clone https://github.com/jordanvt18/perfil-profesionalizacion-partidos-ecuador.git
   cd perfil-profesionalizacion-partidos-ecuador
   ```

2. Copia el archivo `.env.example` a `.env` y ajusta la configuración según tu entorno.

3. Levanta la API y la base de datos con Docker:

   ```bash
   docker-compose up --build
   ```

   Esto iniciará FastAPI en `http://localhost:8000` (detectado automáticamente por `web/main.js` cuando el hostname es `localhost`).

4. Sirve el frontend estático desde la carpeta `web/`:

   ```bash
   cd web
   python -m http.server 5500
   ```

5. Abre la demo en tu navegador:

   - URL: `http://localhost:5500/index.html`
   - Selecciona partido, año y provincia en el panel derecho para actualizar el mapa Leaflet, las barras de niveles académicos y la serie temporal de participación.

> Nota: asegúrate de haber cargado datos reales en la base de datos (candidatos, turnout, agregados) antes de usar la demo para análisis sustantivo.

## Seguridad y privacidad

Consulta `SECURITY.md` para revisar las buenas prácticas recomendadas sobre manejo de credenciales, scraping respetuoso y anonimización de datos sensibles.
