# Fuentes de datos y referencias

Este documento registra todas las fuentes oficiales y públicas utilizadas para construir el índice de profesionalización y los análisis de participación electoral en Ecuador.

> **Importante**: completa las tablas con las URLs y fechas reales de descarga antes de publicar resultados o compartir este repositorio como referencia académica.

## 1. Consejo Nacional Electoral (CNE)

### 1.1 Resultados electorales por recinto/cantón/provincia

| Tipo de dato | Descripción | URL oficial | Fecha de descarga | Licencia / condiciones |
|--------------|------------|------------|-------------------|------------------------|
| Resultados por recinto | Resultados detallados por junta y recinto electoral (actas escaneadas o datos tabulares) | `https://...` | `AAAA-MM-DD` | Uso académico, respetando términos del CNE |
| Resultados por cantón | Totales por cantón y provincia | `https://...` | `AAAA-MM-DD` | Uso académico |
| Resultados por provincia | Totales provinciales por elección | `https://...` | `AAAA-MM-DD` | Uso académico |

### 1.2 Padrones electorales históricos

| Tipo de dato | Descripción | URL oficial | Fecha de descarga | Licencia / condiciones |
|--------------|------------|------------|-------------------|------------------------|
| Padrón por recinto | Padrón de electores por recinto y junta | `https://...` | `AAAA-MM-DD` | Uso académico |
| Padrón por cantón | Padrón agregado por cantón y provincia | `https://...` | `AAAA-MM-DD` | Uso académico |

> Completa estos campos con las rutas oficiales del CNE (portal institucional, datos abiertos, secciones de transparencia) y revisa si existen restricciones de uso o redistribución.

## 2. Currículums públicos de candidatos

Los CVs públicos se obtienen únicamente de fuentes oficiales o páginas donde los candidatos han publicado voluntariamente su información profesional.

### 2.1 Portales oficiales y transparencia

| Tipo de fuente | Descripción | URL base | Fecha de crawling | Notas |
|----------------|------------|---------|--------------------|-------|
| Portal de Asamblea Nacional | Fichas de asambleístas con CV | `https://...` | `AAAA-MM-DD` | Respetar robots.txt y límites de carga |
| Portal de transparencia de institución X | Hojas de vida de autoridades | `https://...` | `AAAA-MM-DD` | Priorizar descarga manual si hay restricciones |

### 2.2 Sitios personales o partidarios

| Tipo de fuente | Descripción | URL base | Fecha de crawling | Notas |
|----------------|------------|---------|--------------------|-------|
| Página oficial del partido | Sección "Nuestros candidatos" | `https://...` | `AAAA-MM-DD` | Confirmar consentimiento implícito de publicación |
| Sitio personal del candidato | CV o biografía detallada | `https://...` | `AAAA-MM-DD` | Evitar información sensible no relevante |

> El scraper descrito en `scripts/scrape_cvs.py` debe respetar siempre robots.txt, aplicar rate limiting y registrar la fecha exacta de ejecución.

## 3. Indicadores socioeconómicos (INEC)

Controles socioeconómicos por provincia/cantón se obtienen del Instituto Nacional de Estadística y Censos (INEC).

| Indicador | Descripción | Nivel geográfico | URL oficial / catálogo | Fecha de descarga | Notas |
|-----------|------------|------------------|------------------------|-------------------|-------|
| PIB per cápita | PIB per cápita en USD o moneda local | Provincia / Cantón | `https://...` | `AAAA-MM-DD` | Alinear años con periodo electoral |
| Tasa de pobreza | Porcentaje de población en pobreza | Provincia / Cantón | `https://...` | `AAAA-MM-DD` | Documentar metodología del INEC |
| Educación promedio | Años de escolaridad promedio | Provincia / Cantón | `https://...` | `AAAA-MM-DD` | Útil como control adicional |

## 4. Geometrías y mapas

Si se utilizan shapefiles o GeoJSON para provincias/cantones:

| Fuente | Tipo | URL / ruta | Fecha de descarga | Licencia |
|--------|------|-----------|-------------------|----------|
| INEC / Geoestadística | Shapefile de provincias y cantones | `https://...` | `AAAA-MM-DD` | Ver licencia de uso |
| Otra fuente oficial | GeoJSON simplificado | `https://...` | `AAAA-MM-DD` | Asegurar compatibilidad con Leaflet |

## 5. Otros recursos

Incluye aquí cualquier fuente adicional relevante (papers, informes académicos, blogs técnicos) utilizada para contextualizar o validar la metodología.

| Tipo | Descripción | Referencia / URL | Notas |
|------|------------|------------------|-------|
| Paper académico | Estudio sobre profesionalización política | `https://...` | Citar adecuadamente |
| Blog técnico | Tutorial de extracción de CVs con spaCy | `https://...` | Solo como referencia técnica |

---

Este archivo `docs/sources.md` debe mantenerse actualizado cada vez que se incorporen nuevos datos o se actualicen descargas. Es parte central de la trazabilidad académica del proyecto.