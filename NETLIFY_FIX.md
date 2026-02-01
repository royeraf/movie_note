# 🚀 Pasos para Arreglar el Error 404 en Netlify

## ✅ Cambios Realizados

He corregido la estructura de las funciones de Netlify. El problema era que estábamos usando una estructura de carpetas (`app/`) cuando Netlify espera archivos de función individuales.

### Estructura Anterior (❌ Incorrecta):
```
netlify/functions/
  └── app/
      └── main.py
```

### Estructura Nueva (✅ Correcta):
```
netlify/functions/
  ├── api.py              # Handler de la función
  ├── api/                # Directorio copiado durante build
  └── requirements.txt
```

## 📝 Archivos Modificados

1. **`netlify/functions/api.py`** - Nueva función serverless
2. **`netlify.toml`** - Redirect actualizado a `/api` en lugar de `/app`
3. **`build-netlify.sh`** - Copia archivos a la ubicación correcta
4. **`.gitignore`** - Actualizado para la nueva estructura

## 🔄 Próximos Pasos

### 1. Haz commit y push de los cambios:

```bash
git add .
git commit -m "Fix Netlify function structure - use api.py instead of app folder"
git push
```

### 2. Netlify re-desplegará automáticamente

Netlify detectará los cambios y:
- Ejecutará `build-netlify.sh`
- Copiará el directorio `api/` a `netlify/functions/`
- Creará la función serverless desde `api.py`
- Configurará los redirects correctamente

### 3. Verifica que las variables de entorno estén configuradas

En el dashboard de Netlify:
- Ve a **Site settings** → **Environment variables**
- Asegúrate de tener:
  - `OMDB_API_KEY` = tu_clave
  - `TMDB_API_KEY` = tu_clave (opcional)

### 4. Espera a que termine el deploy

- Ve a **Deploys** en el dashboard de Netlify
- Espera a que el deploy termine (debería tomar 2-3 minutos)
- Revisa los logs si hay errores

### 5. Prueba los endpoints

Una vez desplegado, prueba:

**Health Check:**
```
https://movienotes2001.netlify.app/api/health
```
Debería retornar: `{"status":"ok"}`

**Búsqueda:**
```
https://movienotes2001.netlify.app/api/search?query=matrix
```
Debería retornar resultados de películas

**Películas guardadas:**
```
https://movienotes2001.netlify.app/api/movies
```
Debería retornar un array (vacío al principio)

## 🔍 Cómo Funciona Ahora

1. **Request**: Usuario busca "matrix" → `/api/search?query=matrix`
2. **Netlify Redirect**: Netlify intercepta y redirige a `/.netlify/functions/api/search?query=matrix`
3. **Function Handler**: `api.py` recibe la request
4. **FastAPI**: El handler pasa la request a tu app FastAPI
5. **Router**: FastAPI enruta a `api/v1/endpoints/search.py`
6. **Response**: La función retorna los resultados

## ⚠️ Notas Importantes

### Base de Datos SQLite
La base de datos SQLite **NO persistirá** entre invocaciones de la función porque Netlify Functions son stateless. Cada vez que se invoca la función, empieza con una base de datos vacía.

**Soluciones:**
1. **Netlify Blobs** (Recomendado para este proyecto):
   ```bash
   npm install @netlify/blobs
   ```
   
2. **Supabase** (PostgreSQL gratis):
   - Crea cuenta en supabase.com
   - Usa SQLModel con PostgreSQL en lugar de SQLite

3. **PlanetScale** (MySQL gratis):
   - Similar a Supabase pero MySQL

### Testing Local

Para probar localmente antes de desplegar:

```bash
# Instala Netlify CLI si no lo tienes
npm install -g netlify-cli

# Ejecuta el build
bash build-netlify.sh

# Inicia el servidor de desarrollo de Netlify
netlify dev
```

Esto simulará el entorno de Netlify localmente.

## 🐛 Solución de Problemas

### Si sigues viendo 404:

1. **Revisa los logs de la función en Netlify**:
   - Dashboard → Functions → api
   - Busca errores de importación o runtime

2. **Verifica que el build se completó**:
   - Dashboard → Deploys → [último deploy]
   - Revisa que no haya errores en el build

3. **Verifica la estructura de archivos**:
   - En el deploy log, busca "Functions bundled"
   - Debería mostrar `api.py`

### Si ves errores de importación:

1. Verifica que `requirements.txt` esté en `netlify/functions/`
2. Asegúrate de que todas las dependencias estén listadas
3. Revisa los logs de build para ver si pip instaló todo correctamente

### Si la base de datos no funciona:

Esto es **esperado** - necesitas implementar persistencia externa (ver sección de Base de Datos arriba).

## 📊 Estructura Final del Proyecto

```
movie_note/
├── api/                          # Backend FastAPI (original)
│   ├── core/
│   ├── models/
│   ├── v1/
│   │   └── endpoints/
│   │       ├── search.py
│   │       └── movies.py
│   ├── index.py
│   └── requirements.txt
├── netlify/
│   └── functions/
│       ├── api.py               # ✅ Handler de Netlify
│       ├── api/                 # ✅ Copiado durante build (gitignored)
│       └── requirements.txt     # ✅ Dependencias de Python
├── src/                         # Frontend Vue
├── dist/                        # Build del frontend
├── build-netlify.sh            # Script de build
├── netlify.toml                # Configuración de Netlify
└── package.json
```

## ✨ Resumen

El problema era la estructura de carpetas. Netlify Functions espera archivos `.py` individuales en `netlify/functions/`, no subcarpetas con `main.py`.

Ahora:
- ✅ `api.py` es el handler principal
- ✅ El directorio `api/` se copia durante el build
- ✅ Los redirects apuntan a `/.netlify/functions/api`
- ✅ Todo debería funcionar después del próximo deploy

**¡Haz push de los cambios y espera a que Netlify termine el deploy!**
