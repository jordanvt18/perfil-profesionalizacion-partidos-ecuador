# Directorio `config/` – Configuración del Mapa de Congruencia

Este directorio contiene los archivos de configuración para el módulo de congruencia programa-votantes.

## Estructura

```
config/
├── README.md                 # Este documento
├── themes_taxonomy.yaml      # Taxonomía de 10 temas y diccionario de palabras clave
├── congruencia_weights.yaml  # Pesos para combinación de señales NLP
└── geo_config.yaml           # Configuración de niveles geográficos y fuentes
```

## Archivos

### `themes_taxonomy.yaml`

Define la taxonomía de 10 temas con:
- Identificador del tema (`id`, `name`, `slug`)
- Descripción legible
- Lista de términos primarios (palabras clave principales)
- Lista de términos secundarios (sinónimos y variaciones morfológicas)
- Bigramas relevantes
- Exclusiones (términos ambiguos que no deben contar para el tema)
- Pesos opcionales para términos de alta especificidad

### `congruencia_weights.yaml`

Define los pesos para la combinación de señales en el pipeline NLP:
- `keyword_weight`: Peso para la coincidencia de palabras clave (default: 0.5)
- `lda_weight`: Peso para el modelo LDA (default: 0.3)
- `nb_weight`: Peso para el clasificador Naive Bayes (default: 0.2)
- `bigram_multiplier`: Multiplicador para bigramas vs. unigramas (default: 2.0)
- `bootstrap_n`: Número de repeticiones bootstrap (default: 1000)
- `confidence_level`: Nivel de confianza para IC (default: 0.95)

### `geo_config.yaml`

Define la configuración geográfica:
- Niveles territoriales soportados (provincia, cantón, parroquia, recinto)
- Mapeo de códigos INEC a nombres
- URLs de descarga de GeoJSON
- Campos de unión (join keys) para cruzar datos electorales con geometrías

## Uso

Los archivos YAML se cargan al iniciar el pipeline ETL y la API. Para modificar la taxonomía o los pesos, editar los archivos correspondientes y reiniciar el pipeline:

```bash
# Recargar configuración y recalcular congruencia
python scripts/build_hybrid_data.py --config config/
```

## Validación

Los archivos de configuración deben seguir el esquema definido en `config/schema/`. Para validar:

```bash
python -c "from src.etl.congruence import validate_config; validate_config('config/')"
```
