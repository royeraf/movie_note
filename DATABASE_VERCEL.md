# 🗄️ Base de Datos en Vercel

## ❌ Problema: SQLite no funciona en serverless

Vercel (y cualquier plataforma serverless) es **stateless**:
- Sin sistema de archivos persistente
- Cada request puede ejecutarse en contenedor diferente
- SQLite local = datos se pierden

## ✅ Solución: Turso (SQLite distribuido)

### ¿Por qué Turso?

1. **Compatible con SQLite** - misma sintaxis
2. **Gratis** - hasta 9GB, 1 billion reads/mes
3. **Edge deployment** - ultra rápido
4. **Cero cambios** - SQLModel funciona igual

---

## 🚀 Setup Completo

### 1. Instala Turso CLI

```bash
curl -sSfL https://get.tur.so/install.sh | bash
```

### 2. Crea cuenta

```bash
turso auth signup
```

### 3. Crea base de datos

```bash
turso db create movie-note
```

Respuesta:
```
Created database movie-note at [region]
URL: libsql://movie-note-[user].turso.io
```

### 4. Obtén credenciales

**URL:**
```bash
turso db show movie-note --url
```

**Token:**
```bash
turso db tokens create movie-note
```

Copia ambos.

### 5. Configura en Vercel

Ve a tu proyecto en Vercel:
- **Settings** → **Environment Variables**

Agrega:
```
DATABASE_URL = libsql://movie-note-[tu-usuario].turso.io
TURSO_AUTH_TOKEN = [tu-token-aqui]
OMDB_API_KEY = 38cb81fd
TMDB_API_KEY = 2d182c8440db914231b28a5822ef79f0
```

### 6. Re-deploy en Vercel

Los cambios ya están en GitHub. Vercel re-desplegará automáticamente.

---

## 📦 Archivos Actualizados

✅ **`api/core/database.py`** - Detecta Turso vs SQLite local
✅ **`api/requirements.txt`** - Agrega `libsql-experimental`
✅ **Push completado** a GitHub

---

## 🔄 Migrar datos existentes (opcional)

Si tienes películas en tu SQLite local:

```bash
# 1. Exporta datos locales
sqlite3 movies.db .dump > movies.sql

# 2. Importa a Turso
turso db shell movie-note < movies.sql
```

---

## 🧪 Probar localmente

Tu app sigue usando SQLite local (no cambies `.env`).

Para probar con Turso local:

```bash
# En .env, cambia temporalmente:
DATABASE_URL=libsql://movie-note-[tu-usuario].turso.io
TURSO_AUTH_TOKEN=[tu-token]

# Ejecuta
uvicorn api.index:app --reload
```

---

## 📊 Cómo funciona

### Local (desarrollo):
```
.env → DATABASE_URL=sqlite:///movies.db
     → database.py detecta SQLite
     → Usa archivo local
```

### Producción (Vercel):
```
Vercel vars → DATABASE_URL=libsql://...
           → database.py detecta Turso
           → Conecta a Turso
```

---

## ✅ Checklist

- [ ] Instalar Turso CLI
- [ ] Crear cuenta: `turso auth signup`
- [ ] Crear DB: `turso db create movie-note`
- [ ] Obtener URL: `turso db show movie-note --url`
- [ ] Obtener token: `turso db tokens create movie-note`
- [ ] Configurar variables en Vercel
- [ ] Esperar re-deploy automático
- [ ] Probar endpoints

---

## 🎯 Comandos útiles Turso

```bash
# Ver bases de datos
turso db list

# Ver info de una DB
turso db show movie-note

# Abrir shell SQL
turso db shell movie-note

# Ver tablas
turso db shell movie-note ".tables"

# Ver datos
turso db shell movie-note "SELECT * FROM movie;"
```

---

## 🌐 Alternativas

### Vercel Postgres
```bash
vercel postgres create
```
- Requiere cambiar de SQLite a PostgreSQL
- Más cambios de código

### Supabase
- PostgreSQL gratis
- Dashboard web
- Requiere cambios de SQLModel

---

**Turso es la opción más simple porque mantiene compatibilidad con SQLite.**
