# Fuentes de datos sugeridas – Mapa de Congruencia Programa-Votantes

Este documento registra las fuentes de datos sugeridas y disponibles para construir el mapa de congruencia entre programas de gobierno y prioridades ciudadanas en el Ecuador.

---

## 1. Programas de gobierno de partidos

### 1.1. Sitios web de partidos políticos

Los planes de gobierno suelen publicarse en los sitios web oficiales de cada partido o movimiento político durante la campaña electoral.

| Partido / Movimiento | URL sugerida | Formato esperado | Notas |
|----------------------|-------------|------------------|-------|
| RCN | `https://www.rcn.gob.ec` | PDF | Publicar alrededor de 60 días antes de elecciones |
| correísmo (RC) | Sitio oficial del movimiento | PDF | Verificar disponibilidad |
| PSC | `https://www.psc-ecuador.com` | PDF | Partido Social Cristiano |
| CREO | `https://creo.ec` | PDF | Movimiento CREO |
| ID | `https://izquierdademocratica.ec` | PDF | Izquierda Democrática |
| UNES | Sitio oficial del movimiento | PDF | Unión Estatus |
| MUPP-NP | Sitio oficial del movimiento | PDF | Movimiento Unidad Plurinacional Pachakutik |
| Mover (ex PAIS) | Sitio oficial del movimiento | PDF | Alianza PAIS / Mover |
| SUMA | `https://sumaproject.com` | PDF | Movimiento SUMA |
| Movimientos locales | Sitios provinciales | PDF | Ej: Península Positiva L.69, Únete L.100 |

> ⚠️ **Nota**: Las URLs pueden cambiar. Verificar disponibilidad 60-90 días antes de las elecciones seccionales de Noviembre 2026.

### 1.2. Boletines del CNE

El Consejo Nacional Electoral (CNE) publica boletines oficiales con información de campañas:

| Tipo de dato | URL | Formato | Estado |
|--------------|-----|---------|--------|
| CNE – Portal principal | `https://www.cne.gob.ec` | HTML/PDF | Activo |
| CNE – Datos abiertos | `https://app01.cne.gob.ec` | CSV/JSON | Activo |
| Boletines de campañas | `https://www.cne.gob.ec/?page_id=126` | PDF | Verificar en temporada electoral |
| Registro de slogans y propuestas | CNE – Secretaría Técnica | PDF | Solicitar vía acceso a información pública |

### 1.3. Archivos PDF de campaña

- **Observatorio Político Ecuador** (Universidad de las Américas): Archiva planes de gobierno históricos.
- **Corte Constitucional del Ecuador**: Algunas propuestas llegan como anexos en consultas constitucionales.
- **Medios de comunicación**: El Comercio, El Universo, La Hora suelen publicar resúmenes de programas en sus portales electorales.

---

## 2. Encuestas de prioridades ciudadanas

### 2.1. INEC (Instituto Nacional de Estadística y Censos)

| Indicador | Nivel geográfico | URL | Frecuencia | Notas |
|-----------|------------------|-----|------------|-------|
| Encuesta Nacional de Empleo (ENEMDU) | Nacional / Provincial | `https://www.ecuadorencifras.gob.ec` | Trimestral | Incluye módulos de percepción |
| Encuesta de Condiciones de Vida (ECV) | Nacional / Provincial | `https://www.ecuadorencifras.gob.ec` | Quinquenal | Datos de pobreza, servicios |
| Censo de Población 2022 | Cantonal | `https://www.ecuadorencifras.gob.ec` | Decenal | Datos sociodemográficos base |

### 2.2. Universidades y centros de investigación

| Institución | Tipo de encuesta | Cobertura | URL | Notas |
|-------------|------------------|-----------|-----|-------|
| CEDATOS | Encuestas de opinión | Nacional | `https://www.cedatos.com.ec` | Referente histórico en Ecuador |
| Market | Encuestas de opinión | Nacional / Quito-Guayaquil | `https://www.market.com.ec` | Barómetro político |
| Perfiles de Opinión | Encuestas de opinión | Nacional | `https://www.perfilesdeopinion.com.ec` | Especializados en política |
| Facultad Latinoamericana de Ciencias Sociales (FLACSO) | Investigación académica | Provincial | `https://www.flacso.edu.ec` | Estudios temáticos |
| Universidad de las Américas (UDLA) | Observatorio Político | Nacional | `https://www.udla.edu.ec` | Análisis electoral |

### 2.3. ONGs y organizaciones internacionales

