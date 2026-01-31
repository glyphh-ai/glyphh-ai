"""
User Segmentation Example

Segment users based on behavioral patterns and attributes using
similarity clustering and fact trees for hierarchical grouping.

Key Principle: Let the model discover natural segments through
similarity rather than predefined rules.

This example demonstrates:
1. Creating user profile concepts with behavioral attributes
2. Similarity search for finding similar users
3. Fact trees for hierarchical segment relationships
4. Dynamic segment discovery through clustering

Use Cases:
- Marketing campaign targeting
- Product personalization
- Pricing tier optimization
- Feature rollout planning
"""

from glyphh import GlyphhModel, Concept, EncoderConfig

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define User Profile Concepts
# =============================================================================

def create_user_profile(
    user_id: str,
    # Demographics
    company_size: str,  # "startup", "smb", "mid-market", "enterprise"
    industry: str,
    region: str,
    # Engagement metrics
    monthly_active_days: int,
    features_used: int,
    total_sessions: int,
    avg_session_minutes: float,
    # Value metrics
    monthly_spend: float,
    lifetime_value: float,
    account_age_months: int,
    # Behavior patterns
    primary_use_case: str,
    integration_count: int,
    team_members: int,
    api_calls_monthly: int,
):
    """Create a user profile concept for segmentation."""
    return Concept(
        name=f"user_{user_id}",
        attributes={
            "user_id": user_id,
            # Demographics
            "company_size": company_size,
            "industry": industry,
            "region": region,
            # Engagement
            "monthly_active_days": monthly_active_days,
            "features_used": features_used,
            "total_sessions": total_sessions,
            "avg_session_minutes": avg_session_minutes,
            # Value
            "monthly_spend": monthly_spend,
            "lifetime_value": lifetime_value,
            "account_age_months": account_age_months,
            # Behavior
            "primary_use_case": primary_use_case,
            "integration_count": integration_count,
            "team_members": team_members,
            "api_calls_monthly": api_calls_monthly,
            # Computed segments (for cortex similarity)
            "layer": company_size,
            "role": industry,
        }
    )

# =============================================================================
# Define Segment Archetypes
# =============================================================================

segment_archetypes = [
    Concept(
        name="power_user",
        attributes={
            "segment_name": "Power Users",
            "description": "High engagement, heavy feature usage, API-driven",
            "monthly_active_days_min": 20,
            "features_used_min": 15,
            "api_calls_monthly_min": 1000,
            "characteristics": ["high engagement", "technical", "API-heavy"]
        }
    ),
    Concept(
        name="casual_user",
        attributes={
            "segment_name": "Casual Users",
            "description": "Light usage, basic features, occasional login",
            "monthly_active_days_max": 5,
            "features_used_max": 5,
            "characteristics": ["low engagement", "basic needs", "price sensitive"]
        }
    ),
    Concept(
        name="enterprise_champion",
        attributes={
            "segment_name": "Enterprise Champions",
            "description": "Large teams, high spend, multiple integrations",
            "company_size": "enterprise",
            "team_members_min": 20,
            "integration_count_min": 5,
            "characteristics": ["high value", "complex needs", "expansion potential"]
        }
    ),
    Concept(
        name="growing_team",
        attributes={
            "segment_name": "Growing Teams",
            "description": "Expanding usage, adding team members, increasing spend",
            "company_size": "smb",
            "characteristics": ["growth trajectory", "upsell potential", "feature hungry"]
        }
    ),
    Concept(
        name="at_risk",
        attributes={
            "segment_name": "At Risk",
            "description": "Declining engagement, reduced usage",
            "monthly_active_days_max": 3,
            "characteristics": ["declining engagement", "churn risk", "needs attention"]
        }
    ),
]

print("Encoding segment archetypes...")
for segment in segment_archetypes:
    glyph = model.encode(segment)
    print(f"  ✓ {segment.name}: {segment.attributes['segment_name']}")

# =============================================================================
# Create Sample User Profiles
# =============================================================================

print("\nCreating user profiles...")

users = [
    # Power users
    create_user_profile(
        "U001", company_size="mid-market", industry="tech", region="west",
        monthly_active_days=25, features_used=18, total_sessions=150,
        avg_session_minutes=45, monthly_spend=500, lifetime_value=12000,
        account_age_months=24, primary_use_case="analytics",
        integration_count=8, team_members=12, api_calls_monthly=5000
    ),
    create_user_profile(
        "U002", company_size="startup", industry="fintech", region="east",
        monthly_active_days=28, features_used=20, total_sessions=200,
        avg_session_minutes=60, monthly_spend=200, lifetime_value=4800,
        account_age_months=18, primary_use_case="automation",
        integration_count=10, team_members=5, api_calls_monthly=8000
    ),
    # Casual users
    create_user_profile(
        "U003", company_size="smb", industry="retail", region="central",
        monthly_active_days=3, features_used=3, total_sessions=10,
        avg_session_minutes=15, monthly_spend=50, lifetime_value=600,
        account_age_months=12, primary_use_case="reporting",
        integration_count=1, team_members=2, api_calls_monthly=50
    ),
    # Enterprise champions
    create_user_profile(
        "U004", company_size="enterprise", industry="finance", region="east",
        monthly_active_days=22, features_used=15, total_sessions=300,
        avg_session_minutes=30, monthly_spend=5000, lifetime_value=180000,
        account_age_months=36, primary_use_case="compliance",
        integration_count=12, team_members=50, api_calls_monthly=20000
    ),
    # Growing teams
    create_user_profile(
        "U005", company_size="smb", industry="healthcare", region="west",
        monthly_active_days=18, features_used=12, total_sessions=80,
        avg_session_minutes=35, monthly_spend=300, lifetime_value=3600,
        account_age_months=12, primary_use_case="workflow",
        integration_count=4, team_members=8, api_calls_monthly=1500
    ),
    # At risk
    create_user_profile(
        "U006", company_size="startup", industry="media", region="west",
        monthly_active_days=2, features_used=2, total_sessions=5,
        avg_session_minutes=10, monthly_spend=100, lifetime_value=1800,
        account_age_months=18, primary_use_case="reporting",
        integration_count=0, team_members=3, api_calls_monthly=10
    ),
]

