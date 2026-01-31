"""
Customer Sentiment Analysis Example

Track customer sentiment over time using temporal patterns to identify
trends and predict satisfaction changes before they become problems.

Key Principle: Don't classify sentiment with rules - let the model learn
patterns from interaction history and track changes over time.

This example demonstrates:
1. Creating customer interaction concepts with sentiment signals
2. Temporal edges to track sentiment changes over time
3. Similarity search to find customers with similar patterns
4. Trend prediction using historical patterns

Use Cases:
- Customer health monitoring
- Proactive support intervention
- NPS prediction
- Account risk assessment
"""

from glyphh import GlyphhModel, Concept, EncoderConfig
from glyphh import TemporalEncoder

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Customer Interaction Concepts
# =============================================================================
# Each interaction captures signals that may indicate sentiment
# We DON'T label as "happy" or "angry" - we capture observable signals

def create_interaction(
    customer_id: str,
    interaction_id: str,
    # Interaction metadata
    channel: str,  # "email", "chat", "phone", "social"
    interaction_type: str,  # "support", "sales", "feedback", "complaint"
    # Observable signals
    response_time_minutes: int,
    message_length: int,
    exclamation_count: int,
    question_count: int,
    caps_ratio: float,  # 0-1, ratio of caps to total
    # Resolution signals
    resolved: bool,
    escalated: bool,
    follow_ups: int,
    # Engagement signals
    nps_score: int = None,  # 0-10 if provided
    csat_score: int = None,  # 1-5 if provided
):
    """Create a customer interaction concept with sentiment signals."""
    return Concept(
        name=f"{customer_id}_{interaction_id}",
        attributes={
            "customer_id": customer_id,
            "interaction_id": interaction_id,
            "channel": channel,
            "interaction_type": interaction_type,
            "response_time_minutes": response_time_minutes,
            "message_length": message_length,
            "exclamation_count": exclamation_count,
            "question_count": question_count,
            "caps_ratio": caps_ratio,
            "resolved": resolved,
            "escalated": escalated,
            "follow_ups": follow_ups,
            "nps_score": nps_score,
            "csat_score": csat_score,
        }
    )

# =============================================================================
# Create Historical Interaction Data
# =============================================================================

print("Creating historical interaction data...")

# Customer A: Declining sentiment pattern
customer_a_interactions = [
    create_interaction(
        "CUST_A", "INT_001",
        channel="email", interaction_type="support",
        response_time_minutes=30, message_length=150,
        exclamation_count=0, question_count=2, caps_ratio=0.02,
        resolved=True, escalated=False, follow_ups=0,
        csat_score=5
    ),
    create_interaction(
        "CUST_A", "INT_002",
        channel="chat", interaction_type="support",
        response_time_minutes=45, message_length=280,
        exclamation_count=2, question_count=4, caps_ratio=0.05,
        resolved=True, escalated=False, follow_ups=1,
        csat_score=4
    ),
    create_interaction(
        "CUST_A", "INT_003",
        channel="phone", interaction_type="complaint",
        response_time_minutes=5, message_length=500,
        exclamation_count=5, question_count=3, caps_ratio=0.15,
        resolved=False, escalated=True, follow_ups=3,
        csat_score=2
    ),
]

# Customer B: Stable positive pattern
customer_b_interactions = [
    create_interaction(
        "CUST_B", "INT_001",
        channel="email", interaction_type="feedback",
        response_time_minutes=120, message_length=200,
        exclamation_count=1, question_count=1, caps_ratio=0.01,
        resolved=True, escalated=False, follow_ups=0,
        nps_score=9
    ),
    create_interaction(
        "CUST_B", "INT_002",
        channel="chat", interaction_type="support",
        response_time_minutes=60, message_length=100,
        exclamation_count=0, question_count=2, caps_ratio=0.01,
        resolved=True, escalated=False, follow_ups=0,
        csat_score=5
    ),
]

# Customer C: Improving pattern
customer_c_interactions = [
    create_interaction(
        "CUST_C", "INT_001",
        channel="social", interaction_type="complaint",
        response_time_minutes=10, message_length=280,
        exclamation_count=4, question_count=2, caps_ratio=0.20,
        resolved=False, escalated=True, follow_ups=2,
        nps_score=3
    ),
    create_interaction(
        "CUST_C", "INT_002",
        channel="phone", interaction_type="support",
        response_time_minutes=30, message_length=150,
        exclamation_count=1, question_count=3, caps_ratio=0.05,
        resolved=True, escalated=False, follow_ups=1,
        csat_score=4
    ),
    create_interaction(
        "CUST_C", "INT_003",
        channel="email", interaction_type="feedback",
        response_time_minutes=180, message_length=300,
        exclamation_count=2, question_count=0, caps_ratio=0.01,
        resolved=True, escalated=False, follow_ups=0,
        nps_score=8
    ),
]

# Encode all interactions
all_interactions = customer_a_interactions + customer_b_interactions + customer_c_interactions
for interaction in all_interactions:
    glyph = model.encode(interaction)
    cust = interaction.attributes["customer_id"]
    int_id = interaction.attributes["interaction_id"]
    print(f"  ✓ {cust}/{int_id}: {interaction.attributes['interaction_type']}")

# =============================================================================
# Create Temporal Edges for Sentiment Tracking
# =============================================================================

print("\nCreating temporal edges for sentiment tracking...")

temporal_encoder = TemporalEncoder(config)

# Track Customer A's decline
for i in range(len(customer_a_interactions) - 1):
    from_int = customer_a_interactions[i]
    to_int = customer_a_interactions[i + 1]
    
    edge = temporal_encoder.create_edge(
        from_concept=from_int,
        to_concept=to_int,
        edge_type="sentiment_transition"
    )
    print(f"  ✓ CUST_A: {from_int.attributes['interaction_id']} → {to_int.attributes['interaction_id']}")

