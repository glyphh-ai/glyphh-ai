"""
Drug Interactions Example

Check drug interactions using fact tree relationships.

This example demonstrates:
1. Encoding drug concepts with interaction attributes
2. Computing similarity to find potential interactions
3. Building fact trees for explainable results
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
            name="drug",
            segments=[
                SegmentConfig(
                    name="properties",
                    roles=[
                        Role(name="drug_class", similarity_weight=1.0),
                        Role(name="mechanism", similarity_weight=0.9),
                        Role(name="metabolism", similarity_weight=0.8),
                        Role(name="contraindications", similarity_weight=1.0),
                    ]
                )
            ]
        )
    ]
)

encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Drug Interaction Checker")
print("=" * 60)

# Drug database
drugs = [
    Concept(name="warfarin", attributes={"drug_class": "anticoagulant", "mechanism": "vitamin_k_inhibitor", "metabolism": "cyp2c9", "contraindications": "bleeding_risk"}),
    Concept(name="aspirin", attributes={"drug_class": "nsaid", "mechanism": "cox_inhibitor", "metabolism": "hepatic", "contraindications": "bleeding_risk"}),
    Concept(name="metformin", attributes={"drug_class": "antidiabetic", "mechanism": "glucose_regulation", "metabolism": "renal", "contraindications": "kidney_disease"}),
    Concept(name="lisinopril", attributes={"drug_class": "ace_inhibitor", "mechanism": "ace_inhibition", "metabolism": "renal", "contraindications": "kidney_disease"}),
]

print("\nEncoding drug database...")
glyphs = []
for drug in drugs:
    glyph = encoder.encode(drug)
    glyphs.append((drug.name, glyph, drug.attributes))
    print(f"  ✓ {drug.name} ({drug.attributes['drug_class']})")

# Check interactions
print("\nChecking interactions (warfarin + aspirin):")
warfarin_glyph = glyphs[0][1]
aspirin_glyph = glyphs[1][1]

result = calculator.compute_similarity(warfarin_glyph, aspirin_glyph, edge_type="neural_cortex")
print(f"  Similarity: {result.score:.3f}")
print(f"  ⚠️  Both have bleeding_risk contraindication - INTERACTION DETECTED")

# Export
model = GlyphhModel(
    name="drug-interactions",
    version="1.0.0",
    encoder_config=config,
    glyphs=[g for _, g, _ in glyphs],
    metadata={"domain": "healthcare"}
)
model.to_file("drug-interactions.glyphh")
print("\n✓ Model exported")

import os
os.remove("drug-interactions.glyphh")