for user in users:
    glyph = model.encode(user)
    print(f"  ✓ {user.name}: {user.attributes['company_size']}/{user.attributes['industry']}")

# =============================================================================
# Segmentation Functions
# =============================================================================

def segment_user(user: Concept):
    """
    Assign a user to segments based on similarity to archetypes.
    
    Returns primary and secondary segment assignments with confidence.
    """
    print(f"\n{'='*60}")
    print(f"SEGMENTING USER: {user.name}")
    print('='*60)
    
    # Find similar segment archetypes
    results = model.similarity_search(user, top_k=3)
    
    segments = []
    for result in results:
        if "segment_name" in result.attributes:
            segments.append({
                "segment": result.attributes["segment_name"],
                "confidence": result.score,
                "characteristics": result.attributes.get("characteristics", [])
            })
    
    if segments:
        print(f"\nPrimary Segment: {segments[0]['segment']}")
        print(f"Confidence: {segments[0]['confidence']:.2f}")
        print(f"Characteristics: {', '.join(segments[0]['characteristics'])}")
        
        if len(segments) > 1:
            print(f"\nSecondary Segments:")
            for seg in segments[1:]:
                print(f"  • {seg['segment']} ({seg['confidence']:.2f})")
    
    return segments


def find_similar_users(user: Concept, top_k: int = 5):
    """
    Find users with similar profiles for cohort analysis.
    """
    print(f"\n{'='*60}")
    print(f"FINDING SIMILAR USERS TO: {user.name}")
    print('='*60)
    
    results = model.similarity_search(user, top_k=top_k + 1)
    
    similar = []
    for result in results:
        if result.concept != user.name and "user_id" in result.attributes:
            similar.append({
                "user_id": result.attributes["user_id"],
                "similarity": result.score,
                "company_size": result.attributes["company_size"],
                "industry": result.attributes["industry"]
            })
    
    print(f"\nSimilar Users:")
    for s in similar[:top_k]:
        print(f"  • {s['user_id']}: {s['similarity']:.2f}")
        print(f"    {s['company_size']} / {s['industry']}")
    
    return similar


def get_segment_members(segment_name: str):
    """
    Get all users belonging to a segment.
    """
    # Find the segment archetype
    segment_results = model.similarity_search(segment_name, top_k=1)
    
    if not segment_results:
        return []
    
    segment = segment_results[0]
    
    # Find users similar to this segment
    user_results = model.similarity_search(segment, top_k=20)
    
    members = []
    for result in user_results:
        if "user_id" in result.attributes:
            members.append({
                "user_id": result.attributes["user_id"],
                "fit_score": result.score
            })
    
    return members

# =============================================================================
# Test Segmentation
# =============================================================================

print("\n" + "="*60)
print("TESTING USER SEGMENTATION")
print("="*60)

# Segment each user
for user in users:
    segments = segment_user(user)

# Find similar users
print("\n" + "="*60)
print("COHORT ANALYSIS")
print("="*60)

find_similar_users(users[0])  # Find users similar to power user

# =============================================================================
# Segment Distribution Analysis
# =============================================================================

print("\n" + "="*60)
print("SEGMENT DISTRIBUTION")
print("="*60)

for archetype in segment_archetypes:
    members = get_segment_members(archetype.attributes["segment_name"])
    print(f"\n{archetype.attributes['segment_name']}:")
    print(f"  Members: {len(members)}")
    if members:
        avg_fit = sum(m["fit_score"] for m in members) / len(members)
        print(f"  Avg Fit Score: {avg_fit:.2f}")

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("user-segmentation.glyphh")
print("✓ Model exported to user-segmentation.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @user-segmentation.glyphh")

print("\nSegment user via API:")
print('  curl -X POST http://localhost:8000/api/v1/user-segmentation/segment \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"user_id": "U001"}\'')

print("\n" + "="*60)
print("KEY BENEFITS")
print("="*60)
print("""
1. DYNAMIC SEGMENTATION
   - Segments emerge from data similarity
   - No rigid rule-based classification
   
2. MULTI-DIMENSIONAL
   - Consider engagement, value, and behavior together
   - Find nuanced segment overlaps
   
3. ACTIONABLE INSIGHTS
   - Identify upsell opportunities
   - Target at-risk users proactively
   
4. COHORT DISCOVERY
   - Find similar users for A/B testing
   - Build lookalike audiences
""")
