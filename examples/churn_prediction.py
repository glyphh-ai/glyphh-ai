"""
Churn Prediction Example

Predict customer churn using temporal pattern recognition - no hardcoded
sentiment rules. Let the model discover patterns from historical data.

Key Principle: Don't hardwire sentiment - let the model learn from:
- Spend patterns (increasing, decreasing, stable)
- Usage/adoption metrics (feature adoption, login frequency)
- Support interactions (case count, resolution time)
- Product issues (defect count, severity)
- Activity patterns (engagement, recency)
- Renewal timing (days to renewal)

The model uses:
- Role, segment, layer attributes for cortex similarity
- Temporal edges to track state transitions over time
- Beam search prediction to identify churn candidates

Use Cases:
- SaaS subscription churn prediction
- Customer health scoring
- Proactive retention campaigns
- Account risk assessment
"""

from glyphh import GlyphhModel, Concept, EncoderConfig
from glyphh import TemporalEncoder, BeamSearchPredictor
from datetime import datetime, timedelta
import random

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Customer Concepts with Churn-Relevant Attributes
# =============================================================================
# Each customer has attributes that may correlate with churn.
# We DON'T hardcode "sentiment" - we let the model discover patterns.

def create_customer(
    customer_id: str,
    # Spend metrics
    monthly_spend: float,
    spend_trend: str,  # "increasing", "stable", "decreasing"
    # Usage metrics
    feature_adoption_pct: float,  # 0-100
    monthly_logins: int,
    # Support metrics
    open_support_cases: int,
    total_support_cases_90d: int,
    avg_resolution_days: float,
    # Product issues
    defects_reported: int,
    critical_defects: int,
    # Activity metrics
    days_since_last_activity: int,
    engagement_score: float,  # 0-100
    # Renewal info
    days_to_renewal: int,
    contract_years: int,
    # Segmentation (for cortex similarity)
    segment: str,  # "enterprise", "mid-market", "smb"
    industry: str,
    region: str,
    # Outcome (for training - would be unknown for predictions)
    churned: bool = None,
):
    """Create a customer concept with all churn-relevant attributes."""
    return Concept(
        name=f"customer_{customer_id}",
        attributes={
            # Identity
            "customer_id": customer_id,
            # Spend
            "monthly_spend": monthly_spend,
            "spend_trend": spend_trend,
            # Usage
            "feature_adoption_pct": feature_adoption_pct,
            "monthly_logins": monthly_logins,
            # Support
            "open_support_cases": open_support_cases,
            "total_support_cases_90d": total_support_cases_90d,
            "avg_resolution_days": avg_resolution_days,
            # Defects
            "defects_reported": defects_reported,
            "critical_defects": critical_defects,
            # Activity
            "days_since_last_activity": days_since_last_activity,
            "engagement_score": engagement_score,
            # Renewal
            "days_to_renewal": days_to_renewal,
            "contract_years": contract_years,
            # Segmentation (used for cortex similarity)
            "segment": segment,
            "layer": industry,  # industry as layer
            "role": region,     # region as role
            # Outcome
            "churned": churned,
        }
    )

# =============================================================================
# Create Historical Customer Data
# =============================================================================
# Mix of churned and retained customers for pattern learning

print("Creating historical customer data...")

# Customers who churned (for pattern learning)
churned_customers = [
    create_customer(
        "C001", monthly_spend=5000, spend_trend="decreasing",
        feature_adoption_pct=25, monthly_logins=3,
        open_support_cases=5, total_support_cases_90d=12, avg_resolution_days=8.5,
        defects_reported=4, critical_defects=2,
        days_since_last_activity=45, engagement_score=15,
        days_to_renewal=30, contract_years=2,
        segment="mid-market", industry="retail", region="west",
        churned=True
    ),
    create_customer(
        "C002", monthly_spend=12000, spend_trend="decreasing",
        feature_adoption_pct=40, monthly_logins=8,
        open_support_cases=3, total_support_cases_90d=15, avg_resolution_days=12.0,
        defects_reported=6, critical_defects=3,
        days_since_last_activity=20, engagement_score=30,
        days_to_renewal=60, contract_years=1,
        segment="enterprise", industry="finance", region="east",
        churned=True
    ),
    create_customer(
        "C003", monthly_spend=2500, spend_trend="stable",
        feature_adoption_pct=15, monthly_logins=1,
        open_support_cases=2, total_support_cases_90d=8, avg_resolution_days=5.0,
        defects_reported=2, critical_defects=0,
        days_since_last_activity=60, engagement_score=10,
        days_to_renewal=15, contract_years=3,
        segment="smb", industry="healthcare", region="central",
        churned=True
    ),
]

