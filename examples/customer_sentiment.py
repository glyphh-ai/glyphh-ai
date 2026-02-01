"""
Customer Sentiment Analysis Example

Analyze customer sentiment using similarity to known sentiment patterns.

This example demonstrates:
1. Encoding customer feedback with sentiment-relevant attributes
2. Computing similarity to sentiment patterns
3. Temporal tracking of sentiment changes
"""

from glyphh import (
    Encoder, EncoderConfig, Concept, GlyphhModel,
    SimilarityCalculator, LayerConfig, SegmentConfig, Role
)

config = EncoderConfig(
    dimension=10000,
    seed=42,
    layers=[
        LayerConfig(
            name="feedback",
            segments=[
                SegmentConfig(
                    name="content",
                    roles=[
                        Role(name="topic", similarity_weight=0.8),
                        Role(name="tone", similarity_weight=1.0),
                        Role(name="urgency", similarity_weight=0.7),
                        Role(name="channel", similarity_weight=0.5),
                    ]
                )
            ]
        )
    ]
)

encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Customer Sentiment Analysis")
print("=" * 60)

# Sentiment patterns
patterns = [
    Concept(name="positive", attributes={"topic": "product", "tone": "positive", "urgency": "low", "channel": "survey"}),
    Concept(name="negative", attributes={"topic": "support", "tone": "negative", "urgency": "high", "channel": "email"}),
    Concept(name="neutral", attributes={"topic": "billing", "tone": "neutral", "urgency": "medium", "channel": "chat"}),
]

print("\nEncoding sentiment patterns...")
pattern_glyphs = []
for p in patterns:
    glyph = encoder.encode(p)
    pattern_glyphs.append((p.name, glyph))
    print(f"  ✓ {p.name}")

# Test feedback
test_feedback = Concept(
    name="feedback_001",
    attributes={"topic": "support", "tone": "negative", "urgency": "high", "channel": "email"}
)

print(f"\nAnalyzing: {test_feedback.name}")
feedback_glyph = encoder.encode(test_feedback)

for name, pattern_glyph in pattern_glyphs:
    result = calculator.compute_similarity(feedback_glyph, pattern_glyph, edge_type="neural_cortex")
    print(f"  {name}: {result.score:.3f}")

# Export
glyphs = [g for _, g in pattern_glyphs]
model = GlyphhModel(
    name="sentiment-model",
    version="1.0.0",
    encoder_config=config,
    glyphs=glyphs,
    metadata={"domain": "customer_support"}
)
model.to_file("sentiment-model.glyphh")
print("\n✓ Model exported")

import os
os.remove("sentiment-model.glyphh")
