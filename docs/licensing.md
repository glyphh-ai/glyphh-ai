# Licensing

## Glyphh SDK

The SDK is **MIT Licensed** - free for any use.

## Glyphh Runtime

### Development Mode (Free)

```bash
docker run -e DEPLOYMENT_MODE=local ghcr.io/glyphh/runtime:latest
```

Development mode is free with the following limits:

| Resource | Limit |
|----------|-------|
| Models | 1 |
| Glyphs per model | 1,000 |
| Authentication | Disabled |
| License validation | Not required |

These limits are designed for local development and testing. For production use, upgrade to a licensed deployment.

### Production Mode (License Required)

```bash
docker run \
  -e DEPLOYMENT_MODE=self-hosted \
  -e LICENSE_KEY=GLYPHH-XXXX-XXXX-XXXX-XXXX \
  -e JWT_SECRET_KEY=your-secret \
  ghcr.io/glyphh/runtime:latest
```

Production mode removes all limits:

| Resource | Limit |
|----------|-------|
| Models | Unlimited |
| Glyphs per model | Unlimited |
| Authentication | JWT required |
| License validation | Required |

### License Validation

In `self-hosted` mode:
- Validates on startup via Platform API
- Revalidates every 24 hours
- 7-day grace period if validation fails
- Continues operating offline during grace period

### Get a License

Contact [sales@glyphh.com](mailto:sales@glyphh.com) for production licenses.

### License Key Format

```
GLYPHH-XXXX-XXXX-XXXX-XXXX
```

Store securely using environment variables or secrets management.

## Comparison

| Feature | Development | Production |
|---------|-------------|------------|
| Price | Free | Contact us |
| Models | 1 | Unlimited |
| Glyphs | 1,000 | Unlimited |
| Auth | None | JWT |
| Support | Community | Priority |
| SLA | None | Available |
