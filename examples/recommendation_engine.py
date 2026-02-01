"""
Recommendation Engine Example

Recommend products based on user preferences and temporal patterns.

This example demonstrates:
1. Encoding user preferences
2. Finding similar products
3. Tracking preference changes over time
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
            name="preference",
            segments=[
                SegmentConfig(
                    name="attributes",
                    roles=[
                        Role(name="category", similarity_weight=1.0),
                        Role(name="style", similarity_weight=0.8),
                        Role(name="price_preference", similarity_weight=0.6),
                        Role(name="brand_affinity", similarity_weight=0.7),
                    ]
                )
            ]
        )
    ]
)

encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Recommendation Engine")
print("=" * 60)

# User preferences (from purchase history)
user_preferences = Concept(
    name="user_001_prefs",
    attributes={"category": "electronics", "style": "modern", "price_preference": "premium", "brand_affinity": "techco"}
)

# Product catalog
products = [
    Concept(name="smartwatch_pro", attributes={"category": "electronics", "style": "modern", "price_preference": "premium", "brand_affinity": "techco"}),
    Concept(name="tablet_basic", attributes={"category": "electronics", "style": "classic", "price_preference": "budget", "brand_affinity": "valueco"}),
    Concept(name="headphones_premium", attributes={"category": "electronics", "style": "modern", "price_preference": "premium", "brand_affinity": "audioco"}),
]

print("\nEncoding user preferences...")
user_glyph = encoder.encode(user_preferences)
print(f"  ✓ {user_preferences.name}")

print("\nEncoding products...")
product_glyphs = []
for product in products:
    glyph = encoder.encode(product)
    product_glyphs.append((product.name, glyph, product.attributes))
    print(f"  ✓ {product.name}")

# Generate recommendations
print("\nRecommendations for user_001:")
recommendations = []
for name, glyph, attrs in product_glyphs:
    result = calculator.compute_similarity(user_glyph, glyph, edge_type="neural_cortex")
    recommendations.append((name, result.score, attrs))

for name, score, attrs in sorted(recommendations, key=lambda x: -x[1]):
    print(f"  {name}: {score:.3f} ({attrs['style']}, {attrs['price_preference']})")

# Export
model = GlyphhModel(
    name="recommendations",
    version="1.0.0",
    encoder_config=config,
    glyphs=[user_glyph] + [g for _, g, _ in product_glyphs],
    metadata={"domain": "ecommerce"}
)
model.to_file("recommendations.glyphh")
print("\n✓ Model exported")

import os
os.remove("recommendations.glyphh")
