<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="logo/glyphh-logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="logo/glyphh-logo.png">
    <img src="logo/glyphh-logo.png" alt="Glyphh Logo" width="200">
  </picture>
</p>

<p align="center">
  <strong>When your LLM can't afford to be wrong, sidecar it with Glyphh.</strong>
</p>

## The Sidecar for AI Agents

Glyphh isn't here to replace your LLM—it's here to make it better. 

LLMs are incredible at understanding context, generating content, and handling ambiguity. But they hallucinate. They can't cite sources. They give different answers to the same question. RAG helps with retrieval but still lets the LLM generate the final answer—and hallucinate along the way. Knowledge graphs provide structure but are rigid, expensive to maintain, and can't handle semantic similarity.

For many use cases, "good enough" is fine. For others—faq, compliance, medical, financial, legal—it's a dealbreaker.

**Glyphh is the deterministic sidecar that handles what LLMs can't:**

```
┌─────────────────────────────────────────────────┐
│                      AI Agent / LLM             │
│                                                 │
│   "What's our return policy?"                   │
│                    │                            │
│                    ▼                            │
│   ┌─────────────────────────────────────┐       │
│   │  Can Glyphh answer this?            │       │
│   │  (Rules-based intent matching)      │       │
│   └─────────────────────────────────────┘       │
│              │                    │             │
│         HIGH CONFIDENCE      LOW CONFIDENCE     │
│              │                    │             │
│              ▼                    ▼             │
│   ┌──────────────────┐  ┌──────────────────┐    │
│   │  Glyphh Runtime  │  │  LLM generates   │    │
│   │  (Deterministic) │  │  (Best effort)   │    │
│   │                  │  │                  │    │
│   │  ✓ Exact answer  │  │  ? May vary      │    │
│   │  ✓ With citation │  │  ? No citation   │    │
│   │  ✓ Audit trail   │  │  ? No audit      │    │
│   └──────────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────┘
```

**The pattern is simple:** Let Glyphh handle queries it can answer deterministically. Fall back to the LLM for everything else. Your agent gets the best of both worlds.

## What is Glyphh?

Glyphh is a semantic knowledge platform using Hyperdimensional Computing (HDC) to encode, store, and query concepts with deterministic, explainable results.

Traditional approaches fall short when AI needs to be **correct, not just plausible**:

| Approach | Limitation |
|----------|------------|
| **RAG** | Retrieves text chunks, not semantic meaning. No reasoning, just pattern matching. |
| **Knowledge Graphs** | Rigid schemas, expensive to maintain, brittle to change. |
| **Vector Databases** | Store embeddings but can't explain *why* results are similar. |
| **Structured Data** | Great for known queries, useless for semantic discovery. |

**Glyphh is different.** Using Hyperdimensional Computing, Glyphh encodes *meaning* into mathematical structures ("glyphs") that support:

- **Deterministic Results** - Same query, same answer. Every time. No hallucinations.
- **Explainable Similarity** - Know *why* concepts are related, with citations.
- **Temporal Reasoning** - Predict sequences and causality, not just similarity.
- **Composable Knowledge** - Combine concepts mathematically (A + B - C = ?).

### Core Capabilities

- **Semantic Encoding** - Transform concepts into high-dimensional vectors using HDC
- **Similarity Search** - Find related concepts with weighted, explainable scoring
- **Fact Trees** - Generate verification reports with citations to source data
- **Temporal Prediction** - Predict future states using beam search over temporal edges
- **Natural Language Queries** - Rules-first matching with optional LLM fallback

## Quick Start

### Installation

```bash
pip install glyphh
```

### Basic Usage

```python
from glyphh import GlyphhModel, Concept, EncoderConfig

# Create a model
config = EncoderConfig(dimension=10000, seed=42)
model = GlyphhModel(config)

# Encode concepts
concept = Concept(
    name="machine learning",
    attributes={"domain": "AI", "type": "technique"}
)
glyph = model.encode(concept)

# Find similar concepts
results = model.similarity_search("deep learning", top_k=5)
for result in results:
    print(f"{result.concept}: {result.score:.3f}")
```

## Documentation

- [Getting Started Guide](docs/getting-started.md)
- [SDK Reference](docs/sdk-reference.md)
- [Runtime Deployment](docs/runtime-deployment.md)
- [API Reference](docs/api-reference.md)
- [Examples](examples/)

## Architecture

### Local Development

Build and test models locally with the SDK:

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Notebook / Script                   │
│                                                             │
│   from glyphh import GlyphhModel, Concept                   │
│                                                             │
│   model = GlyphhModel(config)                               │
│   model.encode(Concept(...))                                │
│   model.similarity_search("query")                          │
│   model.export("my-model.glyphh")                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌────────────────┐
                    │ my-model.glyphh│
                    │ (Portable)     │
                    └────────────────┘
