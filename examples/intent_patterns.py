"""
Intent Pattern Example

This example demonstrates:
1. Creating an IntentEncoder for natural language query matching
2. Adding default and custom intent patterns
3. Matching user queries to intents
4. Integrating intent matching with a model
"""

from glyphh import (
    Encoder, EncoderConfig, Concept, GlyphhModel,
    IntentEncoder, IntentPattern, DEFAULT_INTENT_PATTERNS,
    LayerConfig, SegmentConfig, Role
)

# Configure encoder
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
                        Role(name="type"),
                        Role(name="domain"),
                    ]
                )
            ]
        )
    ]
)

# Create encoder
encoder = Encoder(config)

# Create intent encoder (takes config, not encoder)
intent_encoder = IntentEncoder(config)

# Add default patterns for common operations
intent_encoder.add_defaults()
print("Default patterns loaded:")
for pattern in intent_encoder.get_patterns():
    print(f"  - {pattern.intent_type}: {len(pattern.example_phrases)} phrases")

# Add custom domain-specific patterns
print("\nAdding custom patterns...")

intent_encoder.add_pattern(IntentPattern(
    intent_type="find_technique",
    example_phrases=[
        "find technique for",
        "what technique does",
        "show me techniques",
        "technique to",
    ],
    query_template={
        "operation": "similarity_search",
        "filters": {"type": "technique"},
        "top_k": 5
    }
))
print("  ✓ Added: find_technique")

intent_encoder.add_pattern(IntentPattern(
    intent_type="explain_concept",
    example_phrases=[
        "explain",
        "what is",
        "describe",
        "tell me about",
    ],
    query_template={
        "operation": "fact_tree",
        "max_depth": 2
    }
))
print("  ✓ Added: explain_concept")

# Test intent matching
print("\nTesting intent matching:")

test_queries = [
    "find similar to machine learning",
    "what technique does image recognition use",
    "explain neural networks",
    "compare deep learning and machine learning",
]

for query in test_queries:
    match = intent_encoder.match_intent(query)
    confidence_indicator = "✓" if match.confidence > 0.5 else "?"
    print(f"  {confidence_indicator} '{query}'")
    print(f"      → {match.intent_type} (confidence: {match.confidence:.2f})")

# Create and encode some concepts
print("\nEncoding concepts...")
concepts = [
    Concept(name="machine learning", attributes={"type": "technique", "domain": "AI"}),
    Concept(name="neural network", attributes={"type": "architecture", "domain": "AI"}),
    Concept(name="image recognition", attributes={"type": "application", "domain": "AI"}),
]

glyphs = []
for concept in concepts:
    glyph = encoder.encode(concept)
    glyphs.append(glyph)
    print(f"  ✓ Encoded: {concept.name}")

# Package model with intent patterns
print("\nPackaging model with intent patterns...")
model = GlyphhModel(
    name="model-with-intents",
    version="1.0.0",
    encoder_config=config,
    glyphs=glyphs,
    intent_patterns=intent_encoder.to_dict(),
    metadata={"domain": "AI", "description": "Model with intent patterns"}
)

model.to_file("model-with-intents.glyphh")
print("  ✓ Model exported with intent patterns")

print("\nWhen deployed, the runtime will use these patterns for NL queries:")
print("  POST /api/v1/model-with-intents/query")
print('  {"query": "find similar to machine learning"}')
print("  → Returns match_method: 'rules' with high confidence")

# Cleanup
import os
if os.path.exists("model-with-intents.glyphh"):
    os.remove("model-with-intents.glyphh")
