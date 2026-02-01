# SDK Reference

Complete API reference for the Glyphh SDK.

## Installation

```bash
pip install glyphh
```

## Core Classes

### EncoderConfig

Configuration for the HDC encoder with explicit nested structure.

```python
from glyphh import EncoderConfig, LayerConfig, SegmentConfig, Role

config = EncoderConfig(
    dimension=10000,              # Vector dimension
    seed=42,                      # Random seed for reproducibility
    similarity_weight=1.0,        # Cortex-level similarity weight
    security_weight=1.0,          # Cortex-level security weight
    apply_weights_during_encoding=False,  # Weighting strategy
    layers=[
        LayerConfig(
            name="semantic",
            similarity_weight=0.8,
            security_weight=0.9,
            segments=[
                SegmentConfig(
                    name="attributes",
                    similarity_weight=1.0,
                    roles=[
                        Role(name="type", similarity_weight=1.0),
                        Role(name="category", similarity_weight=0.8),
                        Role(name="id", similarity_weight=0.5, primary_id=True),
                    ]
                )
            ]
        ),
        LayerConfig(
            name="temporal",
            similarity_weight=0.2,
            segments=[
                SegmentConfig(
                    name="window",
                    roles=[Role(name="observed_at")]
                )
            ]
        )
    ]
)
```

#### Configuration Hierarchy

```
EncoderConfig (cortex-level)
├── dimension: int
├── seed: int
├── similarity_weight: float (0.0-1.0)
├── security_weight: float (0.0-1.0)
├── apply_weights_during_encoding: bool
└── layers: List[LayerConfig]
      └── LayerConfig
            ├── name: str
            ├── similarity_weight: float
            ├── security_weight: float
            └── segments: List[SegmentConfig]
                  └── SegmentConfig
                        ├── name: str
                        ├── similarity_weight: float
                        ├── security_weight: float
                        └── roles: List[Role]
                              └── Role
                                    ├── name: str
                                    ├── similarity_weight: float
                                    ├── security_weight: float
                                    └── primary_id: bool
```

#### Weighting Strategies

| Strategy | `apply_weights_during_encoding` | Description |
|----------|--------------------------------|-------------|
| Similarity-time (default) | `False` | Weights stored in glyph, applied during similarity computation |
| Encoding-time | `True` | Weights baked into encoding via weighted bundling |

### Encoder

The main class for encoding concepts into glyphs.

```python
from glyphh import Encoder, EncoderConfig, Concept

config = EncoderConfig(dimension=10000, seed=42)
encoder = Encoder(config)

concept = Concept(
    name="red car",
    attributes={"type": "car", "color": "red", "size": "medium"}
)
glyph = encoder.encode(concept)
```

#### Methods

| Method | Description |
|--------|-------------|
| `encode(concept)` | Encode a concept into a glyph |
| `generate_symbol(key)` | Generate a deterministic symbol vector |
| `bind(role, value)` | Bind a role vector to a value vector |
| `bundle(vectors)` | Bundle multiple vectors via majority vote |
| `weighted_bundle(weighted_vectors)` | Bundle with weights |
| `get_cache_size()` | Get number of cached symbols |
| `clear_cache()` | Clear the symbol cache |

### Concept

Represents a concept to be encoded.

```python
from glyphh import Concept

concept = Concept(
    name="machine learning",
    attributes={
        "domain": "AI",
        "type": "technique",
        "description": "Systems that learn from data"
    },
    relationships=[
        {"type": "related_to", "target": "neural networks"},
        {"type": "used_in", "target": "data science"}
    ],
    metadata={"source": "textbook", "chapter": 1}
)
```

### Glyph

The encoded representation of a concept.

```python
# Glyphs are created by encoding concepts
glyph = encoder.encode(concept)

# Access glyph properties
print(glyph.name)           # Concept name
print(glyph.identifier)     # Unique ID with timestamp
print(glyph.space_id)       # Vector space identifier
print(glyph.global_cortex)  # Top-level vector
print(glyph.layers)         # Hierarchical structure
```

### SimilarityCalculator

Computes similarity between glyphs.

