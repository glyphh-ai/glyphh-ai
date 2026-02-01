"""
Fraud Detection Example

Detect fraudulent transactions using temporal pattern recognition.

This example demonstrates:
1. Encoding transaction concepts with fraud-relevant attributes
2. Using temporal patterns to detect anomalies
3. Computing similarity to known fraud patterns
4. Building explainable fraud scores with fact trees

Use Cases:
- Credit card fraud detection
- Account takeover detection
- Money laundering detection
- Insurance fraud detection
"""

from glyphh import (
    Encoder, EncoderConfig, Concept, GlyphhModel,
    SimilarityCalculator, LayerConfig, SegmentConfig, Role
)

# Configure encoder with fraud-detection structure
config = EncoderConfig(
    dimension=10000,
    seed=42,
    layers=[
        LayerConfig(
            name="transaction",
            similarity_weight=1.0,
            segments=[
                SegmentConfig(
                    name="details",
                    roles=[
                        Role(name="amount_category", similarity_weight=0.8),
                        Role(name="merchant_category", similarity_weight=0.9),
                        Role(name="location", similarity_weight=0.7),
                        Role(name="time_of_day", similarity_weight=0.6),
                    ]
                )
            ]
        ),
        LayerConfig(
            name="behavior",
            similarity_weight=0.8,
            segments=[
                SegmentConfig(
                    name="patterns",
                    roles=[
                        Role(name="velocity", similarity_weight=1.0),
                        Role(name="device_fingerprint", similarity_weight=0.9),
                        Role(name="geo_anomaly", similarity_weight=1.0),
                    ]
                )
            ]
        )
    ]
)

# Create encoder and calculator
encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Fraud Detection Model")
print("=" * 60)

# =============================================================================
# Define Known Fraud Patterns
# =============================================================================

fraud_patterns = [
    Concept(
        name="card_testing",
        attributes={
            "amount_category": "micro",  # Small test amounts
            "merchant_category": "online_retail",
            "location": "foreign",
            "time_of_day": "night",
            "velocity": "high",  # Many transactions quickly
            "device_fingerprint": "new",
            "geo_anomaly": "yes",
            "fraud_type": "card_testing",
        }
    ),
    Concept(
        name="account_takeover",
        attributes={
            "amount_category": "large",
            "merchant_category": "electronics",
            "location": "foreign",
            "time_of_day": "any",
            "velocity": "medium",
            "device_fingerprint": "new",
            "geo_anomaly": "yes",
            "fraud_type": "account_takeover",
        }
    ),
    Concept(
        name="friendly_fraud",
        attributes={
            "amount_category": "medium",
            "merchant_category": "digital_goods",
            "location": "domestic",
            "time_of_day": "any",
            "velocity": "low",
            "device_fingerprint": "known",
            "geo_anomaly": "no",
            "fraud_type": "friendly_fraud",
        }
    ),
]

# Encode fraud patterns
print("\nEncoding known fraud patterns...")
fraud_glyphs = []
for pattern in fraud_patterns:
    glyph = encoder.encode(pattern)
    fraud_glyphs.append(glyph)
    print(f"  ✓ {pattern.name}")

# =============================================================================
# Define Legitimate Transaction Patterns
# =============================================================================

legitimate_patterns = [
    Concept(
        name="normal_purchase",
        attributes={
            "amount_category": "medium",
            "merchant_category": "grocery",
            "location": "domestic",
            "time_of_day": "day",
            "velocity": "low",
            "device_fingerprint": "known",
            "geo_anomaly": "no",
        }
    ),
    Concept(
        name="travel_purchase",
        attributes={
            "amount_category": "large",
            "merchant_category": "travel",
            "location": "foreign",
            "time_of_day": "day",
            "velocity": "low",
            "device_fingerprint": "known",
            "geo_anomaly": "no",  # Pre-notified travel
        }
    ),
]

print("\nEncoding legitimate patterns...")
legit_glyphs = []
for pattern in legitimate_patterns:
    glyph = encoder.encode(pattern)
    legit_glyphs.append(glyph)
    print(f"  ✓ {pattern.name}")

# =============================================================================
# Fraud Detection Function
# =============================================================================

def detect_fraud(transaction: Concept, threshold: float = 0.4):
    """Detect if a transaction matches known fraud patterns."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {transaction.name}")
    print('='*60)
    
    tx_glyph = encoder.encode(transaction)
    
    # Check similarity to fraud patterns
    fraud_scores = []
    for i, fraud_glyph in enumerate(fraud_glyphs):
        result = calculator.compute_similarity(
            tx_glyph, fraud_glyph,
            edge_type="neural_cortex"
        )
        fraud_scores.append((fraud_patterns[i].name, result.score))
    
    # Check similarity to legitimate patterns
    legit_scores = []
    for i, legit_glyph in enumerate(legit_glyphs):
        result = calculator.compute_similarity(
            tx_glyph, legit_glyph,
            edge_type="neural_cortex"
        )
        legit_scores.append((legitimate_patterns[i].name, result.score))
    
    # Find best matches
    best_fraud = max(fraud_scores, key=lambda x: x[1])
    best_legit = max(legit_scores, key=lambda x: x[1])
    
    # Compute fraud risk
    fraud_risk = best_fraud[1] / (best_fraud[1] + best_legit[1] + 0.001)
    
    print(f"\nFraud Pattern Matches:")
    for name, score in sorted(fraud_scores, key=lambda x: -x[1]):
        print(f"  {name}: {score:.3f}")
    
    print(f"\nLegitimate Pattern Matches:")
    for name, score in sorted(legit_scores, key=lambda x: -x[1]):
        print(f"  {name}: {score:.3f}")
    
    print(f"\nFraud Risk Score: {fraud_risk:.2f}")
    
    if fraud_risk > threshold:
        print(f"⚠️  HIGH RISK - Matches '{best_fraud[0]}' pattern")
        return {"risk": "high", "score": fraud_risk, "pattern": best_fraud[0]}
    else:
        print(f"✓ LOW RISK - Matches '{best_legit[0]}' pattern")
        return {"risk": "low", "score": fraud_risk, "pattern": best_legit[0]}

# =============================================================================
# Test Fraud Detection
# =============================================================================

print("\n" + "="*60)
print("TESTING FRAUD DETECTION")
print("="*60)

test_transactions = [
    # Suspicious - matches card testing pattern
    Concept(
        name="suspicious_tx_001",
        attributes={
            "amount_category": "micro",
            "merchant_category": "online_retail",
            "location": "foreign",
            "time_of_day": "night",
            "velocity": "high",
            "device_fingerprint": "new",
            "geo_anomaly": "yes",
        }
    ),
    # Normal - matches legitimate pattern
    Concept(
        name="normal_tx_001",
        attributes={
            "amount_category": "medium",
            "merchant_category": "grocery",
            "location": "domestic",
            "time_of_day": "day",
            "velocity": "low",
            "device_fingerprint": "known",
            "geo_anomaly": "no",
        }
    ),
]

for tx in test_transactions:
    detect_fraud(tx)

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

all_glyphs = fraud_glyphs + legit_glyphs
model = GlyphhModel(
    name="fraud-detection",
    version="1.0.0",
    encoder_config=config,
    glyphs=all_glyphs,
    metadata={
        "domain": "finance",
        "description": "Fraud detection using pattern matching",
    }
)

model.to_file("fraud-detection.glyphh")
print("✓ Model exported to fraud-detection.glyphh")

# Cleanup
import os
if os.path.exists("fraud-detection.glyphh"):
    os.remove("fraud-detection.glyphh")