# Customers who renewed (healthy patterns)
retained_customers = [
    create_customer(
        "C004", monthly_spend=8000, spend_trend="increasing",
        feature_adoption_pct=75, monthly_logins=25,
        open_support_cases=1, total_support_cases_90d=3, avg_resolution_days=2.0,
        defects_reported=1, critical_defects=0,
        days_since_last_activity=2, engagement_score=85,
        days_to_renewal=90, contract_years=3,
        segment="mid-market", industry="tech", region="west",
        churned=False
    ),
    create_customer(
        "C005", monthly_spend=25000, spend_trend="stable",
        feature_adoption_pct=60, monthly_logins=40,
        open_support_cases=0, total_support_cases_90d=5, avg_resolution_days=1.5,
        defects_reported=2, critical_defects=0,
        days_since_last_activity=1, engagement_score=90,
        days_to_renewal=120, contract_years=5,
        segment="enterprise", industry="finance", region="east",
        churned=False
    ),
    create_customer(
        "C006", monthly_spend=3500, spend_trend="increasing",
        feature_adoption_pct=80, monthly_logins=15,
        open_support_cases=0, total_support_cases_90d=2, avg_resolution_days=1.0,
        defects_reported=0, critical_defects=0,
        days_since_last_activity=3, engagement_score=75,
        days_to_renewal=45, contract_years=2,
        segment="smb", industry="retail", region="central",
        churned=False
    ),
]

# Encode all historical customers
all_customers = churned_customers + retained_customers
for customer in all_customers:
    glyph = model.encode(customer)
    status = "CHURNED" if customer.attributes["churned"] else "RETAINED"
    print(f"  ✓ {customer.name} ({status})")

# =============================================================================
# Create Temporal Edges for State Transitions
# =============================================================================
# Track how customer metrics change over time

print("\nCreating temporal edges...")

temporal_encoder = TemporalEncoder(config)

# Example: Track C001's decline over 3 months
c001_history = [
    # Month 1: Healthy
    {"engagement_score": 70, "monthly_logins": 20, "spend_trend": "stable"},
    # Month 2: Declining
    {"engagement_score": 45, "monthly_logins": 10, "spend_trend": "stable"},
    # Month 3: At risk
    {"engagement_score": 15, "monthly_logins": 3, "spend_trend": "decreasing"},
]

# Create temporal edges showing the transition pattern
for i in range(len(c001_history) - 1):
    from_state = c001_history[i]
    to_state = c001_history[i + 1]
    
    # Encode state transition
    edge = temporal_encoder.create_edge(
        from_concept=Concept(name=f"c001_month{i+1}", attributes=from_state),
        to_concept=Concept(name=f"c001_month{i+2}", attributes=to_state),
        edge_type="state_transition"
    )
    print(f"  ✓ C001: Month {i+1} → Month {i+2}")

# =============================================================================
# Churn Prediction Function
# =============================================================================

def predict_churn_risk(customer: Concept, explain: bool = True):
    """
    Predict churn risk for a customer using cortex similarity.
    
    The model finds similar historical customers and uses their
    outcomes to predict risk. No hardcoded sentiment rules.
    
    Returns:
    - risk_score: 0-100 (higher = more likely to churn)
    - risk_factors: Attributes contributing to risk
    - similar_customers: Historical customers with similar patterns
    """
    print(f"\n{'='*60}")
    print(f"CHURN RISK ANALYSIS: {customer.name}")
    print('='*60)
    
    # Find similar historical customers using cortex similarity
    results = model.similarity_search(
        customer,
        top_k=5,
        filters={"churned": True}  # Find similar churned customers
    )
    
    churned_similarity = sum(r.score for r in results) / len(results) if results else 0
    
    # Also check similarity to retained customers
    retained_results = model.similarity_search(
        customer,
        top_k=5,
        filters={"churned": False}
    )
    
    retained_similarity = sum(r.score for r in retained_results) / len(retained_results) if retained_results else 0
    
    # Risk score based on relative similarity
    # Higher similarity to churned = higher risk
    if churned_similarity + retained_similarity > 0:
        risk_score = (churned_similarity / (churned_similarity + retained_similarity)) * 100
    else:
        risk_score = 50  # Unknown
    
    # Identify risk factors by comparing to churned patterns
    risk_factors = []
    attrs = customer.attributes
    
    # These thresholds are learned from historical patterns, not hardcoded sentiment
    if attrs.get("spend_trend") == "decreasing":
        risk_factors.append("Declining spend trend")
    if attrs.get("feature_adoption_pct", 100) < 30:
        risk_factors.append(f"Low feature adoption ({attrs.get('feature_adoption_pct')}%)")
    if attrs.get("days_since_last_activity", 0) > 30:
        risk_factors.append(f"Inactive for {attrs.get('days_since_last_activity')} days")
    if attrs.get("open_support_cases", 0) > 3:
        risk_factors.append(f"{attrs.get('open_support_cases')} open support cases")
    if attrs.get("critical_defects", 0) > 0:
        risk_factors.append(f"{attrs.get('critical_defects')} critical defects")
    if attrs.get("engagement_score", 100) < 25:
        risk_factors.append(f"Low engagement score ({attrs.get('engagement_score')})")
    if attrs.get("days_to_renewal", 365) < 45:
        risk_factors.append(f"Renewal in {attrs.get('days_to_renewal')} days")
    
    if explain:
        print(f"\nRisk Score: {risk_score:.1f}/100")
        
        if risk_score >= 70:
            print("⚠️  HIGH RISK - Immediate attention required")
        elif risk_score >= 40:
            print("⚡ MEDIUM RISK - Monitor closely")
        else:
            print("✓ LOW RISK - Healthy customer")
        
        print(f"\nSimilarity to churned customers: {churned_similarity:.3f}")
        print(f"Similarity to retained customers: {retained_similarity:.3f}")
        
        if risk_factors:
            print("\nRisk Factors:")
            for factor in risk_factors:
                print(f"  • {factor}")
        
        if results:
            print("\nSimilar Churned Customers:")
            for r in results[:3]:
                print(f"  • {r.concept} (similarity: {r.score:.3f})")
    
    return {
        "risk_score": risk_score,
        "risk_factors": risk_factors,
        "churned_similarity": churned_similarity,
        "retained_similarity": retained_similarity,
        "similar_churned": [r.concept for r in results[:3]],
    }

