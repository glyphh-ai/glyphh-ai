"""
Basic Glyphh Model Example

This example demonstrates:
1. Creating a model with EncoderConfig
2. Encoding concepts
3. Running similarity search
4. Exporting the model
"""

from glyphh import GlyphhModel, Concept, EncoderConfig

# Configure the encoder
config = EncoderConfig(
    dimension=10000,  # Vector dimension
    seed=42,          # For reproducibility
)

# Create model
model = GlyphhModel(config)

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

# Encode concepts
print("Encoding concepts...")
for concept in concepts:
    glyph = model.encode(concept)
    print(f"  ✓ Encoded: {concept.name}")

# Test similarity search
print("\nSimilarity search for 'AI techniques':")
results = model.similarity_search("AI techniques", top_k=3)
for i, result in enumerate(results, 1):
    print(f"  {i}. {result.concept}: {result.score:.3f}")

# Test another query
print("\nSimilarity search for 'learning from data':")
results = model.similarity_search("learning from data", top_k=3)
for i, result in enumerate(results, 1):
    print(f"  {i}. {result.concept}: {result.score:.3f}")

# Export model
print("\nExporting model...")
model.export("basic-model.glyphh")
print("  ✓ Model exported to basic-model.glyphh")

print("\nDone! You can now deploy this model to the runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @basic-model.glyphh")
