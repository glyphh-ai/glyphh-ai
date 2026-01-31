# API Reference

REST and MCP API reference for the Glyphh Runtime.

## Authentication

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/...
```

## Deployment API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/deploy` | POST | Deploy .glyphh model |
| `/api/status` | GET | Runtime status |
| `/api/models` | GET | List models |
| `/api/models/{ns}` | DELETE | Remove model |

## Query API

### Similarity Search

```http
POST /api/v1/{namespace}/search
Content-Type: application/json

{"query": "machine learning", "top_k": 10}
```

### Fact Tree

```http
POST /api/v1/{namespace}/fact-tree
Content-Type: application/json

{"claim": "deep learning uses neural networks", "max_depth": 3}
```

### Temporal Prediction

```http
POST /api/v1/{namespace}/predict
Content-Type: application/json

{"current_state": ["data collection"], "steps_ahead": 3}
```

### Natural Language Query

```http
POST /api/v1/{namespace}/query
Content-Type: application/json

{"query": "find similar to machine learning"}
```

## Glyph CRUD

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/{ns}/glyphs` | POST | Create glyph |
| `/api/v1/{ns}/glyphs/{id}` | GET | Get glyph |
| `/api/v1/{ns}/glyphs/{id}` | PUT | Update glyph |
| `/api/v1/{ns}/glyphs/{id}` | DELETE | Delete glyph |

## MCP Tools

| Tool | Description |
|------|-------------|
| `glyph_similarity_search` | Find similar glyphs |
| `glyph_fact_tree` | Generate fact tree |
| `glyph_temporal_predict` | Predict states |
| `glyph_create` | Create glyph |
| `glyph_get` | Get glyph |
| `glyph_list` | List glyphs |

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request |
| `AUTHENTICATION_ERROR` | 401 | Invalid token |
| `AUTHORIZATION_ERROR` | 403 | No permission |
| `NOT_FOUND` | 404 | Not found |
| `UNPROCESSABLE_QUERY` | 422 | NL query failed |
