# Cloud Deployment Workflow

This guide covers deploying Glyphh models to production environments.

## Deployment Options

| Option | Description | Best For |
|--------|-------------|----------|
| Self-Hosted | Your infrastructure (Heroku, AWS, etc.) | Full control |
| Glyphh Cloud | Managed service | Simplicity |

## Self-Hosted Deployment

### 1. Get a License Key

1. Visit https://platform.glyphh.com
2. Navigate to Settings → Licensing
3. Generate a license key for your deployment

### 2. Configure Environment

```bash
# Generate self-hosted template
glyphh runtime init --scenario self-hosted -o .env.production
```

Edit `.env.production`:

```bash
RUNTIME_URL=https://your-app.herokuapp.com
JWT_TOKEN=your_jwt_token_here
```

### 3. Deploy Runtime

#### Heroku

```bash
# Create app
heroku create my-glyphh-runtime

# Set stack to container
heroku stack:set container

# Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# Set config vars
heroku config:set DEPLOYMENT_MODE=self-hosted
heroku config:set JWT_SECRET_KEY=your-secret-key
heroku config:set LICENSE_KEY=your-license-key

# Deploy
git push heroku main
```

#### AWS ECS

See [AWS Deployment Guide](../runtime-deployment.md#aws-ecs) for detailed instructions.

### 4. Deploy Your Model

```bash
glyphh runtime deploy my_model.glyphh --env-file .env.production
```

## Glyphh Cloud Deployment

### 1. Get API Token

1. Visit https://platform.glyphh.com
2. Navigate to Settings → API Tokens
3. Generate a Runtime Token

### 2. Configure Environment

```bash
glyphh runtime init --scenario cloud -o .env.cloud
```

Edit `.env.cloud`:

```bash
RUNTIME_URL=https://runtime.glyphh.com
JWT_TOKEN=your_jwt_token_here
```

### 3. Deploy

```bash
glyphh runtime deploy my_model.glyphh --env-file .env.cloud
```

### 4. Access Endpoints

After deployment, you'll receive:

- MCP endpoint: `https://runtime.glyphh.com/<org_id>/<model_id>/mcp`
- Listener endpoint: `https://runtime.glyphh.com/<org_id>/<model_id>/listener`

## Authentication

### Runtime Tokens (CLI)

Used for deploying models via CLI:

```bash
# Set in .env
JWT_TOKEN=your_runtime_token
```

### Consumer Tokens (Applications)

Used by your applications to query the model:

1. Deploy your model
2. Go to Platform UI → Models → Your Model → Tokens
3. Generate Consumer Token
4. Use in your application's Authorization header

## Monitoring

### Check Status

```bash
glyphh runtime status --env-file .env.production
```

### View Logs

```bash
glyphh runtime logs --env-file .env.production -n 100
```

## Troubleshooting

### Authentication Error

```
❌ Authentication Error: Invalid or missing JWT token
```

**Solution:** Regenerate token from Platform UI.

### License Validation Failed

```
❌ License validation failed
```

**Solution:** Check LICENSE_KEY is correct and network can reach platform.glyphh.com.

## Next Steps

- [Data Loading](data-loading.md) - Load production data
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
