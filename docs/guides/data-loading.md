# Data Loading Guide

This guide covers loading data into deployed Glyphh models.

## Loading Methods

| Method | Best For | Format |
|--------|----------|--------|
| Listener Endpoint | Real-time ingestion | JSON |
| Batch API | Bulk loading | JSON array |
| Studio UI | Manual entry | Form/CSV |

## Listener Endpoint

The listener endpoint accepts JSON concept data and encodes it using the deployed model's configuration.

### Single Concept

```bash
curl -X POST http://localhost:8000/<org_id>/<model_id>/listener \
  -H "Content-Type: application/json" \
  -d '{
    "concept": "red car",
    "attributes": {
      "type": "car",
      "color": "red"
    }
  }'
```

### Batch Concepts

```bash
curl -X POST http://localhost:8000/<org_id>/<model_id>/listener \
  -H "Content-Type: application/json" \
  -d '{
    "concepts": [
      {"concept": "red car", "attributes": {"type": "car", "color": "red"}},
      {"concept": "blue truck", "attributes": {"type": "truck", "color": "blue"}}
    ]
  }'
```

### Response

```json
{
  "created": 2,
  "failed": 0,
  "results": [
    {"index": 0, "glyph_id": "...", "status": "created"},
    {"index": 1, "glyph_id": "...", "status": "created"}
  ]
}
```

## Python Client

```python
import requests

RUNTIME_URL = "http://localhost:8000"
ORG_ID = "my-org"
MODEL_ID = "my-model"

def load_concept(concept: str, attributes: dict):
    response = requests.post(
        f"{RUNTIME_URL}/{ORG_ID}/{MODEL_ID}/listener",
        json={"concept": concept, "attributes": attributes}
    )
    return response.json()

# Load single concept
result = load_concept("red car", {"type": "car", "color": "red"})
print(f"Created glyph: {result['glyph_id']}")

# Load batch
concepts = [
    {"concept": "blue truck", "attributes": {"type": "truck", "color": "blue"}},
    {"concept": "green bike", "attributes": {"type": "bike", "color": "green"}},
]

response = requests.post(
    f"{RUNTIME_URL}/{ORG_ID}/{MODEL_ID}/listener",
    json={"concepts": concepts}
)
print(f"Created {response.json()['created']} glyphs")
```

## Error Handling

### Encoding Failure

If a concept fails to encode, the response includes the error:

```json
{
  "created": 1,
  "failed": 1,
  "results": [
    {"index": 0, "glyph_id": "...", "status": "created"},
    {"index": 1, "status": "failed", "error": "Missing required attribute: type"}
  ]
}
```

### Validation Errors

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid concept format",
    "details": {"field": "attributes", "issue": "must be an object"}
  }
}
```

## Best Practices

1. **Batch loading** - Use batch endpoint for bulk data (more efficient)
2. **Error handling** - Check `failed` count and handle errors
3. **Idempotency** - Include unique IDs in metadata for deduplication
4. **Rate limiting** - Respect rate limits (default: 60 req/min)

## Studio UI

For manual data entry:

1. Open Studio UI
2. Select your model
3. Click "Load Data"
4. Enter concepts via form or upload CSV

## Next Steps

- [Querying Data](../api-reference.md#query-endpoints) - Query your loaded data
- [Troubleshooting](troubleshooting.md) - Common loading issues
