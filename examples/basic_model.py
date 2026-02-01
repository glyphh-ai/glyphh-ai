"""
Basic Glyphh Model Example

This example demonstrates:
1. Creating an encoder with explicit config structure
2. Encoding concepts into glyphs
3. Computing similarity between concepts
4. Packaging and exporting the model
"""

from glyphh import (
    Encoder, EncoderConfig, Concept, GlyphhModel,
    SimilarityCalculator, LayerConfig, SegmentConfig, Role
)

# Configure the encoder with explicit structure
config = EncoderConfig(
    dimension=10000,  # Vector dimension
    seed=42,          # For reproducibility
    layers=[
        LayerConfig(
            name="semantic",
            similarity_weight=1.0,
            segments=[
                SegmentConfig(
                    name="attributes",
                    roles=[
                        Role(name="domain", similarity_weight=0.8),
                        Role(name="type", similarity_weight=1.0),
                        Role(name="description", similarity_weight=0.6),
                    ]
                )
            ]
        )
    ]
)

# Create encoder
encoder = Encoder(config)
print(f"Encoder created: space_id={encoder.space_id}")

# Define concepts
concepts = [
    Concept(
        name="machine learning",
        attributes={
            "domain": "artificial intelligence",
            "type": "technique",
            "description": "Systems that learn from data"
        }
    ),
    Concept(
        name="neural network",
        attributes={
            "domain": "artificial intelligence",
            "type": "architecture",
            "description": "Computing systems inspired by biological brains"
        }
    ),
    Concept(
        name="deep learning",
        attributes={
            "domain": "artificial intelligence",
            "type": "technique",
            "description": "Neural networks with many layers"
        }
    ),
    Concept(
        name="reinforcement learning",
        attributes={
            "domain": "artificial intelligence",
            "type": "technique",
            "description": "Learning through rewards and penalties"
        }
    ),
    Concept(
        name="natural language processing",
        attributes={
            "domain": "artificial intelligence",
            "type": "application",
            "description": "Processing and understanding human language"
        }
    ),
]

# Encode concepts into glyphs
print("\nEncoding concepts...")
glyphs = []
for concept in concepts:
    glyph = encoder.encode(concept)
    glyphs.append(glyph)
    print(f"  ✓ Encoded: {concept.name}")

# Compute similarity between concepts
print("\nComputing similarities:")
calculator = SimilarityCalculator()

# Compare machine learning with other concepts
ml_glyph = glyphs[0]
for i, glyph in enumerate(glyphs[1:], 1):
    result = calculator.compute_similarity(
        ml_glyph, glyph, 
        edge_type="neural_cortex"
    )
    print(f"  machine learning vs {concepts[i].name}: {result.score:.3f}")

# Package the model for deployment
print("\nPackaging model...")
model = GlyphhModel(
    name="basic-model",
    version="1.0.0",
    encoder_config=config,
    glyphs=glyphs,
    metadata={
        "domain": "AI",
        "description": "Basic AI concepts model",
        "num_concepts": len(glyphs)
    }
)

# Export model
model.to_file("basic-model.glyphh")
print("  ✓ Model exported to basic-model.glyphh")

print("\nDone! You can now deploy this model to the runtime:")
print("  glyphh runtime deploy basic-model.glyphh")

# Cleanup
import os
if os.path.exists("basic-model.glyphh"):
    os.remove("basic-model.glyphh")
