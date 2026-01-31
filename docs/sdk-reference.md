# SDK Reference

Complete API reference for the Glyphh SDK.

## Installation

```bash
pip install glyphh
```

## Core Classes

### GlyphhModel

The main class for building and querying Glyphh models.

```python
from glyphh import GlyphhModel, EncoderConfig

config = EncoderConfig(dimension=10000, seed=42)
model = GlyphhModel(config)
```

#### Methods

| Method | Description |
|--------|-------------|
| `encode(concept)` | Encode a concept into a glyph |
| `similarity_search(query, top_k)` | Find similar concepts |
| `generate_fact_tree(claim, max_depth)` | Generate verification tree |
| `predict_temporal(state, steps)` | Predict future states |
| `export(path)` | Export model to .glyphh file |
| `load(path)` | Load model from .glyphh file |

### Concept

Represents a concept to be encoded.

```python
from glyphh import Concept

concept = Concept(
    name="machine learning",
    attributes={"domain": "AI", "type": "technique"}
)
```

### EncoderConfig

Configuration for the HDC encoder.

```python
from glyphh import EncoderConfig

config = EncoderConfig(
    dimension=10000,  # Vector dimension
    seed=42,          # Random seed
    space_id="default"
)
```

### IntentEncoder

Encoder for natural language query matching.

```python
from glyphh import IntentEncoder, IntentPattern

intent_encoder = IntentEncoder(config)
intent_encoder.add_defaults()

match = intent_encoder.match_intent("find similar to X")
print(f"Intent: {match.intent_type}, Confidence: {match.confidence}")
```

## Edge Types

| Edge Type | Description |
|-----------|-------------|
| `similarity` | Semantically similar |
| `contrast` | Opposites |
| `analogy` | Analogical relationship |
| `composition` | Part-of relationship |
| `precedes` | Temporal: comes before |
| `follows` | Temporal: comes after |
| `causes` | Causal relationship |
| `prevents` | Prevention relationship |

## CLI Commands

```bash
glyphh --version           # Show version
glyphh export FILE -o OUT  # Export model
glyphh deploy MODEL --runtime URL  # Deploy to runtime
glyphh query "text" --namespace NS  # Query runtime
```