# Track Customer C's improvement
for i in range(len(customer_c_interactions) - 1):
    from_int = customer_c_interactions[i]
    to_int = customer_c_interactions[i + 1]
    
    edge = temporal_encoder.create_edge(
        from_concept=from_int,
        to_concept=to_int,
        edge_type="sentiment_transition"
    )
    print(f"  ✓ CUST_C: {from_int.attributes['interaction_id']} → {to_int.attributes['interaction_id']}")

# =============================================================================
# Sentiment Analysis Functions
# =============================================================================

def analyze_sentiment_signals(interaction: Concept):
    """
    Analyze sentiment signals from an interaction.
    
    Returns a signal profile, not a sentiment label.
    """
    attrs = interaction.attributes
    
    signals = {
        "urgency": "high" if attrs["response_time_minutes"] < 15 else "normal",
        "frustration_indicators": attrs["exclamation_count"] + (attrs["caps_ratio"] * 10),
        "complexity": attrs["question_count"] + attrs["follow_ups"],
        "resolution_success": attrs["resolved"] and not attrs["escalated"],
    }
    
    return signals


def find_similar_patterns(customer_id: str, recent_interactions: list):
    """
    Find customers with similar interaction patterns.
    
    Uses temporal similarity to identify customers who had
    similar trajectories in the past.
    """
    print(f"\n{'='*60}")
    print(f"PATTERN ANALYSIS: {customer_id}")
    print('='*60)
    
    if not recent_interactions:
        return {"pattern": "unknown", "similar_customers": []}
    
    # Get the most recent interaction
    latest = recent_interactions[-1]
    
    # Find similar interactions from other customers
    results = model.similarity_search(latest, top_k=5)
    
    # Analyze the pattern
    similar_customers = []
    for result in results:
        if result.attributes["customer_id"] != customer_id:
            similar_customers.append({
                "customer": result.attributes["customer_id"],
                "similarity": result.score,
                "interaction_type": result.attributes["interaction_type"]
            })
    
    # Determine trend from recent interactions
    if len(recent_interactions) >= 2:
        first = recent_interactions[0].attributes
        last = recent_interactions[-1].attributes
        
        # Compare signals
        first_score = first.get("csat_score") or first.get("nps_score", 5)
        last_score = last.get("csat_score") or last.get("nps_score", 5)
        
        if last_score < first_score - 1:
            trend = "declining"
        elif last_score > first_score + 1:
            trend = "improving"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"
    
    print(f"\nTrend: {trend.upper()}")
    print(f"\nSimilar Customer Patterns:")
    for sc in similar_customers[:3]:
        print(f"  • {sc['customer']}: {sc['similarity']:.2f} similarity")
    
    return {
        "pattern": trend,
        "similar_customers": similar_customers[:3]
    }

# =============================================================================
# Test Sentiment Analysis
# =============================================================================

print("\n" + "="*60)
print("TESTING SENTIMENT ANALYSIS")
print("="*60)

# Analyze Customer A (declining)
print("\n--- Customer A Analysis ---")
result_a = find_similar_patterns("CUST_A", customer_a_interactions)
print(f"Pattern: {result_a['pattern']}")

# Analyze Customer B (stable)
print("\n--- Customer B Analysis ---")
result_b = find_similar_patterns("CUST_B", customer_b_interactions)
print(f"Pattern: {result_b['pattern']}")

# Analyze Customer C (improving)
print("\n--- Customer C Analysis ---")
result_c = find_similar_patterns("CUST_C", customer_c_interactions)
print(f"Pattern: {result_c['pattern']}")

# =============================================================================
# New Customer Prediction
# =============================================================================

print("\n" + "="*60)
print("NEW CUSTOMER PREDICTION")
print("="*60)

# New customer with concerning signals
new_interaction = create_interaction(
    "CUST_NEW", "INT_001",
    channel="chat", interaction_type="complaint",
    response_time_minutes=8, message_length=400,
    exclamation_count=6, question_count=4, caps_ratio=0.18,
    resolved=False, escalated=True, follow_ups=2,
    csat_score=2
)

print("\nNew customer interaction signals:")
signals = analyze_sentiment_signals(new_interaction)
for key, value in signals.items():
    print(f"  • {key}: {value}")

# Find similar patterns
print("\nFinding similar historical patterns...")
results = model.similarity_search(new_interaction, top_k=3)
print("\nMost similar past interactions:")
for r in results:
    attrs = r.attributes
    print(f"  • {attrs['customer_id']}/{attrs['interaction_id']}")
    print(f"    Type: {attrs['interaction_type']}, Score: {r.score:.2f}")

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("customer-sentiment.glyphh")
print("✓ Model exported to customer-sentiment.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @customer-sentiment.glyphh")

print("\nAnalyze sentiment via API:")
print('  curl -X POST http://localhost:8000/api/v1/customer-sentiment/analyze \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"customer_id": "CUST_001", "interaction_data": {...}}\'')

print("\n" + "="*60)
print("KEY PRINCIPLES")
print("="*60)
print("""
1. SIGNALS, NOT LABELS
   - Capture observable signals (caps, exclamations, escalations)
   - Don't label as "angry" or "happy"
   
2. TEMPORAL PATTERNS
   - Track how signals change over time
   - Identify declining vs improving trajectories
   
3. PATTERN MATCHING
   - Find customers with similar historical patterns
   - Use their outcomes to predict risk
   
4. PROACTIVE INTERVENTION
   - Identify at-risk customers early
   - Enable proactive support outreach
""")
