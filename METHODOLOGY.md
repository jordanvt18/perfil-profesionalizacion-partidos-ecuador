# Metodología

Este documento describe con detalle la construcción de los índices de este proyecto: (1) el índice de profesionalización de candidatos y (2) el mapa de congruencia programa-votantes.

---

# Parte I: Índice de Profesionalización

## Definiciones

- **Score académico (`score_academico`)**: valor numérico asociado al máximo grado académico alcanzado.
- **Score de experiencia (`score_experiencia`)**: valor numérico asociado a años de experiencia en cargos públicos o funciones políticas.
- **Índice de profesionalización (`profesionalizacion`)**: combinación ponderada de score académico y score de experiencia en escala 0–100.

## Escala académica

Se mapea el máximo grado identificado en el CV del candidato a la siguiente escala:

- Primaria: 10
- Secundaria: 30
- Técnico / tecnólogo: 50
- Universitario (licenciatura, ingeniería, etc.): 70
- Posgrado (especialización, maestría, PhD): 90

Este valor se asigna a `score_academico` y se controla que esté siempre en el rango [0, 100].

## Score de experiencia

A partir de los años totales en cargos públicos o funciones políticas se define:

- `score_experiencia = min(40, años_publicos * 2)`

Donde `años_publicos` se calcula sumando:

- Periodos en cargos electivos (concejal, asambleísta, alcalde, etc.).
- Cargos de designación pública (viceministro, director, gerente de empresa pública, etc.).

El límite superior de 40 evita que trayectorias muy largas dominen completamente el índice.

## Fórmula del índice

El índice de profesionalización por candidato se calcula como:

- `profesionalizacion = 0.6 * score_academico + 0.4 * score_experiencia`

Y se normaliza a rango 0–100 si fuera necesario.

## Fuentes de datos

- Actas y resultados oficiales del CNE por recinto/cantón/provincia.
- Padrones electorales históricos.
- CVs públicos de candidatos (páginas oficiales, portales de transparencia, sitios personales).
- Controles socioeconómicos provenientes de INEC (por provincia/cantón).

Todas las URLs oficiales usadas se documentan en `docs/sources.md` junto con la fecha de descarga.

## Limitaciones y disclaimer

- El índice captura solo educación formal y experiencia pública; no mide competencias técnicas, reputación ni desempeño.
- La disponibilidad de CVs públicos puede ser desigual entre partidos y candidatos, introduciendo sesgos.
- Los años de experiencia se basan en capacidad de extracción automática y revisión manual; pueden existir errores de interpretación.
- El índice no implica juicio de valor sobre la idoneidad política ni sobre la calidad de las propuestas.

> Este proyecto tiene fines exclusivamente académicos y de investigación. No constituye recomendación de voto ni evaluación definitiva de personas o partidos.

---

# Parte II: Metodología del Mapa de Congruencia Programa-Votantes

## 1. Construcción de la taxonomía de temas

### 1.1. Criterios de selección

La taxonomía de **10 temas** se construyó con base en:

1. **Revisión de literatura**: Estudios sobre agenda-setting y congruencia política en América Latina (Wiesehomeier & Benoit, 2009; Alcántara Sáez, 2012).
2. **Análisis de programas reales**: Codificación manual de planes de gobierno de elecciones ecuatorianas 2017-2025 para identificar categorías emergentes.
3. **Comparabilidad con encuestas**: Los temas deben ser mapeables a preguntas estándar de encuestas de opinión (Latinobarómetro, INEC, CEDATOS).
4. **Mutuamente excluyentes y colectivamente exhaustivos (MECE)**: Cada mención se asigna a un único tema; la taxonomía cubre el espectro de la agenda pública.

### 1.2. Taxonomía final

| # | Tema | Palabras clave representativas |
|---|------|-------------------------------|
| 1 | Empleo y economía | empleo, trabajo, inversión, PIB, emprendimiento, tributación |
| 2 | Educación | educación, escuela, colegio, universidad, docente, currículo |
| 3 | Salud | salud, hospital, médico, medicamento, aseguramiento, CSS |
| 4 | Seguridad ciudadana | seguridad, delincuencia, crimen, policía, justicia, prevención |
| 5 | Infraestructura y servicios | vías, carreteras, agua potable, alcantarillado, electricidad, internet |
| 6 | Medio ambiente | ambiente, contaminación, deforestación, áreas protegidas, cambio climático |
| 7 | Corrupción y transparencia | corrupción, transparencia, rendición de cuentas, institución, ética |
| 8 | Agricultura y desarrollo rural | agricultura, ganadería, riego, crédito agrícola, soberanía alimentaria |
| 9 | Turismo y cultura | turismo, patrimonio, cultura, artes, industrias creativas |
| 10 | Derechos sociales | género, inclusión, discapacidad, adultos mayores, pueblos, nacionalidades |

