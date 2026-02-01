"""
Patient Triage Example

Triage patients using symptom matching and intent patterns.

This example demonstrates:
1. Encoding symptom patterns with urgency levels
2. Matching patient symptoms to triage categories
3. Providing explainable triage decisions
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
            name="triage",
            segments=[
                SegmentConfig(
                    name="symptoms",
                    roles=[
                        Role(name="primary_symptom", similarity_weight=1.0),
                        Role(name="severity", similarity_weight=0.9),
                        Role(name="duration", similarity_weight=0.7),
                        Role(name="vital_signs", similarity_weight=0.8),
                    ]
                )
            ]
        )
    ]
)

encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Patient Triage System")
print("=" * 60)

# Triage categories
categories = [
    Concept(name="emergent", attributes={"primary_symptom": "chest_pain", "severity": "severe", "duration": "acute", "vital_signs": "abnormal"}),
    Concept(name="urgent", attributes={"primary_symptom": "abdominal_pain", "severity": "moderate", "duration": "hours", "vital_signs": "stable"}),
    Concept(name="non_urgent", attributes={"primary_symptom": "cold_symptoms", "severity": "mild", "duration": "days", "vital_signs": "normal"}),
]

print("\nEncoding triage categories...")
category_glyphs = []
for cat in categories:
    glyph = encoder.encode(cat)
    category_glyphs.append((cat.name, glyph))
    print(f"  ✓ {cat.name}: {cat.attributes['primary_symptom']}")

# Triage a patient
patient = Concept(
    name="patient_001",
    attributes={"primary_symptom": "chest_pain", "severity": "severe", "duration": "acute", "vital_signs": "abnormal"}
)

print(f"\nTriaging: {patient.name}")
patient_glyph = encoder.encode(patient)

best_category = None
best_score = 0
for name, cat_glyph in category_glyphs:
    result = calculator.compute_similarity(patient_glyph, cat_glyph, edge_type="neural_cortex")
    print(f"  {name}: {result.score:.3f}")
    if result.score > best_score:
        best_score = result.score
        best_category = name

print(f"\n⚠️  TRIAGE RESULT: {best_category.upper()} (confidence: {best_score:.3f})")

# Export
model = GlyphhModel(
    name="triage-model",
    version="1.0.0",
    encoder_config=config,
    glyphs=[g for _, g in category_glyphs],
    metadata={"domain": "healthcare"}
)
model.to_file("triage-model.glyphh")
print("\n✓ Model exported")

import os
os.remove("triage-model.glyphh")
