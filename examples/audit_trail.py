"""
Audit Trail Example

Track and verify audit events using temporal edges.

This example demonstrates:
1. Encoding audit events with approval metadata
2. Creating temporal edges between events
3. Verifying audit trail integrity
"""

from glyphh import (
    Encoder, EncoderConfig, Concept, GlyphhModel,
    SimilarityCalculator, TemporalEncoder,
    LayerConfig, SegmentConfig, Role
)

config = EncoderConfig(
    dimension=10000,
    seed=42,
    layers=[
        LayerConfig(
            name="audit",
            segments=[
                SegmentConfig(
                    name="event",
                    roles=[
                        Role(name="action", similarity_weight=1.0),
                        Role(name="resource", similarity_weight=0.9),
                        Role(name="actor", similarity_weight=0.8),
                        Role(name="status", similarity_weight=0.7),
                    ]
                )
            ]
        )
    ]
)

encoder = Encoder(config)
temporal = TemporalEncoder()

print("Audit Trail Management")
print("=" * 60)

# Audit events
events = [
    Concept(name="event_001", attributes={"action": "create", "resource": "document", "actor": "user_a", "status": "pending"}),
    Concept(name="event_002", attributes={"action": "review", "resource": "document", "actor": "user_b", "status": "reviewed"}),
    Concept(name="event_003", attributes={"action": "approve", "resource": "document", "actor": "user_c", "status": "approved"}),
]

print("\nEncoding audit events...")
glyphs = []
for event in events:
    glyph = encoder.encode(event)
    glyphs.append(glyph)
    print(f"  ✓ {event.name}: {event.attributes['action']} by {event.attributes['actor']}")

# Create temporal edges
print("\nCreating temporal edges...")
for i in range(len(glyphs) - 1):
    delta = temporal.compute_temporal_delta(glyphs[i].global_cortex, glyphs[i+1].global_cortex)
    print(f"  ✓ {events[i].name} → {events[i+1].name}")

# Export
model = GlyphhModel(
    name="audit-model",
    version="1.0.0",
    encoder_config=config,
    glyphs=glyphs,
    metadata={"domain": "compliance"}
)
model.to_file("audit-model.glyphh")
print("\n✓ Model exported")

import os
os.remove("audit-model.glyphh")
