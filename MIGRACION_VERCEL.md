# ⚠️ Netlify NO soporta Python

## Problema
Netlify Functions solo soporta:
- JavaScript/TypeScript
- Go

**NO soporta Python directamente**.

## Solución: Migrar a Vercel

### 1. Conecta tu repo en Vercel

Ve a: https://vercel.com/new

1. Importa `royeraf/movie_note`
2. Framework preset: **Vite**
3. Root directory: `./`
4. Build command: `npm run build`
5. Output directory: `dist`

### 2. Configura variables de entorno

En Vercel dashboard:
- `OMDB_API_KEY` = tu_clave
- `TMDB_API_KEY` = tu_clave

### 3. Deploy

Vercel detectará `vercel.json` y desplegará automáticamente.

## Archivos listos

- ✅ `vercel.json` - Config para Vercel
- ✅ `api/index.py` - Rutas con `/api` prefix restaurado
- ✅ Push completado

## Vercel soporta Python nativamente

Las rutas funcionarán así:

```
/api/health → api/index.py → /api/health ✅
/api/search → api/index.py → /api/search ✅
/api/movies → api/index.py → /api/movies ✅
```

## Deploy ahora

Push ya realizado. Ve a Vercel y conecta el repo.