```python
from glyphh import SimilarityCalculator

calculator = SimilarityCalculator(
    threshold=0.5,           # Visibility threshold
    default_metric="cosine"  # "cosine" or "hamming"
)

result = calculator.compute(glyph1, glyph2)
print(f"Score: {result.score:.3f}")
print(f"Visible: {result.visible}")
print(f"Metric: {result.metric}")
```

#### Edge Types for Similarity

| Edge Type | Description |
|-----------|-------------|
| `neural_cortex` | Global cortex comparison |
| `neural_layer` | Layer-level comparison |
| `neural_segment` | Segment-level comparison |
| `neural_role` | Role-level comparison |

### GlyphhModel

Packages glyphs for deployment.

```python
from glyphh import GlyphhModel

model = GlyphhModel(
    name="my-model",
    version="1.0.0",
    encoder_config=config,
    glyphs=[glyph1, glyph2, glyph3],
    metadata={"domain": "AI", "description": "AI concepts"}
)

# Save to file
model.to_file("my-model.glyphh")

# Load from file
loaded = GlyphhModel.from_file("my-model.glyphh")
```

### IntentEncoder

Encoder for natural language query matching.

```python
from glyphh import IntentEncoder, IntentPattern

intent_encoder = IntentEncoder(encoder)
intent_encoder.add_defaults()

match = intent_encoder.match_intent("find similar to X")
print(f"Intent: {match.intent_type}")
print(f"Confidence: {match.confidence}")
print(f"Extracted: {match.extracted_values}")
```

### TemporalEncoder

Computes temporal deltas between glyph versions.

```python
from glyphh import TemporalEncoder

temporal = TemporalEncoder(encoder)

# Compute delta between versions
delta = temporal.compute_delta(glyph_v1, glyph_v2)

# Apply delta to predict next state
predicted = temporal.apply_delta(glyph_v2, delta)
```

### BeamSearchPredictor

Predicts future states using beam search.

```python
from glyphh import BeamSearchPredictor

predictor = BeamSearchPredictor(
    encoder=encoder,
    beam_width=5,
    drift_reduction=True
)

# Predict 3 time steps into the future
predictions = predictor.predict(
    history=[glyph_t1, glyph_t2, glyph_t3],
    time_intervals=3,
    hierarchy_level="cortex"
)

for pred in predictions:
    print(f"Confidence: {pred.confidence:.3f}")
```

### FactTree

Provides explainability for computations.

```python
from glyphh import FactTree, FactNode, Citation

# Fact trees are generated during similarity computation
result = calculator.compute(glyph1, glyph2, generate_fact_tree=True)
fact_tree = result.fact_tree

# Export for inspection
print(fact_tree.to_text())
json_str = fact_tree.to_json()
```

### EdgeGenerator

Generates edges for multi-level reasoning.

```python
from glyphh import EdgeGenerator

generator = EdgeGenerator(encoder)

# Generate spatial edges (for similarity)
spatial_edges = generator.generate_spatial_edges(glyph)

# Generate temporal edges (for change detection)
temporal_edges = generator.generate_temporal_edges(glyph_v1, glyph_v2)
```

## Edge Types

### Spatial Edges (Similarity)

| Edge Type | Description |
|-----------|-------------|
| `neural_cortex` | Global cortex similarity |
| `neural_layer` | Layer-level similarity |
| `neural_segment` | Segment-level similarity |
| `neural_role` | Role-level similarity |

### Temporal Edges (Change Detection)

| Edge Type | Description |
|-----------|-------------|
| `temporal_cortex` | Global change delta |
| `temporal_layer` | Layer-level change |
| `temporal_segment` | Segment-level change |
| `temporal_role` | Role-level change |

## CLI Commands

```bash
glyphh --version                    # Show version
glyphh build FILE -o OUT            # Build model from notebook
glyphh runtime init --scenario X    # Initialize runtime config
glyphh runtime deploy MODEL         # Deploy to runtime
glyphh runtime status               # Check runtime status
```

## Migration from Legacy Config

If you have code using the old config format:

```python
from glyphh import migrate_legacy_config

# Old format
old_config = {
    "dimension": 10000,
    "seed": 42,
    "num_layers": 2,
    "segments_per_layer": 3,
    "default_roles": ["type", "value"]
}

# Convert to new format
new_config = migrate_legacy_config(**old_config)
```
