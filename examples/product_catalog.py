"""
Product Catalog Example

Search products using similarity and intent matching.

This example demonstrates:
1. Encoding products with searchable attributes
2. Semantic product search
3. Finding similar products
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
            name="product",
            segments=[
                SegmentConfig(
                    name="attributes",
                    roles=[
                        Role(name="category", similarity_weight=0.9),
                        Role(name="brand", similarity_weight=0.7),
                        Role(name="color", similarity_weight=0.6),
                        Role(name="price_range", similarity_weight=0.5),
                    ]
                )
            ]
        )
    ]
)

encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Product Catalog Search")
print("=" * 60)

# Product catalog
products = [
    Concept(name="laptop_pro", attributes={"category": "electronics", "brand": "techco", "color": "silver", "price_range": "premium"}),
    Concept(name="laptop_basic", attributes={"category": "electronics", "brand": "techco", "color": "black", "price_range": "budget"}),
    Concept(name="headphones_wireless", attributes={"category": "electronics", "brand": "audioco", "color": "black", "price_range": "mid"}),
    Concept(name="backpack_travel", attributes={"category": "accessories", "brand": "travelco", "color": "blue", "price_range": "mid"}),
]

print("\nEncoding product catalog...")
glyphs = []
for product in products:
    glyph = encoder.encode(product)
    glyphs.append((product.name, glyph, product.attributes))
    print(f"  ✓ {product.name}: {product.attributes['category']}")

# Search for products
query = Concept(name="search", attributes={"category": "electronics", "brand": "", "color": "black", "price_range": ""})
query_glyph = encoder.encode(query)

print("\nSearching for 'black electronics':")
results = []
for name, glyph, attrs in glyphs:
    result = calculator.compute_similarity(query_glyph, glyph, edge_type="neural_cortex")
    results.append((name, result.score, attrs))

for name, score, attrs in sorted(results, key=lambda x: -x[1])[:3]:
    print(f"  {name}: {score:.3f} ({attrs['category']}, {attrs['color']})")

# Export
model = GlyphhModel(
    name="product-catalog",
    version="1.0.0",
    encoder_config=config,
    glyphs=[g for _, g, _ in glyphs],
    metadata={"domain": "ecommerce"}
)
model.to_file("product-catalog.glyphh")
print("\n✓ Model exported")

import os
os.remove("product-catalog.glyphh")
