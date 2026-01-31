"""
Intent Pattern Example

This example demonstrates:
1. Creating an IntentEncoder
2. Adding default and custom patterns
3. Matching natural language queries
4. Integrating with a model
"""

from glyphh import GlyphhModel, Concept, EncoderConfig
from glyphh import IntentEncoder, IntentPattern

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create intent encoder
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
    "predict what comes after data preprocessing",
    "how many concepts are there",
]

for query in test_queries:
    match = intent_encoder.match_intent(query)
    confidence_indicator = "✓" if match.is_high_confidence() else "?"
    print(f"  {confidence_indicator} '{query}'")
    print(f"      → {match.intent_type} (confidence: {match.confidence:.2f})")

# Create model with intent encoder
print("\nCreating model with intent encoder...")
model = GlyphhModel(config)
model.intent_encoder = intent_encoder

# Add some concepts
concepts = [
    Concept(name="machine learning", attributes={"type": "technique"}),
    Concept(name="neural network", attributes={"type": "architecture"}),
    Concept(name="image recognition", attributes={"type": "application"}),
]

for concept in concepts:
    model.encode(concept)

# Export model (includes intent patterns)
model.export("model-with-intents.glyphh")
print("  ✓ Model exported with intent patterns")

print("\nWhen deployed, the runtime will use these patterns for NL queries:")
print("  POST /api/v1/my-model/query")
print('  {"query": "find similar to machine learning"}')
print("  → Returns match_method: 'rules' with high confidence")
