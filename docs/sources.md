# Fuentes de datos y referencias

Este documento registra todas las fuentes oficiales y públicas utilizadas. Las URLs están verificadas para las elecciones generales Ecuador 2025.

## 1. Consejo Nacional Electoral (CNE)

### 1.1 Portales oficiales

| Tipo de dato | URL oficial | Fecha de descarga | Estado |
|--------------|------------|-------------------|--------|
| CNE – Portal principal | `https://www.cne.gob.ec` | 2025-07 | Activo |
| CNE – Datos abiertos | `https://app01.cne.gob.ec` | 2025-07 | Activo |
| Resultados elecciones 2025 | `https://resultados2025.cne.gob.ec` | 2025-07 | Activo |

### 1.2 Descargas programáticas de datos

Los scripts de descarga (`scripts/download_cne.py`) se configuran para:
- Acceder a los endpoints oficiales del CNE
- Descargar padrones, actas y resultados en formato tabular
- Respetar rate limiting y términos de uso

### 1.3 Datos de participación histórica

Los datos de participación utilizados en la demo se basan en tendencias históricas reales reportadas por el CNE para las elecciones de 2017, 2021, 2023 y 2025.

## 2. Perfiles educativos de partidos

Los perfiles educativos de cada partido se basan en:
- Datos históricos del INEC sobre niveles educativos por provincia
- Patrones de reclutamiento documentados en investigación académica
- Distribuciones ajustadas según el perfil ideológico y base social de cada partido

## 3. Indicadores socioeconómicos (INEC)

| Indicador | Nivel geográfico | URL | Notas |
|-----------|------------------|-----|-------|
| Población provincial | Provincia | `https://www.ecuadorencifras.gob.ec` | Datos censales 2022 |
| Educación promedio | Provincia/Cantón | `https://www.ecuadorencifras.gob.ec` | Para controles adicionales |

## 4. Fuentes de la metodología

| Fuente | Referencia |
|--------|-----------|
| Matland & Studlar (2004) | "Determinants of Legislative Turnover" – sistemas electorales y profesionalización |
| Norris & Lovenduski (1995) | "Political Recruitment" – modelos de selección de candidatos |
| Alcántara Sáez (2012) | "El oficio de político" – profesionalización política en América Latina |
| Freidenberg & Pachano (2016) | "El sistema político ecuatoriano" – partidos y candidaturas en Ecuador |

## 5. Licencias y términos de uso

- Los datos del CNE e INEC son de acceso público para fines académicos
- Los CVs solo se obtienen de fuentes donde los candidatos han publicado información voluntariamente
- Los datos demo generados no contienen información personal real
- Toda información se trata según lo establecido en `SECURITY.md`
