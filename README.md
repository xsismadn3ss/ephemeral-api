# Docker

El proyecto usa dos archivos Compose:

- `docker-compose.yml`: base para la API. No declara servicios auxiliares ni redes explícitas.
- `docker-compose.dev.yml`: override de desarrollo. Agrega MongoDB, Redis, healthchecks y dependencias de arranque.

Ambos usan el mismo set de variables de entorno definido en `.example.env`:

- `ENV`
- `MONGO_URI`
- `DB_NAME`
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_USER`
- `REDIS_PASSWORD`
- `PORT`

## Desarrollo

```bash
docker compose --env-file .example.env -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

Con `.example.env`, la API dentro de Docker usará `mongodb://mongo:27017` y `redis:6379`.

## Producción

```bash
docker compose --env-file .env -f docker-compose.yml up -d --build
```

En producción solo se levanta la API. MongoDB y Redis deben existir fuera de este Compose.

## Validación

```bash
docker compose -f docker-compose.yml config
docker compose --env-file .example.env -f docker-compose.yml -f docker-compose.dev.yml config
```