| Organización | Tipo de dato | Cobertura | URL | Notas |
|-------------|--------------|-----------|-----|-------|
| Latinobarómetro | Encuesta de opinión pública | Nacional (países LATAM) | `https://www.latinobarometro.org` | Datos anuales, incluye Ecuador |
| Corporación Latinobarómetro | Percepción de problemas | Nacional | `https://www.latinobarometro.org` | Pregunta: "cuál es el principal problema del país" |
| V-Dem (Varieties of Democracy) | Índices de democracia | Nacional | `https://www.v-dem.net` | Datos comparados |
| Freedom House | Libertades civiles y políticas | Nacional | `https://freedomhouse.org` | Informes anuales |

### 2.4. Sondeos municipales

- **Gobiernos autónomos descentralizados (GAD)**: Algunos municipios realizan sondeos de satisfacción ciudadana. Solicitar vía acceso a información pública (Ley COA).
- **Asociación de Municipalidades del Ecuador (AME)**: `https://www.ame.gob.ec` — puede aggregar datos de sondeos locales.
- **Consejo Nacional de Competencias (CNC)**: `https://www.competencias.gob.ec` — datos sobre descentralización y necesidades territoriales.

---

## 3. Fuentes proxy para prioridades ciudadanas

Cuando no existen encuestas directas, se utilizan datos proxy para inferir prioridades:

### 3.1. Peticiones ciudadanas y quejas municipales

| Fuente | Tipo de dato | Cobertura | URL | Notas |
|--------|--------------|-----------|-----|-------|
| Portal de Quejas Ecuador | Peticiones y reclamos | Nacional | `https://www.quejas.ec` | Geolocalizadas por ciudad |
| Sistema de Contacto Ciudadano (Quito) | Peticiones 123 | Quito | `https://www.quito.gob.ec` | App y portal web |
| SAC Guayaquil | Servicio de Atención Ciudadana | Guayaquil | `https://www.guayaquil.gob.ec` | Reclamos por categoría |
| Portal de Transparencia GAD | Peticiones | Variable | Portales municipales | Solicitar vía Ley COA |

### 3.2. Redes sociales geolocalizadas

| Plataforma | Tipo de dato | Metodología | Limitaciones |
|-----------|--------------|-------------|--------------|
| X (Twitter) | Menciones geolocalizadas | API v2 + filtro geográfico Ecuador | Sesgo urbano, población joven |
| Facebook | Menciones en grupos locales | CrowdTangle / Meta Content Library | Requiere acceso académico |
| WhatsApp | Mensajes en grupos públicos | Análisis de forwarded messages | Difícil de geolocalizar; cuestiones éticas |
| TikTok | Tendencias y hashtags locales | API Research | Nuevo, sesgo juvenil fuerte |

### 3.3. Petitorios y asambleas comunitarias

- **Asambleas parroquiales**: Actas de asambleas parroquiales rurales pueden documentar prioridades comunitarias.
- **Uniones de organizaciones campesinas e indígenas**: CONAIE, FEINE, FENOCIN — plataformas de lucha documentan prioridades.
- **Cartas de necesidades**: Gobiernos parroquiales suelen elevar cartas de necesidades a gobiernos provinciales.

---

## 4. Indicadores socioeconómicos locales

Para contextualizar y validar las prioridades inferidas, se utilizan indicadores del INEC y otras fuentes:

### 4.1. Pobreza y desigualdad

| Indicador | Nivel geográfico | Fuente | URL |
|-----------|------------------|--------|-----|
| Incidencia de pobreza | Provincia / Cantón | INEC – ECV | `https://www.ecuadorencifras.gob.ec` |
| Coeficiente de Gini | Provincia | INEC – ECV | `https://www.ecuadorencifras.gob.ec` |
| Pobreza extrema | Provincia / Cantón | INEC – ECV | `https://www.ecuadorencifras.gob.ec` |

### 4.2. Empleo

| Indicador | Nivel geográfico | Fuente | URL |
|-----------|------------------|--------|-----|
| Tasa de desempleo | Nacional / Provincial | INEC – ENEMDU | `https://www.ecuadorencifras.gob.ec` |
| Empleo informal | Nacional / Provincial | INEC – ENEMDU | `https://www.ecuadorencifras.gob.ec` |
| Empleo adecuado vs. incompleto | Nacional / Provincial | INEC – ENEMDU | `https://www.ecuadorencifras.gob.ec` |

### 4.3. Acceso a servicios

