# Fuentes de datos sugeridas – Mapa de Congruencia Programa-Votantes

Este documento registra las fuentes de datos sugeridas y disponibles para construir el mapa de congruencia entre programas de gobierno y prioridades ciudadanas en el Ecuador.

---

## 0. Elecciones Seccionales 2026 — fuentes verificadas (corte: 16 de agosto de 2026)

### 0.1. Contexto del proceso

| Dato | Valor | Fuente |
|------|-------|--------|
| Fecha de comicios | Domingo 29 de noviembre de 2026 | CNE (`cne.gob.ec`) |
| Inscripción de candidaturas | 2 al 17 de agosto de 2026 | CNE |
| Listado definitivo de provincias | 24 de septiembre de 2026 | CNE |
| Listado definitivo de papeletas | 9 de noviembre de 2026 | CNE |
| Campaña electoral | 12 al 26 de noviembre de 2026 | CNE |
| Postulaciones registradas (15-ago) | 17.934 | CNE / Primicias |

> ⚠️ **Preliminar**: toda candidatura individual es preliminar hasta el listado oficial del CNE del 9 de noviembre de 2026. La calificación en firme puede excluir nombres.

### 0.2. Fuentes utilizadas para la actualización de datos (agosto 2026)

**Nivel High (base primaria)** — usadas para integrar candidaturas y ejes programáticos:

- **CNE** (`cne.gob.ec`, `app01.cne.gob.ec`, `delegaciones.cne.gob.ec`): calendario, requisitos, planes registrados, listados definitivos. Fuente canónica.
- **Primicias** (`primicias.ec`): inscripciones y alianzas (Muñoz 14-ago, Viteri 11-ago, Guschmer 12-ago, Yunda 14-ago, Ubidia, Burbano, Angulo, Roche 15-ago, Zambrano 11-ago, Cueva, Palacios 13-ago, Encalada 13-ago, Macas 13-ago, Ordóñez 14-ago, Weber, Santistevan 13-ago, Carrasco 11-ago, Morales, Riquetti, Palacios Ullauri, Lloret, Luzárraga, Caiza, Bayas, Erazo, Lara, Naranjo, Valdivieso 13-ago, González 15-ago).
- **El Universo** (`eluniverso.com`): Zambrano (11-ago), Angulo, Caiza, Valdivieso.
- **El Comercio** (`elcomercio.com`): contexto RC, suspensión de Amigo, Burbano (14-ago).
- **Expreso** (`expreso.ec`): listas de precandidatos, contexto Amigo.
- **Ecuavisa** (`ecuavisa.com`): inscripción de Ycaza (13-ago), Viteri (12-ago).
- **El Telégrafo** (`eltelegrafo.com.ec`): mensajes de campaña (Burbano), plan nacional ADN 2025.
- **Vistazo** (`vistazo.com`): Luisa González → Pachakutik (14-ago); RC (4-ago).
- **Teleamazonas**: cronograma, contexto Amigo.
- **Diario Correo** (`diariocorreo.com.ec`, El Oro): Falquez (04-jul), Steven Ordóñez, Macas, Cueva.
- **El Diario** (`eldiario.ec`, Manabí): Ycaza, Caiza, Bayas, Erazo.
- **Sitios oficiales de partidos** (`adn-ecuador.org`, `revolucionciudadana.com.ec`): referencia de plataforma nacional, nunca como plan seccional.

**Nivel Medium (respaldo con fuente High)**: La Hora, Radio Centro (Roche 15-ago, Galo Lara 15-ago), Radio Pichincha, La Prensa, La República, Expectativa, notiregionecuador.com, El Mercurio (vía sitio web), Prensa Latina (solo contexto), Wikipedia (solo contexto biográfico).

**Nivel Low (solo corroboración, NO integrados como evidencia)**: Instagram/Facebook/TikTok de candidatos y páginas locales, cuentas de X sin verificación editorial, páginas tipo `CNEImbaburaEc` (riesgo de suplantación). Las candidaturas con fuente única social quedan **LOW** hasta confirmación del CNE.

**Excluidas**: blogs anónimos (p. ej. `radiogovea.wordpress.com`), cuentas anónimas, listas virales sin fecha ni autor.

### 0.3. Decisiones verificadas y conflictos pendientes

**Resuelto (verificación cruzada):**

- Movimiento **Amigo = lista 16** (no 62); **Caminantes = lista 62** (Manabí); **Renace = 107**; **RETO = Renovación Total = 33**.
- **Cynthia Viteri** → ADN (7), Alcaldía de Guayaquil (antes precandidata por Centro Democrático).
- **Fiorella Ycaza** sustituyó a Norero como candidata correísta a la Alcaldía de Guayaquil (auspicio PSE-17).
- **Luisa González** → Pachakutik (18), Prefectura de Manabí.
- **RC-5 y Amigo suspendidas por el TCE** (caso "Caja Chica"); el correísmo participa con listas prestadas (PSE, UP, Todos, Pachakutik, RETO).
- Partidos **bloqueados** por el CNE al corte: RC5, SUMA, ID, RETO y Amigo → no generan candidaturas sintéticas en el frontend.

**Pendiente de confirmación CNE (listado 9-nov-2026) — marcado como preliminar:**

- Sigla definitiva de **Andrés Guschmer** (ADN-7 vs. registro PSC del 15-ago).
- Lista de **Sofía Espín** (Amigo-16 vs. PSE-17) — no integrada como High.
- Dignidad de **Carlos Falquez Aguilar** (alcaldía Machala vs. prefectura El Oro) — no integrada como High.
- **Paola Pabón** (Pichincha): tratada como NO confirmada.
- Listas provinciales (AFE-131, PHD-67, PLAN-77, Futuro-20, Sí Podemos-72, Mejor Ciudad-107, Somos Azuay, etc.): sin verificación independiente contra el registro del CNE.

### 0.4. Planes de trabajo seccionales

Al corte del 16 de agosto de 2026 **ningún plan de trabajo seccional completo está publicado** (son requisito CNE de inscripción y solo serán contrastables tras el listado definitivo). Los ejes programáticos integrados en `data/plans/planes_trabajo.json` provienen de cobertura mediática confiable (fuentes High/Medium) y de los planes nacionales registrados (ADN: plan nacional de 6 ejes en `adn-ecuador.org`). **No se atribuye ningún eje programático sin fuente High/Medium; si no hay evidencia, se declara "sin evidencia"** en lugar de inferir.

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
