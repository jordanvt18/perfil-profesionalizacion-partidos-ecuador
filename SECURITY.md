# Buenas prácticas de seguridad

Este proyecto sigue buenas prácticas de seguridad para proteger credenciales, respetar fuentes de datos oficiales y evitar exposición innecesaria de servicios.

## 1. Manejo de credenciales y variables de entorno

- No se deben commitear archivos `.env` ni credenciales en el repositorio (ver `.gitignore`).
- Usa siempre variables de entorno para configurar:
  - `DATABASE_URL`
  - Usuarios y contraseñas de Postgres (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`).
- Proporciona ejemplos seguros en `/.env.example` y copia ese archivo a `.env` en tu entorno local.

## 2. Base de datos y servicios

- En desarrollo local, la base de datos solo debe exponerse en la red local (por defecto `localhost:5432`).
- En despliegues en la nube, restringe el acceso a la base de datos mediante:
  - IP allowlist o security groups.
  - Contraseñas fuertes y rotación periódica.
- No abras el puerto de Postgres directamente a Internet sin controles adicionales.

## 3. Scraping y uso de fuentes oficiales

- Respeta siempre `robots.txt` de los portales donde se obtienen CVs y datos.
- Implementa rate limiting (esperas entre solicitudes) y evita cargas agresivas sobre servidores públicos.
- Registra la fecha de ejecución y la URL base de cada fuente en `docs/sources.md`.
- Evita extraer información sensible que no sea estrictamente necesaria para el análisis académico.

## 4. Datos personales y privacidad

- Para candidatos no públicos, considera anonimizar identificadores personales en datasets compartidos.
- No publiques información de contacto ni detalles sensibles en los datos procesados.
- Documenta criterios de anonimización y agregación en `METHODOLOGY.md`.

## 5. Frontend y API

- La demo pública en GitHub Pages utiliza datos de ejemplo (`web/demo-data.js`) y no expone credenciales ni servicios internos.
- La API real (FastAPI + Postgres) debe desplegarse en un servicio separado, protegido y con CORS configurado según los dominios permitidos.

---

Antes de abrir el proyecto a colaboración o uso más amplio, revisa esta guía y actualiza controles según las políticas de seguridad de tu entorno de despliegue.