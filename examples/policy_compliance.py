"""
Policy Compliance Example

Check actions against policy rules using fact trees.

This example demonstrates:
1. Encoding policy rules with compliance criteria
2. Checking actions against policies
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
            name="policy",
            segments=[
                SegmentConfig(
                    name="rule",
                    roles=[
                        Role(name="policy_type", similarity_weight=1.0),
                        Role(name="action", similarity_weight=0.9),
                        Role(name="requirement", similarity_weight=0.8),
                        Role(name="department", similarity_weight=0.6),
                    ]
                )
            ]
        )
    ]
)

encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Policy Compliance Checker")
print("=" * 60)

# Policy rules
policies = [
    Concept(name="expense_policy", attributes={"policy_type": "expense", "action": "approve", "requirement": "receipt_required", "department": "finance"}),
    Concept(name="travel_policy", attributes={"policy_type": "travel", "action": "pre_approve", "requirement": "manager_approval", "department": "hr"}),
    Concept(name="data_policy", attributes={"policy_type": "data", "action": "encrypt", "requirement": "pii_protection", "department": "it"}),
]

print("\nEncoding policy rules...")
policy_glyphs = []
for policy in policies:
    glyph = encoder.encode(policy)
    policy_glyphs.append((policy.name, glyph, policy.attributes))
    print(f"  ✓ {policy.name}: {policy.attributes['requirement']}")

# Check an action
action = Concept(
    name="expense_submission",
    attributes={"policy_type": "expense", "action": "submit", "requirement": "receipt_required", "department": "finance"}
)

print(f"\nChecking action: {action.name}")
action_glyph = encoder.encode(action)

for name, policy_glyph, attrs in policy_glyphs:
    result = calculator.compute_similarity(action_glyph, policy_glyph, edge_type="neural_cortex")
    if result.score > 0.5:
        print(f"  ✓ Matches {name}: {attrs['requirement']} (score: {result.score:.3f})")

# Export
model = GlyphhModel(
    name="policy-compliance",
    version="1.0.0",
    encoder_config=config,
    glyphs=[g for _, g, _ in policy_glyphs],
    metadata={"domain": "compliance"}
)
model.to_file("policy-compliance.glyphh")
print("\n✓ Model exported")

import os
os.remove("policy-compliance.glyphh")