### 1.3. Diccionario de palabras clave

El diccionario completo de palabras clave y sinónimos se mantiene en `config/themes_taxonomy.yaml`. Cada tema incluye:
- **Términos primarios**: 8-15 palabras clave directas
- **Términos secundarios**: 15-30 sinónimos y variaciones morfológicas
- **Bigramas**: 5-10 bigramas relevantes (ej: "seguridad ciudadana", "desarrollo rural")
- **Exclusiones**: Términos ambiguos que no deben contar (ej: "seguridad social" se excluye de "seguridad ciudadana" y se redirige a "salud")

---

## 2. Pipeline de extracción NLP

### 2.1. Preprocesamiento

1. **Extracción de texto**: Los PDFs de planes de gobierno se procesan con `pdfminer.six` para obtener texto plano.
2. **Limpieza**: Eliminación de encabezados, pies de página, números de página y caracteres especiales.
3. **Segmentación**: División por secciones/capítulos cuando el documento tiene estructura clara.

### 2.2. Tokenización y anotación

Se utiliza **spaCy** con el modelo `es_core_news_sm` para:
- Tokenización y segmentación por oraciones
- Lematización (reducción a la forma canónica)
- POS tagging (etiquetado gramatical)
- Reconocimiento de entidades nombradas (NER)
- Filtrado de stop words en español

### 2.3. Clasificación temática

La clasificación combina tres enfoques:

#### A. Coincidencia de palabras clave (ponderación 0.5)

Cada token lematizado se compara contra el diccionario de la taxonomía. Un token puede coincidir con múltiples temas; en ese caso, se asigna un peso fraccional. Los bigramas detectados reciben un peso de 2× respecto a unigramas.

#### B. Modelo LDA (ponderación 0.3)

Se entrena un modelo **Latent Dirichlet Allocation** (LDA) con `scikit-learn` sobre el corpus de programas. El número de tópicos se fija en 10 (alineado con la taxonomía). Para cada documento, se obtiene la distribución de tópicos y se mapea cada tópico al tema más probable de la taxonomía mediante inspección manual de las palabras más probables por tópico.

#### C. Clasificador supervisado (ponderación 0.2)

Se entrena un clasificador **Naive Bayes multinomial** con TF-IDF sobre un conjunto de entrenamiento de párrafos etiquetados manualmente (mínimo 500 párrafos). Este clasificador asigna un tema a cada párrafo del programa.

#### Combinación final

Para cada párrafo, se combinan las tres señales:

```
theme_score(tema_i) = 0.5 × keyword_score + 0.3 × lda_score + 0.2 × nb_score
```

El tema con mayor puntuación se asigna al párrafo. Las puntuaciones se acumulan a nivel de documento.

---

## 3. Construcción de vectores

### 3.1. Vector de programa (`program_vector`)

Para cada partido, se construye un vector de 10 dimensiones:

```
program_vector = [p1, p2, p3, ..., p10]
```

Donde `p_i` es la **proporción de menciones** del tema *i* en el programa de gobierno:

```
p_i = menciones_tema_i / total_menciones
```

El vector se normaliza para que `sum(program_vector) = 1`.

### 3.2. Vector de prioridades (`priority_vector`)

Para cada unidad territorial (provincia o cantón), se construye un vector de 10 dimensiones:

```
priority_vector = [q1, q2, q3, ..., q10]
```

Donde `q_i` es la **proporción de ciudadanos** que identifican el tema *i* como su prioridad principal:

```
q_i = ciudadanos_prioridad_i / total_encuestados
```

Fuentes de datos para el vector de prioridades:
- **Encuestas directas** (peso 0.6): Encuestas de opinión con pregunta abierta sobre principal problema/prioridad
- **Sondeos municipales** (peso 0.2): Datos de consultas ciudadanas de gobiernos locales
- **Datos proxy** (peso 0.2): Peticiones en portales municipales, menciones en redes sociales geolocalizadas

El vector se normaliza para que `sum(priority_vector) = 1`.

---

## 4. Cálculo de la congruencia

### 4.1. Similitud coseno

La congruencia entre un partido *j* y una unidad territorial *k* se calcula como:

```
cosine_sim = (Σᵢ program_vector_j[i] × priority_vector_k[i]) / (||program_vector_j|| × ||priority_vector_k||)
```

