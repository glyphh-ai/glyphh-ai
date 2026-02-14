# Local Development Workflow

This guide walks you through the complete local development workflow for building and testing Glyphh models.

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Glyphh SDK installed (`pip install glyphh`)

## Workflow Overview

```
1. Initialize Model → 2. Add Concepts → 3. Package → 4. Deploy → 5. Query
```

## Step 1: Initialize a Model

```bash
# Create a new model with default configuration
glyphh build init --name my_model --dimension 10000

# This creates model.json with:
# - Model name
# - EncoderConfig (dimension, seed, layers)
# - Empty concepts array
```

## Step 2: Add Concepts

### Via CLI

```bash
# Add concepts one at a time
glyphh build add --concept "red car" --attributes '{"type":"car","color":"red"}'
glyphh build add --concept "blue truck" --attributes '{"type":"truck","color":"blue"}'

# List concepts
glyphh build list
```

### Via Python

```python
from glyphh import Encoder, EncoderConfig, Concept

config = EncoderConfig(dimension=10000, seed=42)
encoder = Encoder(config)

concepts = [
    Concept(name="red car", attributes={"type": "car", "color": "red"}),
    Concept(name="blue truck", attributes={"type": "truck", "color": "blue"}),
]

glyphs = [encoder.encode(c) for c in concepts]
```

## Step 3: Package the Model

```bash
# Create .glyphh package
glyphh package create --output my_model.glyphh --version 1.0.0

# Validate the package
glyphh package validate my_model.glyphh

# View package info
glyphh package info my_model.glyphh
```

## Step 4: Start Local Runtime

```bash
# Generate local .env configuration
glyphh runtime init --scenario local

# Start runtime with Docker Compose
docker-compose up -d

# Check status
glyphh runtime status
```

## Step 5: Deploy and Query

```bash
# Deploy the model
glyphh runtime deploy my_model.glyphh

# Query via CLI
glyphh query "FIND SIMILAR TO 'red car'" --runtime http://localhost:8000 --org local --model-id my_model

# Or use natural language
glyphh query "find similar to red car" --nl --runtime http://localhost:8000 --org local --model-id my_model
```

## Iterating on Your Model

When you make changes:

1. Update concepts in model.json or via CLI
2. Re-package: `glyphh package create --output my_model.glyphh`
3. Re-deploy: `glyphh runtime deploy my_model.glyphh`

## Troubleshooting

### Runtime not starting

```bash
# Check Docker logs
docker-compose logs runtime

# Verify database is running
docker-compose ps
```

### Connection refused

```bash
# Ensure runtime is running
glyphh runtime status

# Check .env configuration
cat .env
```

## Next Steps

- [Cloud Deployment](cloud-deployment.md) - Deploy to production
- [Data Loading](data-loading.md) - Load data via listener endpoint
