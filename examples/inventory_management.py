"""
Inventory Management Example

Track inventory with state transitions using temporal patterns.

This example demonstrates:
1. Encoding inventory items with state attributes
2. Tracking state transitions over time
3. Predicting inventory needs
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
            name="inventory",
            segments=[
                SegmentConfig(
                    name="item",
                    roles=[
                        Role(name="category", similarity_weight=0.8),
                        Role(name="stock_level", similarity_weight=1.0),
                        Role(name="reorder_status", similarity_weight=0.9),
                        Role(name="location", similarity_weight=0.6),
                    ]
                )
            ]
        )
    ]
)

encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Inventory Management")
print("=" * 60)

# Inventory items
items = [
    Concept(name="widget_a", attributes={"category": "electronics", "stock_level": "low", "reorder_status": "needed", "location": "warehouse_1"}),
    Concept(name="widget_b", attributes={"category": "electronics", "stock_level": "high", "reorder_status": "ok", "location": "warehouse_1"}),
    Concept(name="gadget_a", attributes={"category": "accessories", "stock_level": "medium", "reorder_status": "ok", "location": "warehouse_2"}),
]

print("\nEncoding inventory items...")
glyphs = []
for item in items:
    glyph = encoder.encode(item)
    glyphs.append(glyph)
    print(f"  ✓ {item.name}: {item.attributes['stock_level']} stock")

# Find items needing reorder
print("\nItems needing reorder:")
reorder_pattern = Concept(name="reorder_needed", attributes={"category": "any", "stock_level": "low", "reorder_status": "needed", "location": "any"})
reorder_glyph = encoder.encode(reorder_pattern)

for i, glyph in enumerate(glyphs):
    result = calculator.compute_similarity(reorder_glyph, glyph, edge_type="neural_cortex")
    if result.score > 0.5:
        print(f"  ⚠️  {items[i].name}: similarity {result.score:.3f}")

# Export
model = GlyphhModel(
    name="inventory-model",
    version="1.0.0",
    encoder_config=config,
    glyphs=glyphs,
    metadata={"domain": "logistics"}
)
model.to_file("inventory-model.glyphh")
print("\n✓ Model exported")

import os
os.remove("inventory-model.glyphh")
