# 🔄 Solución Alternativa: Vercel Postgres

## ❌ Problema con Turso
```
ValueError: Hrana: `api error: `status=308 Permanent Redirect
```

**Turso + SQLModel NO funcionan bien en Vercel** (requiere reescribir todos los endpoints).

## ✅ Mejor Opción: Vercel Postgres

### Ventajas
- ✅ **Gratis** hasta 256MB
- ✅ **Compatible con SQLModel** (cero cambios de código)
- ✅ **Nativo de Vercel** (integración perfecta)
- ✅ **PostgreSQL** (mejor que SQLite para producción)

---

## 🚀 Setup Vercel Postgres

### 1. Crea la base de datos en Vercel CLI

```bash
# Instala Vercel CLI si no lo tienes
npm install -g vercel

# Login
vercel login

# Crea Postgres database
vercel postgres create
```

**Selecciona:**
- Database name: `movie-note-db`
- Region: (el más cercano)

### 2. Vincula a tu proyecto

```bash
# En tu carpeta del proyecto
cd /home/royer/Desktop/movie_note
vercel  link

# Conecta la database
vercel env pull .env.local
```

Esto descargará automáticamente la `POSTGRES_URL`.

### 3. Actualiza requirements.txt

```bash
# Agrega psycopg2
echo "psycopg2-binary" >> api/requirements.txt
```

### 4. Código (ya casi listo)

Solo necesitas cambiar `DATABASE_URL` en Vercel a la URL de Postgres (se autoconfigura).

**No necesitas cambiar código** - SQLModel funciona igual con Postgres.

---

## 📝 Alternativa: Supabase (También Gratis)

Si prefieres no usar Vercel Postgres:

### 1. Ve a https://supabase.com

### 2. Crea proyecto gratis

### 3. Obtén DATABASE_URL

**Settings → Database → Connection string**

Copia la URL tipo:
```
postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
```

### 4. Configura en Vercel

**Environment Variables:**
```
DATABASE_URL=postgresql://postgres:...
```

### 5. Agrega psycopg2

```
psycopg2-binary
```

---

## 🎯 Recomendación

**Usa Vercel Postgres:**

```bash
# 1. Crea DB
vercel postgres create

# 2. Vincula proyecto
vercel link

# 3. Agrega psycopg2
echo "psycopg2-binary" >> api/requirements.txt

# 4. Commit y push
git add api/requirements.txt
git commit -m "Add PostgreSQL support"
git push
```

Vercel configurará `DATABASE_URL` automáticamente.

---

## ⚠️ Rollback Turso Changes

```bash
# Revertir a configuración simple
git checkout HEAD~3 api/core/database.py
git checkout HEAD~3 api/requirements.txt
```

Luego agregar solo `psycopg2-binary`.

---

**¿Prefieres Vercel Postgres o Supabase?**
