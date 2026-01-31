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
4. Trend prediction using beam search

Use Cases:
- Market trend detection
- Product usage pattern analysis
- Seasonal demand forecasting
- Anomaly detection
"""

from glyphh import GlyphhModel, Concept, EncoderConfig
from glyphh import TemporalEncoder, BeamSearchPredictor

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Metric Snapshot Concepts
# =============================================================================

def create_metric_snapshot(
    metric_name: str,
    period: str,  # "2025-W01", "2025-W02", etc.
    # Core metrics
    value: float,
    change_pct: float,  # vs previous period
    # Trend indicators
    moving_avg_7d: float,
    moving_avg_30d: float,
    volatility: float,  # standard deviation
    # Context
    category: str,
    subcategory: str,
    # Seasonality
    is_holiday_period: bool = False,
    day_of_week_effect: float = 0,  # -1 to 1
):
    """Create a metric snapshot for trend analysis."""
    return Concept(
        name=f"{metric_name}_{period}",
        attributes={
            "metric_name": metric_name,
            "period": period,
            "value": value,
            "change_pct": change_pct,
            "moving_avg_7d": moving_avg_7d,
            "moving_avg_30d": moving_avg_30d,
            "volatility": volatility,
            "category": category,
            "subcategory": subcategory,
            "is_holiday_period": is_holiday_period,
            "day_of_week_effect": day_of_week_effect,
            # For cortex similarity
            "layer": category,
            "role": metric_name,
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
            "change_pct_min": 20,
            "volatility_high": True,
            "typical_duration_weeks": 2,
            "characteristics": ["rapid growth", "high volatility", "potential peak"]
        }
    ),
    Concept(
        name="steady_growth",
        attributes={
            "pattern_name": "Steady Growth",
            "description": "Consistent upward trend with low volatility",
            "change_pct_range": [5, 15],
            "volatility_low": True,
            "typical_duration_weeks": 8,
            "characteristics": ["sustainable", "predictable", "healthy"]
        }
    ),
    Concept(
        name="decline",
        attributes={
            "pattern_name": "Decline",
            "description": "Consistent downward trend",
            "change_pct_max": -5,
            "typical_duration_weeks": 4,
            "characteristics": ["concerning", "needs attention", "investigate cause"]
        }
    ),
    Concept(
        name="seasonal_peak",
        attributes={
            "pattern_name": "Seasonal Peak",
            "description": "Expected increase due to seasonality",
            "is_holiday_period": True,
            "typical_duration_weeks": 3,
            "characteristics": ["expected", "temporary", "plan for capacity"]
        }
    ),
    Concept(
        name="anomaly",
        attributes={
            "pattern_name": "Anomaly",
            "description": "Unexpected deviation from normal pattern",
            "volatility_extreme": True,
            "characteristics": ["investigate", "potential issue", "or opportunity"]
        }
    ),
    Concept(
        name="plateau",
        attributes={
            "pattern_name": "Plateau",
            "description": "Flat trend after growth period",
            "change_pct_range": [-2, 2],
            "volatility_low": True,
            "characteristics": ["stabilized", "mature", "optimize efficiency"]
        }
    ),
]

print("Encoding trend patterns...")
for pattern in trend_patterns:
    glyph = model.encode(pattern)
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
for metric in all_metrics:
    glyph = model.encode(metric)
    print(f"  ✓ {metric.name}: {metric.attributes['value']}")

# =============================================================================
# Create Temporal Edges
# =============================================================================

print("\nCreating temporal edges...")

temporal_encoder = TemporalEncoder(config)

# Link signups data sequentially
for i in range(len(signups_data) - 1):
    edge = temporal_encoder.create_edge(
        from_concept=signups_data[i],
        to_concept=signups_data[i + 1],
        edge_type="metric_transition"
    )
    print(f"  ✓ {signups_data[i].attributes['period']} → {signups_data[i+1].attributes['period']}")

# Link revenue data
for i in range(len(revenue_data) - 1):
    edge = temporal_encoder.create_edge(
        from_concept=revenue_data[i],
        to_concept=revenue_data[i + 1],
        edge_type="metric_transition"
    )

# =============================================================================
# Trend Analysis Functions
# =============================================================================

def identify_trend(metric_snapshot: Concept):
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
    results = model.similarity_search(metric_snapshot, top_k=3)
    
    patterns = []
    for result in results:
        if "pattern_name" in result.attributes:
            patterns.append({
                "pattern": result.attributes["pattern_name"],
                "confidence": result.score,
                "characteristics": result.attributes.get("characteristics", [])
            })
    
    if patterns:
        print(f"\nIdentified Pattern: {patterns[0]['pattern']}")
        print(f"Confidence: {patterns[0]['confidence']:.2f}")
        print(f"Characteristics: {', '.join(patterns[0]['characteristics'])}")
    
    return patterns


def find_similar_periods(metric_snapshot: Concept, top_k: int = 3):
    """
    Find historical periods with similar patterns.
    """
    results = model.similarity_search(metric_snapshot, top_k=top_k + 1)
    
    similar = []
    for result in results:
        if "period" in result.attributes and result.concept != metric_snapshot.name:
            similar.append({
                "period": result.attributes["period"],
                "metric": result.attributes["metric_name"],
                "value": result.attributes["value"],
                "similarity": result.score
            })
    
    return similar[:top_k]


def predict_next_period(metric_history: list):
    """
    Predict the next period's trend based on historical patterns.
    """
    if len(metric_history) < 2:
        return None
    
    latest = metric_history[-1]
    
    print(f"\n{'='*60}")
    print(f"TREND PREDICTION")
    print('='*60)
    print(f"Current: {latest.attributes['period']}")
    print(f"Value: {latest.attributes['value']}")
    
    # Find similar historical sequences
    similar = find_similar_periods(latest)
    
    print(f"\nSimilar Historical Periods:")
    for s in similar:
        print(f"  • {s['metric']} {s['period']}: {s['value']} ({s['similarity']:.2f})")
    
    # Use beam search for prediction
    predictor = BeamSearchPredictor(beam_width=3, drift_reduction=True)
    
    # Simplified prediction based on pattern matching
    avg_change = sum(m.attributes["change_pct"] for m in metric_history[-3:]) / 3
    predicted_value = latest.attributes["value"] * (1 + avg_change / 100)
    
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
    patterns = identify_trend(snapshot)

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
    patterns = identify_trend(snapshot)

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("trend-analysis.glyphh")
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
