"""
Churn Prediction Example

Predict customer churn using pattern recognition - no hardcoded sentiment rules.
Let the model discover patterns from historical data.

Key Principle: Don't hardwire sentiment - let the model learn from:
- Spend patterns (increasing, decreasing, stable)
- Usage/adoption metrics (feature adoption, login frequency)
- Support interactions (case count, resolution time)
- Activity patterns (engagement, recency)

Use Cases:
- SaaS subscription churn prediction
- Customer health scoring
- Proactive retention campaigns
"""

from glyphh import (
    Encoder, EncoderConfig, Concept, GlyphhModel,
    SimilarityCalculator, LayerConfig, SegmentConfig, Role
)

# Configure encoder with churn-relevant structure
config = EncoderConfig(
    dimension=10000,
    seed=42,
    layers=[
        LayerConfig(
            name="customer",
            similarity_weight=1.0,
            segments=[
                SegmentConfig(
                    name="metrics",
                    roles=[
                        Role(name="spend_trend", similarity_weight=1.0),
                        Role(name="feature_adoption", similarity_weight=0.9),
                        Role(name="engagement_level", similarity_weight=0.8),
                        Role(name="support_cases", similarity_weight=0.7),
                        Role(name="days_inactive", similarity_weight=0.9),
                    ]
                ),
                SegmentConfig(
                    name="segment",
                    roles=[
                        Role(name="tier", similarity_weight=0.5),
                        Role(name="industry", similarity_weight=0.4),
                    ]
                )
            ]
        )
    ]
)

encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Churn Prediction Model")
print("=" * 60)

# =============================================================================
# Historical Customer Data (for pattern learning)
# =============================================================================

# Customers who churned
churned_customers = [
    Concept(
        name="churned_001",
        attributes={
            "spend_trend": "decreasing",
            "feature_adoption": "low",
            "engagement_level": "low",
            "support_cases": "high",
            "days_inactive": "high",
            "tier": "mid-market",
            "industry": "retail",
            "outcome": "churned",
        }
    ),
    Concept(
        name="churned_002",
        attributes={
            "spend_trend": "decreasing",
            "feature_adoption": "medium",
            "engagement_level": "low",
            "support_cases": "high",
            "days_inactive": "medium",
            "tier": "enterprise",
            "industry": "finance",
            "outcome": "churned",
        }
    ),
]

# Customers who renewed
retained_customers = [
    Concept(
        name="retained_001",
        attributes={
            "spend_trend": "increasing",
            "feature_adoption": "high",
            "engagement_level": "high",
            "support_cases": "low",
            "days_inactive": "low",
            "tier": "mid-market",
            "industry": "tech",
            "outcome": "retained",
        }
    ),
    Concept(
        name="retained_002",
        attributes={
            "spend_trend": "stable",
            "feature_adoption": "high",
            "engagement_level": "high",
            "support_cases": "low",
            "days_inactive": "low",
            "tier": "enterprise",
            "industry": "healthcare",
            "outcome": "retained",
        }
    ),
]

# Encode historical data
print("\nEncoding historical customer data...")
churned_glyphs = []
for customer in churned_customers:
    glyph = encoder.encode(customer)
    churned_glyphs.append(glyph)
    print(f"  ✓ {customer.name} (CHURNED)")

retained_glyphs = []
for customer in retained_customers:
    glyph = encoder.encode(customer)
    retained_glyphs.append(glyph)
    print(f"  ✓ {customer.name} (RETAINED)")

# =============================================================================
# Churn Prediction Function
# =============================================================================

def predict_churn_risk(customer: Concept):
    """Predict churn risk based on similarity to historical patterns."""
    print(f"\n{'='*60}")
    print(f"CHURN RISK ANALYSIS: {customer.name}")
    print('='*60)
    
    customer_glyph = encoder.encode(customer)
    
    # Similarity to churned customers
    churned_scores = []
    for i, glyph in enumerate(churned_glyphs):
        result = calculator.compute_similarity(
            customer_glyph, glyph,
            edge_type="neural_cortex"
        )
        churned_scores.append(result.score)
    avg_churned = sum(churned_scores) / len(churned_scores)
    
    # Similarity to retained customers
    retained_scores = []
    for i, glyph in enumerate(retained_glyphs):
        result = calculator.compute_similarity(
            customer_glyph, glyph,
            edge_type="neural_cortex"
        )
        retained_scores.append(result.score)
    avg_retained = sum(retained_scores) / len(retained_scores)
    
    # Risk score
    risk_score = avg_churned / (avg_churned + avg_retained + 0.001) * 100
    
    print(f"\nSimilarity to churned customers: {avg_churned:.3f}")
    print(f"Similarity to retained customers: {avg_retained:.3f}")
    print(f"\nRisk Score: {risk_score:.1f}/100")
    
    if risk_score >= 60:
        print("⚠️  HIGH RISK - Immediate attention required")
    elif risk_score >= 40:
        print("⚡ MEDIUM RISK - Monitor closely")
    else:
        print("✓ LOW RISK - Healthy customer")
    
    return {"risk_score": risk_score}

# =============================================================================
# Test Predictions
# =============================================================================

print("\n" + "="*60)
print("TESTING CHURN PREDICTIONS")
print("="*60)

test_customers = [
    # High risk - similar to churned patterns
    Concept(
        name="customer_NEW001",
        attributes={
            "spend_trend": "decreasing",
            "feature_adoption": "low",
            "engagement_level": "low",
            "support_cases": "high",
            "days_inactive": "high",
            "tier": "mid-market",
            "industry": "retail",
        }
    ),
    # Low risk - similar to retained patterns
    Concept(
        name="customer_NEW002",
        attributes={
            "spend_trend": "increasing",
            "feature_adoption": "high",
            "engagement_level": "high",
            "support_cases": "low",
            "days_inactive": "low",
            "tier": "enterprise",
            "industry": "tech",
        }
    ),
]

for customer in test_customers:
    predict_churn_risk(customer)

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

all_glyphs = churned_glyphs + retained_glyphs
model = GlyphhModel(
    name="churn-model",
    version="1.0.0",
    encoder_config=config,
    glyphs=all_glyphs,
    metadata={
        "domain": "customer_success",
        "description": "Churn prediction using pattern matching",
    }
)

model.to_file("churn-model.glyphh")
print("✓ Model exported to churn-model.glyphh")

# Cleanup
import os
if os.path.exists("churn-model.glyphh"):
    os.remove("churn-model.glyphh")

print("\n" + "="*60)
print("KEY PRINCIPLES")
print("="*60)
print("""
1. NO HARDCODED SENTIMENT - Let the model discover patterns
2. SIGNALS, NOT RULES - Spend, usage, support, activity
3. CORTEX SIMILARITY - Find customers with similar patterns
4. EXPLAINABLE - Show which factors contribute to risk
""")
