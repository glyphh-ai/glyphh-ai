# SDK and Runtime Configuration Relationship

This guide explains the relationship between SDK configuration (EncoderConfig) and Runtime configuration (ModelScopeConfig).

## Configuration Types

### EncoderConfig (SDK)

Defines **what gets encoded** - the structure and parameters for encoding concepts into glyphs.

```python
from glyphh import EncoderConfig, LayerConfig, SegmentConfig, Role

config = EncoderConfig(
    dimension=10000,              # Vector dimension
    seed=42,                      # Random seed for reproducibility
    similarity_weight=1.0,        # Cortex-level weight
    security_weight=1.0,          # Security filtering weight
    layers=[
        LayerConfig(
            name="semantic",
            segments=[
                SegmentConfig(
                    name="attributes",
                    roles=[
                        Role(name="type"),
                        Role(name="color"),
                    ]
                )
            ]
        )
    ]
)
```

**Key characteristics:**
- Defined at model creation time
- Travels with the `.glyphh` file
- Changes require re-encoding all glyphs
- Immutable after deployment (without re-encode)

### ModelScopeConfig (Runtime)

Defines **how searches work** - query parameters that can be adjusted without re-encoding.

```python
# Updated via PATCH /api/models/{org_id}/{model_id}/config
{
    "similarity_weights": {
        "semantic": 1.0,
        "temporal": 0.2
    },
    "beam_width": 5,
    "max_tree_depth": 3
}
```

**Key characteristics:**
- Stored in Runtime
- Can be updated without redeployment
- Changes apply immediately (hot update)
- Does not affect encoded glyphs

## Configuration Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SDK (Development)                               │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │  EncoderConfig  │───▶│     Encoder     │───▶│   GlyphhModel   │        │
│  │  - dimension    │    │  - encode()     │    │  - glyphs       │        │
│  │  - seed         │    │  - bind()       │    │  - config       │        │
│  │  - layers       │    │  - bundle()     │    │  - metadata     │        │
│  └─────────────────┘    └─────────────────┘    └────────┬────────┘        │
│                                                          │                  │
│                                                          ▼                  │
│                                                   ┌─────────────┐          │
│                                                   │ .glyphh file│          │
│                                                   │ (packaged)  │          │
│                                                   └──────┬──────┘          │
└──────────────────────────────────────────────────────────┼──────────────────┘
                                                           │
                                                           │ Deploy
                                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Runtime (Production)                              │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │ EncoderConfig   │    │ ModelScopeConfig│    │   Query Engine  │        │
│  │ (from .glyphh)  │    │ (hot-updatable) │───▶│  - search()     │        │
│  │                 │    │ - sim_weights   │    │  - fact_tree()  │        │
│  │                 │    │ - beam_width    │    │  - predict()    │        │
│  └────────┬────────┘    └─────────────────┘    └─────────────────┘        │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐                                                       │
│  │ Runtime Encoder │◀── Used for listener endpoint encoding                │
│  │ (from config)   │                                                       │
│  └─────────────────┘                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## When to Use Each

### EncoderConfig Changes

Use when you need to change:
- Vector dimension
- Layer/segment/role structure
- Encoding seed
- What attributes are encoded

**Process:**
1. Update EncoderConfig in SDK
2. Re-encode all concepts
3. Re-package model
4. Re-deploy to Runtime

### ModelScopeConfig Changes

Use when you need to change:
- Similarity weights (layer importance)
- Beam width (search breadth)
- Max tree depth (fact tree depth)

**Process:**
1. Call PATCH `/api/models/{org_id}/{model_id}/config`
2. Changes apply immediately

## Hot Updates

ModelScopeConfig supports hot updates - changes apply immediately without:
- Re-encoding glyphs
- Restarting Runtime
- Redeploying model

```bash
# Update similarity weights
curl -X PATCH http://localhost:8000/api/models/my-org/my-model/config \
  -H "Content-Type: application/json" \
  -d '{
    "similarity_weights": {"semantic": 1.0, "temporal": 0.5},
    "beam_width": 10
  }'
```

## Re-encoding

When EncoderConfig changes are needed after deployment:

```bash
# Trigger re-encode
curl -X POST http://localhost:8000/api/models/my-org/my-model/re-encode
```

This re-encodes all glyphs using the new configuration. Use sparingly as it's resource-intensive.

## Best Practices

1. **Plan EncoderConfig carefully** - Changes require re-encoding
2. **Use ModelScopeConfig for tuning** - Adjust weights without re-encoding
3. **Test locally first** - Validate config before production deployment
4. **Version your models** - Track config changes with semantic versioning

## Related Documentation

- [SDK Reference](../sdk-reference.md) - EncoderConfig details
- [Runtime API](../api-reference.md) - Config update endpoints
- [Local Development](local-development.md) - Testing workflow
