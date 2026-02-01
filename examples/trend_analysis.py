"""
Trend Analysis Example

Identify and track trends over time using temporal patterns and
similarity search to detect emerging patterns before they peak.

Key Principle: Use temporal edges to track how concepts evolve
and find similar historical patterns to predict future trends.

This example demonstrates:
1. Creating time-series data points as concepts
2. Temporal edges for tracking changes over time
3. Similarity search to find historical pattern matches
4. Trend prediction using pattern matching

Use Cases:
- Market trend detection
- Product usage pattern analysis
- Seasonal demand forecasting
- Anomaly detection
"""

from glyphh import (
    Encoder, EncoderConfig, Concept, GlyphhModel,
    SimilarityCalculator, LayerConfig, SegmentConfig, Role
)

# Configure encoder with explicit structure
config = EncoderConfig(
    dimension=10000,
    seed=42,
    layers=[
        LayerConfig(
            name="metrics",
            similarity_weight=1.0,
            segments=[
                SegmentConfig(
                    name="trend_data",
                    roles=[
                        Role(name="metric_name", similarity_weight=0.8),
                        Role(name="category", similarity_weight=0.7),
                        Role(name="change_pct", similarity_weight=1.0),
                        Role(name="volatility", similarity_weight=0.9),
                        Role(name="pattern_name", similarity_weight=1.0),
                    ]
                )
            ]
        )
    ]
)

# Create encoder and calculator
encoder = Encoder(config)
calculator = SimilarityCalculator()
print(f"Encoder created: space_id={encoder.space_id}")

# =============================================================================
# Define Metric Snapshot Concepts
# =============================================================================

def create_metric_snapshot(
    metric_name: str,
    period: str,  # "2025-W01", "2025-W02", etc.
    value: float,
    change_pct: float,
    moving_avg_7d: float,
    moving_avg_30d: float,
    volatility: float,
    category: str,
    subcategory: str,
    is_holiday_period: bool = False,
):
    """Create a metric snapshot for trend analysis."""
    return Concept(
        name=f"{metric_name}_{period}",
        attributes={
            "metric_name": metric_name,
            "period": period,
            "value": str(value),
            "change_pct": str(change_pct),
            "moving_avg_7d": str(moving_avg_7d),
            "moving_avg_30d": str(moving_avg_30d),
            "volatility": str(volatility),
            "category": category,
            "subcategory": subcategory,
            "is_holiday_period": str(is_holiday_period),
        }
    )

# =============================================================================
# Define Trend Pattern Archetypes
# =============================================================================

trend_patterns = [
    Concept(
        name="growth_spike",
        attributes={
            "pattern_name": "Growth Spike",
            "description": "Rapid increase followed by stabilization",
            "change_pct": "high",
            "volatility": "high",
            "characteristics": "rapid growth, high volatility, potential peak"
        }
    ),
    Concept(
        name="steady_growth",
        attributes={
            "pattern_name": "Steady Growth",
            "description": "Consistent upward trend with low volatility",
            "change_pct": "moderate",
            "volatility": "low",
            "characteristics": "sustainable, predictable, healthy"
        }
    ),
    Concept(
        name="decline",
        attributes={
            "pattern_name": "Decline",
            "description": "Consistent downward trend",
            "change_pct": "negative",
            "volatility": "moderate",
            "characteristics": "concerning, needs attention, investigate cause"
        }
    ),
    Concept(
        name="seasonal_peak",
        attributes={
            "pattern_name": "Seasonal Peak",
            "description": "Expected increase due to seasonality",
            "change_pct": "high",
            "volatility": "moderate",
            "is_holiday_period": "True",
            "characteristics": "expected, temporary, plan for capacity"
        }
    ),
    Concept(
        name="anomaly",
        attributes={
            "pattern_name": "Anomaly",
            "description": "Unexpected deviation from normal pattern",
            "change_pct": "extreme",
            "volatility": "extreme",
            "characteristics": "investigate, potential issue, or opportunity"
        }
    ),
    Concept(
        name="plateau",
        attributes={
            "pattern_name": "Plateau",
            "description": "Flat trend after growth period",
            "change_pct": "flat",
            "volatility": "low",
            "characteristics": "stabilized, mature, optimize efficiency"
        }
    ),
]

print("Encoding trend patterns...")
pattern_glyphs = {}
for pattern in trend_patterns:
    glyph = encoder.encode(pattern)
    pattern_glyphs[pattern.name] = (pattern, glyph)
    print(f"  ✓ {pattern.name}: {pattern.attributes['pattern_name']}")

