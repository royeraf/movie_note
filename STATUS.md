# ⏳ Esperando Deploy

Push realizado. Netlify está desplegando.

Espera 2-3 minutos y prueba:

```
https://movienotes2001.netlify.app/api/health
https://movienotes2001.netlify.app/api/search?query=matrix
https://movienotes2001.netlify.app/api/movies
```

Si aún falla, verifica en Netlify Dashboard → Functions que la función `api` aparezca listada.