Donde `||·||` es la norma Euclidiana. El resultado está en el rango [-1, 1] (aunque en práctica, dado que todos los componentes son no negativos, el rango efectivo es [0, 1]).

### 4.2. Escalamiento a 0-100

```
congruencia_100 = cosine_sim × 100
```

Dado que los vectores tienen componentes no negativos, `cosine_sim` está en [0, 1], por lo que la congruencia está en [0, 100]:
- **0**: Sin ninguna alineación (vectores ortogonales)
- **100**: Alineación perfecta (vectores idénticos en dirección)

### 4.3. Interpretación

| Rango | Interpretación |
|-------|----------------|
| 80-100 | Congruencia muy alta: el programa refleja casi exactamente las prioridades ciudadanas |
| 60-79 | Congruencia alta: el programa cubre las prioridades principales con algunas omisiones |
| 40-59 | Congruencia moderada: el programa alinea parcialmente con las prioridades |
| 20-39 | Congruencia baja: el programa enfatiza temas distintos a las prioridades ciudadanas |
| 0-19 | Congruencia muy baja: el programa ignora las prioridades de la población |

---

## 5. Intervalos de confianza (Bootstrap)

### 5.1. Procedimiento

Para estimar la incertidumbre del índice de congruencia, se utiliza **remuestreo bootstrap**:

1. Se remuestrean con reemplazo los párrafos del programa de gobierno (1000 repeticiones).
2. Para cada remuestreo, se recalcula el `program_vector` y la congruencia.
3. Se obtiene la distribución empírica de la congruencia.
4. Se reporta el **intervalo de confianza al 95%** (percentiles 2.5 y 97.5).

Para el `priority_vector`, cuando los datos provienen de encuestas, se aplica un bootstrap paralelo sobre los respondientes:

1. Se remuestrean con reemplazo los respondientes (1000 repeticiones).
2. Para cada remuestreo, se recalcula el `priority_vector` y la congruencia.
3. Se reporta el IC al 95%.

### 5.2. Reporte

Cada puntaje de congruencia se reporta como:

```
{
  "congruencia": 72.3,
  "ic_inf": 68.1,
  "ic_sup": 76.5,
  "n_bootstrap": 1000
}
```

---

## 6. Limitaciones

### 6.1. Datos proxy

Cuando no existen encuestas directas de prioridades para una provincia o cantón, se utilizan datos proxy (peticiones municipales, redes sociales). Estos datos pueden:
- **Sesgar hacia poblaciones conectadas**: Las redes sociales sobre-representan zonas urbanas y poblaciones más jóvenes.
- **Confundir volumen con prioridad**: Una alta cantidad de quejas sobre un tema puede reflejar problemas agudos puntuales, no necesariamente prioridad estructural.

### 6.2. Sesgo de taxonomía

- La taxonomía de 10 temas puede ser **insuficiente** para capturar dimensiones específicas del contexto ecuatoriano (ej: migración, políticas petroleras, relaciones con Perú/Colombia).
- La asignación de un tema por párrafo puede **perder matices** cuando un párrafo aborda múltiples temas.
- Los términos del diccionario pueden tener **connotaciones distintas** según el contexto (ej: "seguridad" puede referirse a seguridad ciudadana o seguridad social).

### 6.3. Extracción NLP

- El modelo `es_core_news_sm` de spaCy no está optimizado para texto político ecuatoriano; puede haber errores en lematización y NER.
- El modelo LDA puede **agrupar tópicos** de manera no alineada con la taxonomía, requiriendo mapeo manual.
- Los programas de gobierno varían en formato y estructura; algunos son documentos extensos, otros son resúmenes ejecutivos, afectando la comparabilidad.

### 6.4. Cobertura

- No todos los partidos publican programas completos en formato accesible.
- Las encuestas de opinión no cubren todas las provincias y cantones con la misma profundidad.
- Los datos proxy pueden no estar disponibles para todas las localidades.

### 6.5. Interpretación

- **La congruencia no mide calidad**: Un partido puede mencionar todos los temas que importan a la ciudadanía pero con propuestas vagas o inviables.
- **La congruencia no mide compromiso**: Un programa puede ser congruente pero no reflejarse en la acción de gobierno.
- **La congruencia no implica representatividad**: Un partido puede ser congruente con las prioridades mayoritarias pero ignorar las necesidades de minorías.

> Este proyecto tiene fines exclusivamente académicos y de investigación. No constituye recomendación de voto ni evaluación definitiva de personas o partidos.
