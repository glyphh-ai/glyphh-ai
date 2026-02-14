<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="logo/glyphh-logo.png">
    <source media="(prefers-color-scheme: light)" srcset="logo/glyphh-logo-dark.png">
    <img src="logo/glyphh-logo-dark.png" alt="Glyphh Logo" width="250">
  </picture>
</p>

<h1 align="center">When your LLM can't afford to be wrong</h1>

<p align="center">
  <strong>Sidecar it with Glyphh AI.</strong>
</p>

<p align="center">
  Glyphh is the deterministic sidecar for your LLM + RAG stack.<br>
  When accuracy matters, get grounded answers with citations—not guesses.
</p>

---

## The Problem

When AI needs to be **correct**, not just plausible:

| Approach | Problem |
|----------|---------|
| 🤖 **LLMs** | Hallucinate |
| 📄 **RAG** | Still guesses |
| 🕸️ **Knowledge Graphs** | Rigid & brittle |
| 📊 **Vector DBs** | No reasoning |

## The Solution

**Glyphh AI: Neural-Semantic Artificial Intelligence**

Meaning encoded as math. Not embeddings. Not tokens. Pure mathematical structures that can be reasoned over.

| ✓ Deterministic | 📖 Explainable | 🔍 Auditable | 🧮 Composable |
|-----------------|----------------|--------------|---------------|
| Same question = same answer | Know why, with citations | Full approval trail | A + B - C = ? |

## The Sidecar Pattern

Your LLM handles ambiguity and generation. **Glyphh handles facts that can't be wrong.**

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent / LLM                           │
│                                                             │
│   User: "What's the return policy for enterprise customers?"│
│                                                             │
│                         │                                   │
│                         ▼                                   │
│            ┌────────────────────────┐                       │
│            │  Check Glyphh first    │                       │
│            │  (Rules-based match)   │                       │
│            └────────────────────────┘                       │
│                    │           │                            │
│            HIGH CONFIDENCE   LOW CONFIDENCE                 │
│                    │           │                            │
│                    ▼           ▼                            │
│         ┌──────────────┐  ┌──────────────┐                  │
│         │   Glyphh     │  │     LLM      │                  │
│         │ Deterministic│  │  Best effort │                  │
│         │              │  │              │                  │
│         │ ✓ Exact      │  │ ? May vary   │                  │
│         │ ✓ Cited      │  │ ? No citation│                  │
│         │ ✓ Auditable  │  │ ? No audit   │                  │
│         └──────────────┘  └──────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

**Grounded Response from Glyphh:**

```json
{
  "answer": "Enterprise customers have 60-day returns with full refund...",
  "confidence": 0.94,
  "match_method": "rules",
  "citation": {
    "source": "Policy v3.2 §4.1",
    "approved_by": "Legal Team",
    "approved_date": "2025-01-15"
  }
}
```

## Quick Start

### Installation

```bash
pip install glyphh
```

### Basic Usage

```python
from glyphh import (
    Encoder, EncoderConfig, Concept, 
    SimilarityCalculator, LayerConfig, SegmentConfig, Role
)

# Configure the encoder with explicit structure
config = EncoderConfig(
    dimension=10000,
    seed=42,
    layers=[
        LayerConfig(
            name="semantic",
            segments=[
                SegmentConfig(
                    name="attributes",
                    roles=[
                        Role(name="domain", similarity_weight=0.8),
                        Role(name="type", similarity_weight=1.0),
                    ]
                )
            ]
        )
    ]
)

# Create encoder and encode concepts
encoder = Encoder(config)

concept = Concept(
    name="machine learning",
    attributes={"domain": "AI", "type": "technique"}
)
glyph = encoder.encode(concept)

# Compute similarity between concepts
calculator = SimilarityCalculator()
result = calculator.compute(glyph1, glyph2)
print(f"Similarity: {result.score:.3f}")
```

## Getting Started

| Step | Action | Description |
|------|--------|-------------|
| 🛠️ **1** | Build or Browse | Create custom models with the SDK or grab pre-built ones from Studio |
| 🚀 **2** | Deploy in Minutes | One-click deploy to Glyphh Cloud or self-host with Docker |
| 🔌 **3** | Connect Your Agent | REST API or MCP—your AI agent queries Glyphh for grounded answers |

## Glyphh Studio

Pre-built models for common use cases. Customize or deploy as-is.

| Model | Use Case | Description |
|-------|----------|-------------|
| 💬 FAQ Verification | Support | Answers that can't be wrong. Citations included. |
| 📉 Churn Prediction | Customer Success | Temporal patterns that predict customer behavior. |
| ⚖️ Policy Compliance | Legal | HR, legal, and regulatory rules encoded as facts. |
| 🛒 Product Catalog | E-commerce | Semantic search over products with attributes. |
| 🏥 Medical Protocols | Healthcare | Clinical guidelines with audit trails. |
| 🏦 Financial Rules | Finance | Lending, insurance, and compliance logic. |

## Enterprise Ready

Run in the cloud or locally for air-gapped, on-prem, and data-sovereign use cases.

🏠 Self-hosted Option • 🏢 Multi-tenant • 🔑 API Keys • 📋 Audit Logs • 📁 Namespaces • 🐳 Docker Ready

## Deployment Options

### Local Development (SDK Only)

```bash
pip install glyphh
python examples/basic_model.py
```

### Local Runtime (Docker)

```bash
docker-compose up -d
curl -X POST http://localhost:8000/api/deploy \
  -H "Content-Type: application/octet-stream" \
  --data-binary @my-model.glyphh
```

Note: Local mode is limited to 1 model and 1,000 glyphs. See [Licensing](docs/licensing.md).

### Production (Self-Hosted or Cloud)

```bash
docker pull ghcr.io/glyphh/runtime:latest
docker run -d \
  -e DEPLOYMENT_MODE=production \
  -e GLYPHH_LICENSE_KEY=$LICENSE_KEY \
  -e DATABASE_URL=$DATABASE_URL \
  ghcr.io/glyphh/runtime:latest
```

## Pricing

**Free to build. Pay when you ship.**

| Development | Production |
|-------------|------------|
| **Free** forever | **$35** per runtime / month |
| Full SDK access | Everything in Development |
| Local runtime (Docker) | Unlimited models |
| 1 model, 1,000 glyphs limit | Unlimited glyphs |
| All SDK features | Production license key |
| Community support | Priority support |

Need enterprise features, custom SLAs, or on-premise deployment? [Contact sales →](mailto:support@glyphh.ai)

## Documentation

- [Getting Started Guide](docs/getting-started.md)
- [SDK Reference](docs/sdk-reference.md)
- [Runtime Deployment](docs/runtime-deployment.md)
- [API Reference](docs/api-reference.md)
- [Examples](examples/)

## License

Glyphh is available under the [Glyphh AI Community License](LICENSE).

- ✓ Free to download and use for development
- ✓ Free tier available for production (1 model, 1,000 glyphs)
- ✓ Source code viewable for learning
- ✗ Not open source — cannot redistribute or build competing products

Production use beyond the free tier requires a license. See [Licensing](docs/licensing.md) for details.

## Support

- 📖 [Documentation](docs/)
- 💬 [Discussions](https://github.com/glyphh-ai/glyphh-ai/discussions)
- 🐛 [Issue Tracker](https://github.com/glyphh-ai/glyphh-ai/issues)
- 📧 [Contact](mailto:support@glyphh.ai)

---

<p align="center">
  <strong>© 2026 Glyphh AI LLC. All rights reserved.</strong><br>
  Patent Pending - Appl. No. 63/969,729
</p>
