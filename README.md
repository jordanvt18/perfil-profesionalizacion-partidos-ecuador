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
│   ├── index.html                 # Frontend interactivo
│   ├── main.js                    # Lógica: mapa, gráficos, tabla
│   ├── styles.css                 # Estilos
│   └── demo-data.js               # Datos demo (modo sin backend)
├── scripts/
│   └── generate_realistic_data.py # Generador de datos sintéticos calibrados
├── data/demo/                     # Datos demo (JSON)
├── METHODOLOGY.md                 # Metodología detallada
└── docs/sources.md                # Fuentes oficiales
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

## ⚠️ Disclaimer

Proyecto académico y de investigación ciudadana. No constituye recomendación de voto ni evaluación definitiva de personas o partidos. Los datos demo son sintéticos y representativos — diseñados únicamente para fines de análisis y visualización.

## 📝 Licencia

MIT