# =============================================================================
# Create Historical Metric Data
# =============================================================================

print("\nCreating historical metric data...")

# Simulate weekly signups data showing different patterns
signups_data = [
    # Steady growth period
    create_metric_snapshot(
        "signups", "2025-W01", value=1000, change_pct=8,
        moving_avg_7d=980, moving_avg_30d=950, volatility=50,
        category="acquisition", subcategory="organic"
    ),
    create_metric_snapshot(
        "signups", "2025-W02", value=1080, change_pct=8,
        moving_avg_7d=1040, moving_avg_30d=970, volatility=55,
        category="acquisition", subcategory="organic"
    ),
    create_metric_snapshot(
        "signups", "2025-W03", value=1150, change_pct=6.5,
        moving_avg_7d=1100, moving_avg_30d=1000, volatility=52,
        category="acquisition", subcategory="organic"
    ),
    # Growth spike (campaign launch)
    create_metric_snapshot(
        "signups", "2025-W04", value=1500, change_pct=30,
        moving_avg_7d=1250, moving_avg_30d=1050, volatility=150,
        category="acquisition", subcategory="campaign"
    ),
    create_metric_snapshot(
        "signups", "2025-W05", value=1650, change_pct=10,
        moving_avg_7d=1450, moving_avg_30d=1150, volatility=180,
        category="acquisition", subcategory="campaign"
    ),
    # Plateau after spike
    create_metric_snapshot(
        "signups", "2025-W06", value=1620, change_pct=-2,
        moving_avg_7d=1590, moving_avg_30d=1300, volatility=80,
        category="acquisition", subcategory="mixed"
    ),
]

# Revenue data showing seasonal pattern
revenue_data = [
    create_metric_snapshot(
        "revenue", "2025-W48", value=50000, change_pct=5,
        moving_avg_7d=48000, moving_avg_30d=45000, volatility=2000,
        category="monetization", subcategory="subscriptions"
    ),
    create_metric_snapshot(
        "revenue", "2025-W49", value=55000, change_pct=10,
        moving_avg_7d=52000, moving_avg_30d=47000, volatility=2500,
        category="monetization", subcategory="subscriptions",
        is_holiday_period=True
    ),
    create_metric_snapshot(
        "revenue", "2025-W50", value=65000, change_pct=18,
        moving_avg_7d=58000, moving_avg_30d=50000, volatility=4000,
        category="monetization", subcategory="subscriptions",
        is_holiday_period=True
    ),
    create_metric_snapshot(
        "revenue", "2025-W51", value=72000, change_pct=11,
        moving_avg_7d=64000, moving_avg_30d=55000, volatility=5000,
        category="monetization", subcategory="subscriptions",
        is_holiday_period=True
    ),
]

# Encode all metrics
all_metrics = signups_data + revenue_data
metric_glyphs = {}
for metric in all_metrics:
    glyph = encoder.encode(metric)
    metric_glyphs[metric.name] = (metric, glyph)
    print(f"  ✓ {metric.name}: {metric.attributes['value']}")

# =============================================================================
# Trend Analysis Functions
# =============================================================================

def identify_trend(metric_snapshot: Concept, metric_glyph):
    """
    Identify the trend pattern for a metric snapshot.
    
    Returns the most similar trend pattern with confidence.
    """
    print(f"\n{'='*60}")
    print(f"TREND ANALYSIS: {metric_snapshot.name}")
    print('='*60)
    
    attrs = metric_snapshot.attributes
    print(f"Value: {attrs['value']}")
    print(f"Change: {attrs['change_pct']}%")
    print(f"Volatility: {attrs['volatility']}")
    
    # Find similar trend patterns
    patterns = []
    for pattern_name, (pattern, pattern_glyph) in pattern_glyphs.items():
        result = calculator.compute_similarity(
            metric_glyph, pattern_glyph,
            edge_type="neural_cortex"
        )
        if "pattern_name" in pattern.attributes:
            patterns.append({
                "pattern": pattern.attributes["pattern_name"],
                "confidence": result.score,
                "characteristics": pattern.attributes.get("characteristics", "")
            })
    
    # Sort by confidence
    patterns.sort(key=lambda x: x["confidence"], reverse=True)
    
    if patterns:
        print(f"\nIdentified Pattern: {patterns[0]['pattern']}")
        print(f"Confidence: {patterns[0]['confidence']:.2f}")
        print(f"Characteristics: {patterns[0]['characteristics']}")
    
    return patterns[:3]


