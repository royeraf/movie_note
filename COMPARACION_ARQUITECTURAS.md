# 📊 Diferencia entre LectoSistem y Movie Note

## 🏗️ Arquitectura de Despliegue

### LectoSistem (Desktop/Render)
```
┌─────────────────────────────────────┐
│   SERVIDOR TRADICIONAL (Render)     │
├─────────────────────────────────────┤
│  Backend FastAPI (siempre activo)   │
│  ├─ main.py (sirve frontend + API)  │
│  ├─ SQLite file: desempenos.db      │
│  │   (archivo persistente en disco) │
│  └─ Frontend dist/ (archivos HTML)  │
└─────────────────────────────────────┘
        ↑
        │ Persistencia: ✅ SÍ
        │ El archivo .db se guarda en disco
        │ El servidor está siempre corriendo
```

### Movie Note (Vercel/Netlify)
```
┌─────────────────────────────────────┐
│    SERVERLESS (Sin servidor fijo)   │
├─────────────────────────────────────┤
│  Frontend (CDN estático)             │
│  └─ dist/ → Netlify/Vercel CDN      │
├─────────────────────────────────────┤
│  Backend (Funciones Lambda)          │
│  ├─ Se ejecuta SOLO cuando llaman   │
│  ├─ Contenedor nuevo cada request   │
│  └─ SQLite local: ❌ NO PERSISTE    │
│      (contenedor se destruye)       │
└─────────────────────────────────────┘
        ↑
        │ Persistencia: ❌ NO
        │ Cada request = contenedor nuevo
        │ El archivo .db desaparece
```

---

## 🔍 Diferencias Clave

| Aspecto | LectoSistem (Render) | Movie Note (Vercel) |
|---------|---------------------|---------------------|
| **Tipo** | Servidor tradicional | Serverless/Lambda |
| **Backend** | Siempre corriendo | Solo cuando se llama |
| **SQLite local** | ✅ Funciona | ❌ No persiste |
| **Sistema archivos** | ✅ Persistente | ❌ Efímero |
| **Costo** | Paga por tiempo activo | Paga por invocación |
| **Escalamiento** | Manual | Automático |
| **Startup time** | Siempre listo | Cold start (~1-2s) |

---

## 💾 Base de Datos

### LectoSistem
```python
# backend/app/database.py
DATABASE_URL = "sqlite:///./desempenos.db"
engine = create_engine(DATABASE_URL, ...)
```

**¿Por qué funciona?**
- Render ejecuta tu app en un **contenedor persistente**
- El archivo `desempenos.db` se guarda en disco
- El contenedor NO se destruye entre requests
- La DB persiste mientras el servidor esté activo

### Movie Note
```python
# api/core/database.py
DATABASE_URL = "sqlite:///./movies.db"
engine = create_engine(DATABASE_URL, ...)
```

**¿Por qué NO funciona?**
- Vercel ejecuta tu función en **contenedores efímeros**
- Cada request puede usar un contenedor diferente
- El contenedor se destruye después del request
- El archivo `movies.db` desaparece

---

## 🚀 Soluciones para Movie Note

### Opción 1: Turso (SQLite distribuido)
```python
# Cambiar solo la URL
DATABASE_URL = "libsql://movie-note-xxx.turso.io"
TURSO_AUTH_TOKEN = "eyJ..."
```
✅ Sintaxis SQLite igual
✅ Código casi sin cambios

### Opción 2: Migrar a Render (como LectoSistem)
```python
# Mantener SQLite local
DATABASE_URL = "sqlite:///./movies.db"
```
✅ Funciona igual que LectoSistem
❌ Servidor siempre activo (más costoso)

### Opción 3: Supabase/PostgreSQL
```python
# Cambiar a PostgreSQL
DATABASE_URL = "postgresql://..."
```
❌ Requiere cambiar SQLModel/queries

---

## 📝 Código de LectoSistem

### Servidor Monolítico
```python
# backend/app/main.py
app = FastAPI(...)

# API Routes
app.include_router(api_router, prefix="/api")

# ✅ Sirve el FRONTEND también
app.mount("/assets", StaticFiles(directory=frontend_dist))

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Sirve index.html para Vue Router
    return FileResponse("frontend/dist/index.html")
```

**Una sola app sirve:**
- Backend API (`/api/*`)
- Frontend estático (`/`, `/assets/*`)
- SQLite persistente

---

## 📝 Código de Movie Note

### Frontend y Backend Separados
```
Frontend (Netlify/Vercel CDN)
  └─ dist/ → Servido como archivos estáticos

Backend (Vercel Functions)
  └─ api/*.py → Funciones Lambda independientes
```

**Dos servicios separados:**
- Frontend: CDN (rápido, barato)
- Backend: Funciones (escalable)
- DB: Externa requerida (Turso/Supabase)

---

## 🎯 Recomendación para Movie Note

### Si quieres mantener SQLite:
1. **Usa Turso** (ya configurado)
2. Deploy en Vercel
3. Configura variables de entorno

### Si quieres simplicidad (como LectoSistem):
1. **Migra a Render**
2. Sirve frontend + backend juntos
3. SQLite local funciona

---

## 🔧 Configuración Render (estilo LectoSistem)

Si prefieres el modelo tradicional:

```toml
# render.yaml
services:
  - type: web
    name: movie-note
    env: python
    buildCommand: "pip install -r requirements.txt && cd frontend && npm install && npm run build"
    startCommand: "uvicorn api.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: DATABASE_URL
        value: sqlite:///./movies.db
      - key: OMDB_API_KEY
        sync: false
```

Así funcionaría igual que LectoSistem.

---

## ✅ Conclusión

| Proyecto | Plataforma | Modelo | SQLite Local |
|----------|-----------|--------|--------------|
| **LectoSistem** | Render | Monolito | ✅ Funciona |
| **Movie Note** | Vercel | Serverless | ❌ Requiere Turso |

**Tu elección:**
- Serverless + Turso = Moderno, escalable
- Render + SQLite = Simple, como LectoSistem