```

### Production: Agent + MCP Integration

Deploy to runtime and integrate with AI agents via MCP:

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent (Claude, GPT, etc.)             │
│                                                             │
│   User: "What's the return policy for enterprise customers?"│
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ MCP Protocol
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Glyphh Runtime                           │
│                                                             │
│   ┌─────────────┐  ┌─────────────┐  ┌──────────────┐        │
│   │ FAQ Model   │  │ Policy Model│  │ Product Model│        │
│   └─────────────┘  └─────────────┘  └──────────────┘        │
│                                                             │
│   MCP Tools:                                                │
│   • glyphh_query     - Semantic search                      │
│   • glyphh_verify    - Fact verification with citations     │
│   • glyphh_predict   - Temporal prediction                  │
│   • glyphh_explain   - Get reasoning chain                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│   Response to Agent:                                        │
│                                                             │
│   {                                                         │
│     "answer": "Enterprise customers have 60-day returns...",│
│     "confidence": 0.94,                                     │
│     "citation": {                                           │
│       "source": "Policy Manual v3.2, Section 4.1",          │
│       "approved_by": "Legal Team",                          │
│       "approved_date": "2025-01-15"                         │
│     },                                                      │
│     "match_method": "rules"                                 │
│   }                                                         │
└─────────────────────────────────────────────────────────────┘
```

The agent gets a deterministic answer with full citation—no hallucination possible.

## Components

### Glyphh SDK

Build models locally in Python:

```bash
pip install glyphh
```

- Define concepts and encode them using HDC
- Add intent patterns for NL query matching
- Build fact trees and temporal relationships
- Test everything locally before deployment
- Export as portable `.glyphh` files

### Glyphh Runtime

Serve models in production with full API access:

```bash
docker pull ghcr.io/glyphh/runtime:latest
```

- **REST API** - Standard HTTP endpoints for any client
- **MCP Server** - Native integration with AI agents (Claude, etc.)
- **WebSocket Listeners** - Real-time data ingestion
- **Multi-tenant** - Namespace isolation, auth, quotas

## Examples

### Building a Knowledge Base

```python
from glyphh import GlyphhModel, Concept, EncoderConfig

# Initialize model
config = EncoderConfig(dimension=10000, seed=42)
model = GlyphhModel(config)

# Add concepts
concepts = [
    Concept(name="Python", attributes={"type": "language", "paradigm": "multi"}),
    Concept(name="JavaScript", attributes={"type": "language", "paradigm": "multi"}),
    Concept(name="Rust", attributes={"type": "language", "paradigm": "systems"}),
]

for concept in concepts:
    model.encode(concept)

# Query
results = model.similarity_search("programming language", top_k=3)
```

### Deploying to Runtime

```bash
# Export model
glyphh export my-model.glyphh

# Deploy to runtime
curl -X POST http://localhost:8000/api/deploy \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @my-model.glyphh
```

### Natural Language Queries

The sidecar pattern in action—rules-first, LLM fallback:

```python
# Agent calls Glyphh via MCP or REST
response = requests.post(
    "http://localhost:8000/api/v1/my-namespace/query",
    json={"query": "what's the warranty on premium products?"}
)

result = response.json()

if result["match_method"] == "rules":
    # Glyphh answered deterministically
    print(f"Answer: {result['answer']}")
    print(f"Source: {result['citation']['source']}")
else:
    # Low confidence - agent should use LLM
    print("Glyphh unsure, falling back to LLM")
```

## Deployment Options

### Local Development (SDK Only)

```bash
# Install SDK
pip install glyphh

# Build and test models locally
python examples/basic_model.py
python examples/faq_verification.py
```

### Local Runtime (Docker)

```bash
# Start runtime with PostgreSQL
docker-compose up -d

# Deploy your model
curl -X POST http://localhost:8000/api/deploy \
  -H "Content-Type: application/octet-stream" \
  --data-binary @my-model.glyphh
```

Note: Local mode is limited to 1 model and 1,000 glyphs. See [Licensing](docs/licensing.md).

### Production (Self-Hosted or Cloud)

```bash
# Pull production image
docker pull ghcr.io/glyphh/runtime:latest

# Run with license
docker run -d \
  -e DEPLOYMENT_MODE=production \
  -e GLYPHH_LICENSE_KEY=$LICENSE_KEY \
  -e DATABASE_URL=$DATABASE_URL \
  ghcr.io/glyphh/runtime:latest
```

## License

Glyphh SDK is available under the [MIT License](LICENSE).

Glyphh Runtime requires a license for production use. See [Licensing](docs/licensing.md) for details.

## Support

- 📖 [Documentation](docs/)
- 💬 [Discussions](https://github.com/glyphh/glyphh-ai/discussions)
- 🐛 [Issue Tracker](https://github.com/glyphh/glyphh-ai/issues)
- 📧 [Contact](mailto:support@glyphh.com)

---

<p align="center">
  <strong>© 2026 Glyphh AI LLC. All rights reserved.</strong><br>
  Patent Pending - Appl. No. 63/969,729
</p>
