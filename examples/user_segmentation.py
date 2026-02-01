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
            name="user_profile",
            similarity_weight=1.0,
            segments=[
                SegmentConfig(
                    name="demographics",
                    roles=[
                        Role(name="company_size", similarity_weight=0.8),
                        Role(name="industry", similarity_weight=0.7),
                        Role(name="region", similarity_weight=0.5),
                    ]
                ),
                SegmentConfig(
                    name="engagement",
                    roles=[
                        Role(name="monthly_active_days", similarity_weight=1.0),
                        Role(name="features_used", similarity_weight=0.9),
                        Role(name="api_calls_monthly", similarity_weight=0.8),
                    ]
                ),
                SegmentConfig(
                    name="value",
                    roles=[
                        Role(name="monthly_spend", similarity_weight=1.0),
                        Role(name="lifetime_value", similarity_weight=0.9),
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
# Define User Profile Concepts
# =============================================================================

def create_user_profile(
    user_id: str,
    company_size: str,
    industry: str,
    region: str,
    monthly_active_days: int,
    features_used: int,
    total_sessions: int,
    avg_session_minutes: float,
    monthly_spend: float,
    lifetime_value: float,
    account_age_months: int,
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
            "company_size": company_size,
            "industry": industry,
            "region": region,
            "monthly_active_days": str(monthly_active_days),
            "features_used": str(features_used),
            "total_sessions": str(total_sessions),
            "avg_session_minutes": str(avg_session_minutes),
            "monthly_spend": str(monthly_spend),
            "lifetime_value": str(lifetime_value),
            "account_age_months": str(account_age_months),
            "primary_use_case": primary_use_case,
            "integration_count": str(integration_count),
            "team_members": str(team_members),
            "api_calls_monthly": str(api_calls_monthly),
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
            "monthly_active_days": "high",
            "features_used": "high",
            "api_calls_monthly": "high",
            "characteristics": "high engagement, technical, API-heavy"
        }
    ),
    Concept(
        name="casual_user",
        attributes={
            "segment_name": "Casual Users",
            "description": "Light usage, basic features, occasional login",
            "monthly_active_days": "low",
            "features_used": "low",
            "characteristics": "low engagement, basic needs, price sensitive"
        }
    ),
    Concept(
        name="enterprise_champion",
        attributes={
            "segment_name": "Enterprise Champions",
            "description": "Large teams, high spend, multiple integrations",
            "company_size": "enterprise",
            "team_members": "high",
            "integration_count": "high",
            "characteristics": "high value, complex needs, expansion potential"
        }
    ),
    Concept(
        name="growing_team",
        attributes={
            "segment_name": "Growing Teams",
            "description": "Expanding usage, adding team members, increasing spend",
            "company_size": "smb",
            "characteristics": "growth trajectory, upsell potential, feature hungry"
        }
    ),
    Concept(
        name="at_risk",
        attributes={
            "segment_name": "At Risk",
            "description": "Declining engagement, reduced usage",
            "monthly_active_days": "very_low",
            "characteristics": "declining engagement, churn risk, needs attention"
        }
    ),
]

print("Encoding segment archetypes...")
segment_glyphs = {}
for segment in segment_archetypes:
    glyph = encoder.encode(segment)
    segment_glyphs[segment.name] = (segment, glyph)
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

user_glyphs = {}
for user in users:
    glyph = encoder.encode(user)
    user_glyphs[user.name] = (user, glyph)
    print(f"  ✓ {user.name}: {user.attributes['company_size']}/{user.attributes['industry']}")

# =============================================================================
# Segmentation Functions
# =============================================================================

def segment_user(user: Concept, user_glyph):
    """
    Assign a user to segments based on similarity to archetypes.
    
    Returns primary and secondary segment assignments with confidence.
    """
    print(f"\n{'='*60}")
    print(f"SEGMENTING USER: {user.name}")
    print('='*60)
    
    # Find similar segment archetypes
    segments = []
    for seg_name, (seg_concept, seg_glyph) in segment_glyphs.items():
        result = calculator.compute_similarity(
            user_glyph, seg_glyph,
            edge_type="neural_cortex"
        )
        if "segment_name" in seg_concept.attributes:
            segments.append({
                "segment": seg_concept.attributes["segment_name"],
                "confidence": result.score,
                "characteristics": seg_concept.attributes.get("characteristics", "")
            })
    
    # Sort by confidence
    segments.sort(key=lambda x: x["confidence"], reverse=True)
    
    if segments:
        print(f"\nPrimary Segment: {segments[0]['segment']}")
        print(f"Confidence: {segments[0]['confidence']:.2f}")
        print(f"Characteristics: {segments[0]['characteristics']}")
        
        if len(segments) > 1:
            print(f"\nSecondary Segments:")
            for seg in segments[1:3]:
                print(f"  • {seg['segment']} ({seg['confidence']:.2f})")
    
    return segments


def find_similar_users(user: Concept, user_glyph, top_k: int = 5):
    """
    Find users with similar profiles for cohort analysis.
    """
    print(f"\n{'='*60}")
    print(f"FINDING SIMILAR USERS TO: {user.name}")
    print('='*60)
    
    similar = []
    for name, (u_concept, u_glyph) in user_glyphs.items():
        if name != user.name and "user_id" in u_concept.attributes:
            result = calculator.compute_similarity(
                user_glyph, u_glyph,
                edge_type="neural_cortex"
            )
            similar.append({
                "user_id": u_concept.attributes["user_id"],
                "similarity": result.score,
                "company_size": u_concept.attributes["company_size"],
                "industry": u_concept.attributes["industry"]
            })
    
    similar.sort(key=lambda x: x["similarity"], reverse=True)
    
    print(f"\nSimilar Users:")
    for s in similar[:top_k]:
        print(f"  • {s['user_id']}: {s['similarity']:.2f}")
        print(f"    {s['company_size']} / {s['industry']}")
    
    return similar[:top_k]


def get_segment_members(segment_name: str):
    """
    Get all users belonging to a segment.
    """
    # Find the segment archetype
    segment_concept = None
    segment_glyph = None
    for name, (concept, glyph) in segment_glyphs.items():
        if concept.attributes.get("segment_name") == segment_name:
            segment_concept = concept
            segment_glyph = glyph
            break
    
    if not segment_concept:
        return []
    
    # Find users similar to this segment
    members = []
    for name, (user, user_glyph) in user_glyphs.items():
        if "user_id" in user.attributes:
            result = calculator.compute_similarity(
                user_glyph, segment_glyph,
                edge_type="neural_cortex"
            )
            members.append({
                "user_id": user.attributes["user_id"],
                "fit_score": result.score
            })
    
    members.sort(key=lambda x: x["fit_score"], reverse=True)
    return members

# =============================================================================
# Test Segmentation
# =============================================================================

print("\n" + "="*60)
print("TESTING USER SEGMENTATION")
print("="*60)

# Segment each user
for user in users:
    glyph = user_glyphs[user.name][1]
    segments = segment_user(user, glyph)

# Find similar users
print("\n" + "="*60)
print("COHORT ANALYSIS")
print("="*60)

user_0 = users[0]
glyph_0 = user_glyphs[user_0.name][1]
find_similar_users(user_0, glyph_0)

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
# Package and Export Model
# =============================================================================

print("\n" + "="*60)
print("PACKAGING MODEL")
print("="*60)

# Collect all glyphs
all_glyphs = [glyph for _, glyph in segment_glyphs.values()]
all_glyphs.extend([glyph for _, glyph in user_glyphs.values()])

model = GlyphhModel(
    name="user-segmentation",
    version="1.0.0",
    encoder_config=config,
    glyphs=all_glyphs,
    metadata={
        "domain": "marketing",
        "description": "User segmentation model",
        "num_segments": len(segment_archetypes),
        "num_users": len(users)
    }
)

model.to_file("user-segmentation.glyphh")
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

# Cleanup
import os
if os.path.exists("user-segmentation.glyphh"):
    os.remove("user-segmentation.glyphh")
