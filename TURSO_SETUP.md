# Turso Setup - SQLite Distribuido para Vercel

## 1. Instala Turso CLI

```bash
curl -sSfL https://get.tur.so/install.sh | bash
```

## 2. Crea cuenta y login

```bash
turso auth signup
turso auth login
```

## 3. Crea base de datos

```bash
turso db create movie-note
```

## 4. Obtén la URL y token

```bash
turso db show movie-note --url
turso db tokens create movie-note
```

## 5. Configura en Vercel

Ve a Vercel Dashboard → Settings → Environment Variables:

```
DATABASE_URL=libsql://[tu-db].turso.io
TURSO_AUTH_TOKEN=[tu-token]
```

## 6. Actualiza dependencias

Agrega a `api/requirements.txt`:
```
libsql-experimental
```

## 7. Actualiza código

Ver `api/core/database.py` (ya actualizado)

---

## Migra datos locales (opcional)

```bash
# Dump de SQLite local
sqlite3 movies.db .dump > movies.sql

# Ejecuta en Turso
turso db shell movie-note < movies.sql
```

---

## Beneficios de Turso

- ✅ Sintaxis SQLite (no cambias queries)
- ✅ Gratis hasta 9GB
- ✅ Edge deployment (rápido)
- ✅ SQLModel funciona igual
