# Runtime Deployment Guide

Deploy the Glyphh Runtime in production environments.

## Deployment Modes

| Mode | Auth | License | Use Case |
|------|------|---------|----------|
| `local` | Disabled | Not required | Development |
| `self-hosted` | JWT | Call-home | On-premise |
| `cloud` | JWT | Internal | Managed cloud |

### Mode Comparison

| Feature | Local | Self-Hosted | Cloud |
|---------|-------|-------------|-------|
| Authentication | Bypassed | JWT required | JWT required |
| License validation | None | Platform API | Internal |
| Max models | **1** | Unlimited | Unlimited |
| Max glyphs | **1,000** | Unlimited | Unlimited |
| Grace period | N/A | 7 days | N/A |
| API docs (/docs) | Enabled | Disabled | Disabled |

### Local Mode Limits

Local mode is free for development with these hard limits:

| Resource | Limit |
|----------|-------|
| Models | 1 |
| Glyphs per model | 1,000 |

These limits encourage upgrading to a production license for real workloads.

> **Note:** Local mode is not suitable for production. Use `self-hosted` or `cloud` for production deployments.

## Docker Images

```bash
# Full (with LLM fallback)
docker pull ghcr.io/glyphh/runtime:latest

# Lite (rules-only)
docker pull ghcr.io/glyphh/runtime:lite
```

## Local Development

```yaml
# docker-compose.yml
version: '3.8'
services:
  runtime:
    image: ghcr.io/glyphh/runtime:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://glyphh:glyphh@db:5432/glyphh_runtime
      - DEPLOYMENT_MODE=local
    depends_on:
      - db

  db:
    image: pgvector/pgvector:pg16
    environment:
      - POSTGRES_USER=glyphh
      - POSTGRES_PASSWORD=glyphh
      - POSTGRES_DB=glyphh_runtime
```

## Production Deployment

### Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
DEPLOYMENT_MODE=self-hosted
JWT_SECRET_KEY=your-256-bit-secret
LICENSE_KEY=GLYPHH-XXXX-XXXX-XXXX-XXXX
```

### JWT Authentication

```python
import jwt
from datetime import datetime, timedelta

token = jwt.encode({
    "sub": "user-123",
    "namespaces": ["my-model"],
    "permissions": {"my-model": ["read", "write"]},
    "exp": datetime.utcnow() + timedelta(hours=24)
}, "your-secret", algorithm="HS256")
```

### Health Checks

```bash
GET /health        # Liveness
GET /health/ready  # Readiness
GET /metrics       # Prometheus
```

## Licensing

| Tier | Mode | Requirements |
|------|------|--------------|
| Development | `local` | Free, no license needed |
| Self-Hosted | `self-hosted` | License key + call-home validation |
| Cloud | `cloud` | Managed by Glyphh |

### Self-Hosted License Behavior

- **Validation:** Calls `platform.glyphh.com/api/v1/licenses/validate` on startup
- **Revalidation:** Every 24 hours
- **Grace Period:** 7 days if validation fails (network issues, etc.)
- **Expiration:** Runtime stops accepting requests after grace period

### Resource Quotas

All deployment modes enforce resource quotas per namespace:

| Resource | Default Limit | Configurable |
|----------|---------------|--------------|
| Glyphs | 1,000,000 | Yes |
| Storage | 10 GB | Yes |
| Memory | 1024 MB | Yes |

Quotas can be adjusted via the `/namespaces/{namespace}/quotas` endpoint (admin permission required).

Contact [sales@glyphh.com](mailto:sales@glyphh.com) for production licenses.
