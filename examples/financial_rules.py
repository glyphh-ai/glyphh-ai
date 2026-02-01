"""
Financial Rules Example

Implement financial compliance rules using fact trees.

This example demonstrates:
1. Encoding financial rules with compliance attributes
2. Checking transactions against rules
3. Building audit trails with citations
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
            name="rule",
            segments=[
                SegmentConfig(
                    name="criteria",
                    roles=[
                        Role(name="rule_type", similarity_weight=1.0),
                        Role(name="threshold", similarity_weight=0.9),
                        Role(name="action", similarity_weight=0.8),
                        Role(name="jurisdiction", similarity_weight=0.7),
                    ]
                )
            ]
        )
    ]
)

encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Financial Rules Engine")
print("=" * 60)

# Compliance rules
rules = [
    Concept(name="aml_reporting", attributes={"rule_type": "aml", "threshold": "10000", "action": "report", "jurisdiction": "us"}),
    Concept(name="kyc_verification", attributes={"rule_type": "kyc", "threshold": "5000", "action": "verify", "jurisdiction": "us"}),
    Concept(name="wire_approval", attributes={"rule_type": "wire", "threshold": "25000", "action": "approve", "jurisdiction": "international"}),
]

print("\nEncoding compliance rules...")
rule_glyphs = []
for rule in rules:
    glyph = encoder.encode(rule)
    rule_glyphs.append((rule.name, glyph))
    print(f"  ✓ {rule.name}: {rule.attributes['action']} for {rule.attributes['rule_type']}")

# Test transaction
transaction = Concept(
    name="wire_transfer_001",
    attributes={"rule_type": "wire", "threshold": "50000", "action": "approve", "jurisdiction": "international"}
)

print(f"\nChecking transaction: {transaction.name}")
tx_glyph = encoder.encode(transaction)

for name, rule_glyph in rule_glyphs:
    result = calculator.compute_similarity(tx_glyph, rule_glyph, edge_type="neural_cortex")
    print(f"  {name}: {result.score:.3f}")

# Export
model = GlyphhModel(
    name="financial-rules",
    version="1.0.0",
    encoder_config=config,
    glyphs=[g for _, g in rule_glyphs],
    metadata={"domain": "finance"}
)
model.to_file("financial-rules.glyphh")
print("\n✓ Model exported")

import os
os.remove("financial-rules.glyphh")
