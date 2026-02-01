# 🔧 Fix Error 500 - Turso Connection

## ❌ Problema
```json
{"error": {"code": "500", "message": "A server error has occurred"}}
```

**Causa:** `libsql-experimental` no es compatible con SQLAlchemy/SQLModel.

## ✅ Solución Aplicada

### 1. Cambio en `requirements.txt`
```diff
- libsql-experimental
+ sqlalchemy-libsql
```

### 2. Actualización de `database.py`
```python
# Convertir URL para SQLAlchemy
turso_url = settings.DATABASE_URL.replace("libsql://", "sqlite+libsql://")

engine = create_engine(
    turso_url,
    connect_args={
        "check_same_thread": False,
        "sync_url": settings.DATABASE_URL,  # URL original libsql://
        "auth_token": auth_token            # Token de Turso
    }
)
```

## 📋 Configuración en Vercel

Asegúrate de tener estas variables:

```
DATABASE_URL=libsql://movie-note-[tu-user].turso.io
TURSO_AUTH_TOKEN=[tu-token]
OMDB_API_KEY=38cb81fd
TMDB_API_KEY=2d182c8440db914231b28a5822ef79f0
```

## ⏳ Siguiente Paso

1. **Push completado** ✅
2. **Espera el re-deploy** de Vercel (2-3 min)
3. **Prueba los endpoints:**

```bash
# Health check
curl https://tu-sitio.vercel.app/api/health

# Búsqueda
curl https://tu-sitio.vercel.app/api/search?query=matrix

# Películas
curl https://tu-sitio.vercel.app/api/movies
```

## 🐛 Si aún falla

Ver logs en Vercel:
1. Dashboard → tu proyecto
2. **Functions** → `api`
3. Ver **Logs** para detalles del error

Errores comunes:
- ❌ `TURSO_AUTH_TOKEN` no configurado
- ❌ `DATABASE_URL` incorrecto
- ❌ Base de datos no inicializada

### Inicializar tablas en Turso

```bash
# Conecta a Turso
turso db shell movie-note

# Crea las tablas (copia el schema)
CREATE TABLE movie (
    imdb_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    year TEXT,
    poster TEXT,
    actors TEXT,
    plot TEXT,
    status TEXT DEFAULT 'por_ver',
    color TEXT DEFAULT 'rojo',
    is_favorite BOOLEAN DEFAULT 0
);
```

O deja que FastAPI las cree automáticamente la primera vez (ya está configurado).

---

**Espera el deploy y prueba. Si aún hay error, revisa los logs de Vercel.**
