# Infrastructure

Local development infrastructure is managed with Docker Compose.

## Services

- PostgreSQL 16: relational database
- Redis 7: broker/cache
- MinIO: S3-compatible object storage

## Start

```powershell
copy .env.example .env
docker compose up -d
```

## Stop

```powershell
docker compose down
```

## Verify config

```powershell
docker compose config
```
