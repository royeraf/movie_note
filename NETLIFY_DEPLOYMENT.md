# Netlify Deployment Guide

## El Problema

El error `404 (Not Found)` en `/api/search` ocurre porque Netlify no sabe cómo enrutar las solicitudes de API a tu función serverless de Python.

## La Solución

He configurado tu proyecto para que funcione correctamente en Netlify. Aquí está lo que se ha hecho:

### 1. Archivos Creados/Modificados

- **`netlify.toml`**: Configuración de Netlify que:
  - Define el comando de build
  - Configura redirects de `/api/*` a las funciones serverless
  - Establece headers CORS

- **`build-netlify.sh`**: Script que:
  - Construye el frontend con Vite
  - Copia el directorio `api/` a `netlify/functions/app/`
  - Copia `requirements.txt` a `netlify/functions/`

- **`netlify/functions/app/main.py`**: Handler de la función serverless que importa tu aplicación FastAPI

### 2. Pasos para Desplegar en Netlify

#### Opción A: Desde el Dashboard de Netlify (Recomendado)

1. **Sube tu código a GitHub** (si aún no lo has hecho):
   ```bash
   git add .
   git commit -m "Configure Netlify deployment"
   git push
   ```

2. **Ve a [Netlify](https://app.netlify.com/)**

3. **Click en "Add new site" → "Import an existing project"**

4. **Conecta tu repositorio de GitHub**

5. **Configura las variables de entorno**:
   - Ve a "Site settings" → "Environment variables"
   - Agrega las siguientes variables:
     - `OMDB_API_KEY`: Tu clave de OMDb API
     - `TMDB_API_KEY`: Tu clave de TMDB API (opcional)

6. **Netlify detectará automáticamente el `netlify.toml`** y usará la configuración correcta

7. **Click en "Deploy site"**

#### Opción B: Usando Netlify CLI

1. **Instala Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

2. **Login a Netlify**:
   ```bash
   netlify login
   ```

3. **Inicializa el sitio**:
   ```bash
   netlify init
   ```

4. **Configura las variables de entorno**:
   ```bash
   netlify env:set OMDB_API_KEY "tu_clave_aqui"
   netlify env:set TMDB_API_KEY "tu_clave_aqui"
   ```

5. **Despliega**:
   ```bash
   netlify deploy --prod
   ```

### 3. Verificación Post-Despliegue

Una vez desplegado, verifica que todo funcione:

1. **Verifica el health check**:
   ```
   https://tu-sitio.netlify.app/api/health
   ```
   Debería retornar: `{"status": "ok"}`

2. **Prueba la búsqueda**:
   ```
   https://tu-sitio.netlify.app/api/search?query=matrix
   ```
   Debería retornar resultados de películas

3. **Verifica la documentación de la API**:
   ```
   https://tu-sitio.netlify.app/api/docs
   ```

### 4. Solución de Problemas

#### Si sigues viendo 404:

1. **Verifica los logs de la función**:
   - Ve a Netlify Dashboard → Functions → app
   - Revisa los logs para ver errores específicos

2. **Verifica las variables de entorno**:
   - Asegúrate de que `OMDB_API_KEY` y/o `TMDB_API_KEY` estén configuradas

3. **Verifica el build**:
   - Ve a Netlify Dashboard → Deploys → [último deploy]
   - Revisa los logs del build para asegurarte de que el script se ejecutó correctamente

#### Si ves errores de importación de Python:

1. **Verifica que `requirements.txt` esté en `netlify/functions/`**
2. **Asegúrate de que todas las dependencias estén listadas**

#### Si la base de datos no funciona:

Netlify Functions son stateless, por lo que la base de datos SQLite local no persistirá entre invocaciones. Considera:
- Usar Netlify Blobs para almacenamiento persistente
- Usar un servicio de base de datos externo (como Supabase, PlanetScale, etc.)

### 5. Estructura del Proyecto

```
movie_note/
├── api/                          # Backend FastAPI
│   ├── core/
│   ├── models/
│   ├── v1/
│   │   └── endpoints/
│   │       └── search.py        # Endpoint de búsqueda
│   ├── index.py                 # App principal
│   └── requirements.txt
├── netlify/
│   └── functions/
│       ├── app/
│       │   └── main.py          # Handler de Netlify
│       └── requirements.txt     # (copiado por build script)
├── src/                         # Frontend Vue
├── build-netlify.sh            # Script de build
└── netlify.toml                # Configuración de Netlify
```

### 6. Cómo Funciona

1. **Build**: Netlify ejecuta `build-netlify.sh` que:
   - Construye el frontend Vue → `dist/`
   - Copia `api/` a `netlify/functions/app/api/`

2. **Deploy**: Netlify:
   - Sirve archivos estáticos desde `dist/`
   - Crea una función serverless desde `netlify/functions/app/`
   - Instala dependencias de Python desde `netlify/functions/requirements.txt`

3. **Runtime**: Cuando haces una request a `/api/search`:
   - Netlify intercepta la request (gracias al redirect en `netlify.toml`)
   - La redirige a `/.netlify/functions/app/search`
   - La función Python procesa la request
   - Retorna la respuesta

## Notas Importantes

- ⚠️ **No olvides configurar las variables de entorno en Netlify**
- ⚠️ **La base de datos SQLite no persistirá** - considera usar un servicio externo
- ✅ **Los archivos copiados están en `.gitignore`** - no los commitees
- ✅ **El build script se ejecuta automáticamente** en cada deploy

## Testing Local

Para probar localmente antes de desplegar:

```bash
# Ejecuta el build script
bash build-netlify.sh

# Prueba las funciones localmente con Netlify CLI
netlify dev
```

Esto iniciará un servidor local que simula el entorno de Netlify.
