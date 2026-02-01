"""
Medical Protocols Example

Lookup medical protocols with citations and evidence levels.

This example demonstrates:
1. Encoding medical protocols with evidence metadata
2. Finding relevant protocols for symptoms
3. Providing citations for audit trails
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
            name="protocol",
            segments=[
                SegmentConfig(
                    name="content",
                    roles=[
                        Role(name="condition", similarity_weight=1.0),
                        Role(name="treatment", similarity_weight=0.9),
                        Role(name="evidence_level", similarity_weight=0.8),
                        Role(name="specialty", similarity_weight=0.6),
                    ]
                )
            ]
        )
    ]
)

encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Medical Protocol Lookup")
print("=" * 60)

# Medical protocols
protocols = [
    Concept(
        name="hypertension_protocol",
        attributes={
            "condition": "hypertension",
            "treatment": "ace_inhibitor",
            "evidence_level": "A",
            "specialty": "cardiology",
            "source": "ACC/AHA Guidelines 2024",
        }
    ),
    Concept(
        name="diabetes_protocol",
        attributes={
            "condition": "diabetes_type2",
            "treatment": "metformin",
            "evidence_level": "A",
            "specialty": "endocrinology",
            "source": "ADA Standards 2024",
        }
    ),
    Concept(
        name="chest_pain_protocol",
        attributes={
            "condition": "chest_pain",
            "treatment": "ecg_troponin",
            "evidence_level": "A",
            "specialty": "emergency",
            "source": "ACEP Guidelines 2024",
        }
    ),
]

print("\nEncoding medical protocols...")
glyphs = []
protocol_data = {}
for protocol in protocols:
    glyph = encoder.encode(protocol)
    glyphs.append(glyph)
    protocol_data[protocol.name] = protocol.attributes
    print(f"  ✓ {protocol.name}: {protocol.attributes['condition']}")

# Query for a condition
print("\nLooking up protocol for 'high blood pressure':")
query = Concept(name="query", attributes={"condition": "hypertension", "treatment": "", "evidence_level": "", "specialty": "cardiology"})
query_glyph = encoder.encode(query)

best_match = None
best_score = 0
for i, glyph in enumerate(glyphs):
    result = calculator.compute_similarity(query_glyph, glyph, edge_type="neural_cortex")
    if result.score > best_score:
        best_score = result.score
        best_match = protocols[i]

if best_match:
    attrs = best_match.attributes
    print(f"\n✓ Found: {best_match.name} (confidence: {best_score:.3f})")
    print(f"  Treatment: {attrs['treatment']}")
    print(f"  Evidence Level: {attrs['evidence_level']}")
    print(f"  Citation: {attrs['source']}")

# Export
model = GlyphhModel(
    name="medical-protocols",
    version="1.0.0",
    encoder_config=config,
    glyphs=glyphs,
    metadata={"domain": "healthcare"}
)
model.to_file("medical-protocols.glyphh")
print("\n✓ Model exported")

import os
os.remove("medical-protocols.glyphh")