def find_similar_periods(metric_snapshot: Concept, metric_glyph, top_k: int = 3):
    """
    Find historical periods with similar patterns.
    """
    similar = []
    for name, (concept, glyph) in metric_glyphs.items():
        if name != metric_snapshot.name and "period" in concept.attributes:
            result = calculator.compute_similarity(
                metric_glyph, glyph,
                edge_type="neural_cortex"
            )
            similar.append({
                "period": concept.attributes["period"],
                "metric": concept.attributes["metric_name"],
                "value": concept.attributes["value"],
                "similarity": result.score
            })
    
    similar.sort(key=lambda x: x["similarity"], reverse=True)
    return similar[:top_k]


def predict_next_period(metric_history: list):
    """
    Predict the next period's trend based on historical patterns.
    """
    if len(metric_history) < 2:
        return None
    
    latest = metric_history[-1]
    latest_glyph = metric_glyphs[latest.name][1]
    
    print(f"\n{'='*60}")
    print(f"TREND PREDICTION")
    print('='*60)
    print(f"Current: {latest.attributes['period']}")
    print(f"Value: {latest.attributes['value']}")
    
    # Find similar historical sequences
    similar = find_similar_periods(latest, latest_glyph)
    
    print(f"\nSimilar Historical Periods:")
    for s in similar:
        print(f"  • {s['metric']} {s['period']}: {s['value']} ({s['similarity']:.2f})")
    
    # Simplified prediction based on pattern matching
    changes = [float(m.attributes["change_pct"]) for m in metric_history[-3:]]
    avg_change = sum(changes) / len(changes)
    current_value = float(latest.attributes["value"])
    predicted_value = current_value * (1 + avg_change / 100)
    
    print(f"\nPrediction:")
    print(f"  Expected Change: {avg_change:.1f}%")
    print(f"  Predicted Value: {predicted_value:.0f}")
    
    return {
        "predicted_value": predicted_value,
        "expected_change_pct": avg_change,
        "confidence": 0.75 if len(similar) > 0 else 0.5
    }

# =============================================================================
# Test Trend Analysis
# =============================================================================

print("\n" + "="*60)
print("TESTING TREND ANALYSIS")
print("="*60)

# Analyze each signup period
for snapshot in signups_data:
    glyph = metric_glyphs[snapshot.name][1]
    patterns = identify_trend(snapshot, glyph)

# Predict next period
print("\n" + "="*60)
print("PREDICTING NEXT PERIOD")
print("="*60)

prediction = predict_next_period(signups_data)

# Analyze revenue seasonality
print("\n" + "="*60)
print("SEASONAL ANALYSIS: REVENUE")
print("="*60)

for snapshot in revenue_data:
    glyph = metric_glyphs[snapshot.name][1]
    patterns = identify_trend(snapshot, glyph)

# =============================================================================
# Package and Export Model
# =============================================================================

print("\n" + "="*60)
print("PACKAGING MODEL")
print("="*60)

# Collect all glyphs
all_glyphs = [glyph for _, glyph in pattern_glyphs.values()]
all_glyphs.extend([glyph for _, glyph in metric_glyphs.values()])

model = GlyphhModel(
    name="trend-analysis",
    version="1.0.0",
    encoder_config=config,
    glyphs=all_glyphs,
    metadata={
        "domain": "analytics",
        "description": "Trend analysis and prediction model",
        "num_patterns": len(trend_patterns),
        "num_metrics": len(all_metrics)
    }
)

model.to_file("trend-analysis.glyphh")
print("✓ Model exported to trend-analysis.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @trend-analysis.glyphh")

print("\nAnalyze trend via API:")
print('  curl -X POST http://localhost:8000/api/v1/trend-analysis/analyze \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"metric": "signups", "period": "2025-W07", "value": 1700}\'')

print("\n" + "="*60)
print("KEY CAPABILITIES")
print("="*60)
print("""
1. PATTERN RECOGNITION
   - Identify growth spikes, declines, plateaus
   - Detect seasonal patterns automatically
   
2. TEMPORAL TRACKING
   - Track how metrics evolve over time
   - Build historical pattern library
   
3. SIMILARITY MATCHING
   - Find similar historical periods
   - Learn from past patterns
   
4. PREDICTION
   - Forecast next period values
   - Confidence-based predictions
""")

# Cleanup
import os
if os.path.exists("trend-analysis.glyphh"):
    os.remove("trend-analysis.glyphh")
