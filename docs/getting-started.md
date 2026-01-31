# Getting Started with Glyphh

This guide walks you through installing Glyphh, building your first model, and deploying it to production.

## Prerequisites

- Python 3.9+
- pip or conda
- Docker (for runtime deployment)

## Installation

### SDK Installation

```bash
pip install glyphh
```

Verify installation:

```bash
glyphh --version
```

### Runtime Installation (Docker)

```bash
docker pull ghcr.io/glyphh/runtime:latest
```

Or use the lite version (no LLM fallback):

```bash
docker pull ghcr.io/glyphh/runtime:lite
```

## Your First Model

### 1. Create a Model

Create a file called `notebook.py`:

```python
from glyphh import GlyphhModel, Concept, EncoderConfig

# Configure the encoder
config = EncoderConfig(
    dimension=10000,  # Vector dimension (higher = more capacity)
    seed=42,          # Reproducible encoding
)

# Create model
model = GlyphhModel(config)

# Define concepts
concepts = [
    Concept(
        name="machine learning",
        attributes={
            "domain": "artificial intelligence",
            "type": "technique",
            "description": "Systems that learn from data"
        }
    ),
    Concept(
        name="neural network",
        attributes={
            "domain": "artificial intelligence",
            "type": "architecture",
            "description": "Computing systems inspired by biological brains"
        }
    ),
]

# Encode concepts
for concept in concepts:
    glyph = model.encode(concept)
    print(f"Encoded: {concept.name}")

# Test similarity search
print("\nSimilarity search for 'AI techniques':")
results = model.similarity_search("AI techniques", top_k=3)
for result in results:
    print(f"  {result.concept}: {result.score:.3f}")
```

Run it:

```bash
python notebook.py
```

### 2. Export the Model

```python
# Export as .glyphh file
model.export("my-model.glyphh")
```

Or use the CLI:

```bash
glyphh export notebook.py -o my-model.glyphh
```

## Deploying to Runtime

### 1. Start the Runtime

Create `docker-compose.yml`:

```yaml
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
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

Start it:

```bash
docker-compose up -d
```

### 2. Deploy Your Model

```bash
curl -X POST http://localhost:8000/api/deploy \
  -H "Content-Type: application/octet-stream" \
  --data-binary @my-model.glyphh
```

### 3. Query Your Model

```bash
curl -X POST http://localhost:8000/api/v1/my-model/search \
  -H "Content-Type: application/json" \
  -d '{"query": "AI techniques", "top_k": 5}'
```

## Next Steps

- [SDK Reference](sdk-reference.md) - Complete SDK API documentation
- [Runtime Deployment](runtime-deployment.md) - Production deployment guide
- [API Reference](api-reference.md) - REST and MCP API documentation
