# MovieNote 🎬

Tu santuario personal de cine para anotar películas vistas y por ver.

## Tecnologías
- **Frontend**: Vue 3 + Vite + Tailwind CSS v4 🚀
- **Backend**: FastAPI + SQLModel (SQLite) 🐍
- **Gestor de Paquetes**: Bun ⚡
- **Despliegue**: Optimizado para Vercel ☁️

## Requisitos
1. **Bun** instalado.
2. Una **API Key de TMDB** (Consíguela en [themoviedb.org](https://www.themoviedb.org/settings/api)).

## Instalación y Ejecución

### 1. Preparación
```bash
# Instala las dependencias del frontend
bun install

# Instala las dependencias del backend (opcional si usas venv)
pip install -r requirements.txt
```

### 2. Configuración
Crea un archivo `.env` en la raíz con tu API Key:
```env
TMDB_API_KEY=tu_clave_aqui
```

### 3. Desarrollo
Para ejecutar ambos en local durante el desarrollo:

**Terminal 1 (Frontend):**
```bash
bun run dev
```

**Terminal 2 (Backend):**
```bash
python -m uvicorn api.index:app --reload
```

## Despliegue en Vercel
1. Sube el código a GitHub.
2. Conecta tu repositorio en Vercel.
3. Configura la variable de entorno `TMDB_API_KEY`.
4. Vercel detectará automáticamente la configuración y desplegará el monorepo.
