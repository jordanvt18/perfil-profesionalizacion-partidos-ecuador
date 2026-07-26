# Seguridad y buenas prácticas

Este documento establece las buenas prácticas de seguridad para el repositorio
`perfil-profesionalizacion-partidos-ecuador` antes de hacer deploy.

## 🔐 Principios

1. **Nunca exponer credenciales** — Ni en código fuente, datos demo, ni commits.
2. **Datos demo anónimos** — Los datos sintéticos no contienen información personal real.
3. **GitHub Pages seguro** — Sin backend expuesto, sin API keys, sin endpoints privados.
4. **Scraping ético** — Solo fuentes públicas, respetando robots.txt y rate limiting.

## 📋 Checklist pre-deploy

- [ ] `.env` y `.env.example` no contienen secretos reales
- [ ] `.gitignore` incluye `.env`, `data/raw/`, `data/processed/` locales
- [ ] `demo-data.js` no contiene información personal real
- [ ] No hay tokens, API keys, ni contraseñas en ningún archivo del repo
- [ ] URLs de fuentes oficiales verificadas y documentadas en `docs/sources.md`
- [ ] El frontend funciona en modo demo sin backend (DEMO_MODE = true)
- [ ] GitHub Pages configurado para servir desde `/web` o raíz del repo
- [ ] `SECURITY.md` visible en el repo

## 🚫 Qué NO incluir

- **Datos personales reales** de candidatos (nombres, cédulas, direcciones)
- **Credenciales** de APIs, bases de datos, o servicios cloud
- **CVs completos** con información sensible (solo metadatos agregados)
- **Cookies, tokens de sesión, o secretos** de cualquier tipo
- **Archivos `.parquet` o `.csv` con datos reales** del CNE (solo datos demo sintéticos)

## 🔍 Revisión de archivos sensibles

Antes de cada push, revisar:

```bash
# Buscar secretos accidentales
git diff --cached | grep -iE '(password|secret|token|api_key|credential)'

# Verificar que .env no esté commiteado
git status | grep .env
```

## 📡 GitHub Pages

Configuración recomendada:
- **Source**: rama `main`, carpeta `/web` (o `/docs`)
- **HTTPS**: siempre forzado
- **Sin Secrets**: GitHub Pages no expone secrets del repo

## 🔗 Enlaces externos

- Todos los `target="_blank"` incluyen `rel="noopener noreferrer"` para prevenir tabnabbing
- Las dependencias CDN (Leaflet, Plotly, D3) se cargan desde unpkg/CDN oficiales con SRI cuando es posible

## 📝 Reporte de vulnerabilidades

Si encuentras alguna vulnerabilidad en este repositorio, por favor abre un issue en GitHub o contacta al mantenedor.