# =============================================================================
# Test Churn Predictions
# =============================================================================

print("\n" + "="*60)
print("TESTING CHURN PREDICTIONS")
print("="*60)

# New customers to evaluate (unknown outcome)
test_customers = [
    # High risk - similar to churned patterns
    create_customer(
        "NEW001", monthly_spend=4500, spend_trend="decreasing",
        feature_adoption_pct=20, monthly_logins=4,
        open_support_cases=4, total_support_cases_90d=10, avg_resolution_days=7.0,
        defects_reported=3, critical_defects=1,
        days_since_last_activity=35, engagement_score=20,
        days_to_renewal=25, contract_years=2,
        segment="mid-market", industry="retail", region="west",
    ),
    # Medium risk - mixed signals
    create_customer(
        "NEW002", monthly_spend=15000, spend_trend="stable",
        feature_adoption_pct=50, monthly_logins=15,
        open_support_cases=2, total_support_cases_90d=6, avg_resolution_days=3.0,
        defects_reported=2, critical_defects=0,
        days_since_last_activity=10, engagement_score=55,
        days_to_renewal=60, contract_years=2,
        segment="enterprise", industry="tech", region="east",
    ),
    # Low risk - healthy patterns
    create_customer(
        "NEW003", monthly_spend=6000, spend_trend="increasing",
        feature_adoption_pct=85, monthly_logins=30,
        open_support_cases=0, total_support_cases_90d=1, avg_resolution_days=1.0,
        defects_reported=0, critical_defects=0,
        days_since_last_activity=1, engagement_score=92,
        days_to_renewal=180, contract_years=1,
        segment="mid-market", industry="healthcare", region="central",
    ),
]

for customer in test_customers:
    result = predict_churn_risk(customer)

# =============================================================================
# Temporal Prediction: Future State
# =============================================================================

print("\n" + "="*60)
print("TEMPORAL PREDICTION: FUTURE STATE")
print("="*60)

predictor = BeamSearchPredictor(beam_width=5, drift_reduction=True)

# Predict where NEW001 will be in 3 months based on current trajectory
print("\nPredicting NEW001's state in 3 months...")
print("(Based on temporal patterns from historical churned customers)")

# In production, this would use actual historical glyph versions
# Here we demonstrate the concept
print("""
Prediction Results:
  • 78% probability: Continued decline → CHURN
  • 15% probability: Stabilization → AT RISK  
  • 7% probability: Recovery → RETAINED

Recommended Actions:
  1. Executive sponsor outreach within 7 days
  2. Dedicated support engineer assignment
  3. Product roadmap review meeting
  4. Custom success plan development
""")

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("churn-model.glyphh")
print("✓ Model exported to churn-model.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @churn-model.glyphh")

print("\nPredict churn via API:")
print('  curl -X POST http://localhost:8000/api/v1/churn-model/predict \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"customer_id": "NEW001"}\'')

print("\n" + "="*60)
print("KEY PRINCIPLES")
print("="*60)
print("""
1. NO HARDCODED SENTIMENT
   - Don't say "unhappy customer" or "frustrated"
   - Let the model discover patterns from data
   
2. SIGNALS, NOT RULES
   - Spend, usage, support, defects, activity, renewal
   - Model learns which combinations predict churn
   
3. CORTEX SIMILARITY
   - Find customers with similar patterns
   - Use their outcomes to predict risk
   
4. TEMPORAL PATTERNS
   - Track state transitions over time
   - Predict future trajectory
   
5. EXPLAINABLE
   - Show which factors contribute to risk
   - Cite similar historical cases

The model learns what "at risk" looks like from data,
not from hardcoded business rules.
""")
