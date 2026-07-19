# Índice de profesionalización de partidos – Metodología

Este documento describe con detalle la construcción del índice de profesionalización de candidatos y su agregación por partido y provincia.

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