| Indicador | Nivel geográfico | Fuente | URL |
|-----------|------------------|--------|-----|
| Cobertura de agua potable | Cantón | INEC – Censo 2022 | `https://www.ecuadorencifras.gob.ec` |
| Cobertura de alcantarillado | Cantón | INEC – Censo 2022 | `https://www.ecuadorencifras.gob.ec` |
| Cobertura eléctrica | Cantón | INEC – Censo 2022 | `https://www.ecuadorencifras.gob.ec` |
| Acceso a internet | Cantón | INEC – Censo 2022 | `https://www.ecuadorencifras.gob.ec` |
| Establecimientos de salud | Cantón | INEC – Registro Estadístico | `https://www.ecuadorencifras.gob.ec` |
| Establecimientos educativos | Cantón | INEC – AMIE | `https://educacion.gob.ec` |

### 4.4. Seguridad

| Indicador | Nivel geográfico | Fuente | URL |
|-----------|------------------|--------|-----|
| Tasa de homicidios | Provincia | INEC – Registro Civil | `https://www.ecuadorencifras.gob.ec` |
| Denuncias por delito | Provincia / Cantón | Fiscalía General del Estado | `https://www.fiscalia.gob.ec` |
| Percepción de seguridad | Nacional | Latinobarómetro | `https://www.latinobarometro.org` |

---

## 5. Geografía electoral

### 5.1. GeoJSON del CNE

| Tipo de dato | Formato | URL | Notas |
|--------------|---------|-----|-------|
| Recintos electorales | GeoJSON | CNE – Datos abiertos | Coordenadas de cada recinto |
| Cantones | GeoJSON / Shapefile | INEC – Cartografía | Límites cantonales oficiales |
| Provincias | GeoJSON / Shapefile | INEC – Cartografía | Límites provinciales oficiales |
| Parroquias | GeoJSON / Shapefile | INEC – Cartografía | Límites parroquiales rurales y urbanas |

### 5.2. Fuentes alternativas de geometrías

| Fuente | URL | Formato | Notas |
|--------|-----|---------|-------|
| Datos Abiertos Ecuador | `https://datosabiertos.ec` | CSV/GeoJSON | Portal nacional de datos abiertos |
| Humanitarian Data Exchange (HDX) | `https://data.humdata.org` | GeoJSON | Shapefiles de Ecuador para uso humanitario |
| Natural Earth | `https://www.naturalearthdata.com` | Shapefile | Límites nacionales y de primer orden |
| GeoBoundaries | `https://www.geoboundaries.org` | GeoJSON | Límites administrativos globales, incluye Ecuador |

### 5.3. Datos electorales históricos

| Tipo de dato | Elecciones | Fuente | URL |
|--------------|-----------|--------|-----|
| Resultados por recinto | 2017, 2021, 2023, 2025 | CNE | `https://resultados2025.cne.gob.ec` |
| Padrones electorales | Histórico | CNE – Datos abiertos | `https://app01.cne.gob.ec` |
| Participación electoral | 2017-2025 | CNE | `https://www.cne.gob.ec` |
| Voto en el exterior | 2017-2025 | CNE | Distritos electorales fuera del país |

---

## 6. Calendario de actualización sugerido

| Fuente | Frecuencia de actualización | Acción |
|--------|---------------------------|--------|
| Programas de gobierno | Por ciclo electoral (cada 4 años) | Descargar al publicarse oficialmente |
| Encuestas INEC | Trimestral (ENEMDU) / Quinquenal (ECV) | Descargar al publicarse |
| Encuestas de opinión (CEDATOS, Market) | Mensual durante campaña | Descargar boletines mensuales |
| Datos proxy (redes sociales, quejas) | Mensual | Monitoreo continuo |
| Geometrías electorales | Por redistritación | Verificar cambios antes de cada elección |
| Indicadores socioeconómicos | Anual / Trimestral | Actualizar al publicarse nuevas cifras |

---

## 7. Acceso y licencias

- Los datos del **CNE** e **INEC** son de acceso público para fines académicos y de investigación.
- Las encuestas de empresas privadas (CEDATOS, Market) pueden requerir compra o convenio académico para acceso completo.
- Los datos de redes sociales están sujetos a los términos de servicio de cada plataforma.
- Los programas de gobierno son documentos públicos publicados por los partidos políticos.
- Toda información se trata según lo establecido en la normativa ecuatoriana de protección de datos personales (Ley Orgánica de Protección de Datos Personales, 2021).

> Este documento se actualiza conforme se identifican nuevas fuentes. Última revisión: Agosto 2026.
