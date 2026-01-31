# Glyphh Documentation

- [Getting Started](getting-started.md) - Install and build your first model
- [SDK Reference](sdk-reference.md) - SDK API documentation
- [Runtime Deployment](runtime-deployment.md) - Production deployment
- [API Reference](api-reference.md) - REST and MCP APIs
- [Licensing](licensing.md) - License information

## Quick Start

```bash
pip install glyphh
```

```python
from glyphh import GlyphhModel, Concept, EncoderConfig

config = EncoderConfig(dimension=10000, seed=42)
model = GlyphhModel(config)

concept = Concept(name="machine learning", attributes={"domain": "AI"})
model.encode(concept)

results = model.similarity_search("deep learning", top_k=5)
```
