"""
Support Ticket Routing Example

Automatically route support tickets to the right team based on content
analysis using similarity search and intent pattern matching.

Key Principle: Route tickets deterministically based on learned patterns,
not keyword matching. The model understands context and intent.

This example demonstrates:
1. Creating ticket category concepts with team assignments
2. Intent pattern matching for ticket classification
3. Similarity search to find related past tickets
4. Confidence-based routing with escalation

Use Cases:
- Help desk ticket triage
- Customer support automation
- IT service management
- Internal request routing
"""

from glyphh import GlyphhModel, Concept, EncoderConfig
from glyphh import IntentEncoder, IntentPattern

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Support Categories with Team Assignments
# =============================================================================

categories = [
    Concept(
        name="billing_issues",
        attributes={
            "category": "billing",
            "team": "Finance Support",
            "priority": "medium",
            "sla_hours": 24,
            "keywords": "invoice payment charge refund subscription",
            "description": "Issues related to billing, payments, and subscriptions"
        }
    ),
    Concept(
        name="technical_support",
        attributes={
            "category": "technical",
            "team": "Technical Support",
            "priority": "high",
            "sla_hours": 4,
            "keywords": "error bug crash not working broken",
            "description": "Technical issues requiring engineering support"
        }
    ),
    Concept(
        name="account_access",
        attributes={
            "category": "account",
            "team": "Account Services",
            "priority": "high",
            "sla_hours": 2,
            "keywords": "login password reset locked access denied",
            "description": "Account access and authentication issues"
        }
    ),
    Concept(
        name="feature_request",
        attributes={
            "category": "product",
            "team": "Product Team",
            "priority": "low",
            "sla_hours": 72,
            "keywords": "feature request suggestion improvement wish",
            "description": "Feature requests and product suggestions"
        }
    ),
    Concept(
        name="general_inquiry",
        attributes={
            "category": "general",
            "team": "Customer Success",
            "priority": "medium",
            "sla_hours": 24,
            "keywords": "question how to help information",
            "description": "General questions and information requests"
        }
    ),
    Concept(
        name="cancellation",
        attributes={
            "category": "retention",
            "team": "Retention Team",
            "priority": "urgent",
            "sla_hours": 1,
            "keywords": "cancel subscription end terminate close account",
            "description": "Cancellation requests requiring retention intervention"
        }
    ),
]

# Encode categories
print("Encoding support categories...")
for category in categories:
    glyph = model.encode(category)
    print(f"  ✓ {category.name} → {category.attributes['team']}")

# =============================================================================
# Define Historical Tickets for Pattern Learning
# =============================================================================

historical_tickets = [
    Concept(
        name="ticket_001",
        attributes={
            "subject": "Can't log into my account",
            "body": "I've been trying to log in but it says my password is wrong",
            "resolved_category": "account",
            "resolution_time_hours": 1.5
        }
    ),
    Concept(
        name="ticket_002",
        attributes={
            "subject": "Double charged on my credit card",
            "body": "I was charged twice for my monthly subscription",
            "resolved_category": "billing",
            "resolution_time_hours": 12
        }
    ),
    Concept(
        name="ticket_003",
        attributes={
            "subject": "App crashes when I click export",
            "body": "Every time I try to export my data the application crashes",
            "resolved_category": "technical",
            "resolution_time_hours": 6
        }
    ),
    Concept(
        name="ticket_004",
        attributes={
            "subject": "Would love to see dark mode",
            "body": "It would be great if you could add a dark mode option",
            "resolved_category": "product",
            "resolution_time_hours": 0
        }
    ),
    Concept(
        name="ticket_005",
        attributes={
            "subject": "I want to cancel my subscription",
            "body": "Please cancel my account effective immediately",
            "resolved_category": "retention",
            "resolution_time_hours": 0.5
        }
    ),
]

print("\nEncoding historical tickets...")
for ticket in historical_tickets:
    glyph = model.encode(ticket)
    print(f"  ✓ {ticket.name}: {ticket.attributes['subject'][:40]}...")

# =============================================================================
# Set up Intent Patterns for Ticket Classification
# =============================================================================

intent_encoder = IntentEncoder(config)

intent_encoder.add_pattern(IntentPattern(
    intent_type="billing_issue",
    example_phrases=[
        "charged twice",
        "wrong amount",
        "refund request",
        "invoice problem",
        "payment failed",
        "subscription charge",
    ],
    query_template={
        "operation": "route",
        "category": "billing",
        "team": "Finance Support"
    }
))

intent_encoder.add_pattern(IntentPattern(
    intent_type="access_issue",
    example_phrases=[
        "can't log in",
        "password not working",
        "account locked",
        "reset password",
        "access denied",
        "forgot password",
    ],
    query_template={
        "operation": "route",
        "category": "account",
        "team": "Account Services"
    }
))

intent_encoder.add_pattern(IntentPattern(
    intent_type="technical_issue",
    example_phrases=[
        "not working",
        "error message",
        "app crashes",
        "bug found",
        "broken feature",
        "doesn't load",
    ],
    query_template={
        "operation": "route",
        "category": "technical",
        "team": "Technical Support"
    }
))

intent_encoder.add_pattern(IntentPattern(
    intent_type="cancellation_request",
    example_phrases=[
        "cancel subscription",
        "close account",
        "stop billing",
        "end service",
        "terminate account",
        "unsubscribe",
    ],
    query_template={
        "operation": "route",
        "category": "retention",
        "team": "Retention Team",
        "priority": "urgent"
    }
))

model.intent_encoder = intent_encoder

# =============================================================================
# Ticket Routing Function
# =============================================================================

def route_ticket(subject: str, body: str, confidence_threshold: float = 0.7):
    """
    Route a support ticket to the appropriate team.
    
    Uses intent matching first, then falls back to similarity search
    against historical tickets and category definitions.
    
    Returns:
    - team: Assigned team
    - category: Ticket category
    - priority: Priority level
    - sla_hours: SLA in hours
    - confidence: Routing confidence
    - similar_tickets: Related historical tickets
    """
    ticket_text = f"{subject} {body}"
    
    print(f"\n{'='*60}")
    print(f"ROUTING TICKET")
    print(f"Subject: {subject}")
    print('='*60)
    
    # Try intent matching first
    intent_match = model.intent_encoder.match_intent(ticket_text)
    
    if intent_match.is_high_confidence():
        template = intent_match.structured_query
        print(f"\n✓ Intent Match: {intent_match.intent_type}")
        print(f"  Confidence: {intent_match.confidence:.2f}")
        
        # Get full category details
        category_results = model.similarity_search(
            template.get("category", ""),
            top_k=1,
            filters={"category": template.get("category")}
        )
        
        if category_results:
            cat = category_results[0].attributes
            return {
                "team": cat.get("team", template.get("team")),
                "category": cat.get("category"),
                "priority": template.get("priority", cat.get("priority")),
                "sla_hours": cat.get("sla_hours"),
                "confidence": intent_match.confidence,
                "match_method": "intent",
                "similar_tickets": []
            }
    
    # Fall back to similarity search
    print("\n? No strong intent match, using similarity search...")
    
    # Search against categories
    category_results = model.similarity_search(ticket_text, top_k=3)
    
    if category_results and category_results[0].score >= confidence_threshold:
        top_match = category_results[0]
        attrs = top_match.attributes
        
        print(f"\n✓ Category Match: {top_match.concept}")
        print(f"  Confidence: {top_match.score:.2f}")
        
        # Find similar historical tickets
        similar = model.similarity_search(
            ticket_text,
            top_k=3,
            filters={"resolved_category": attrs.get("category")}
        )
        
        return {
            "team": attrs.get("team"),
            "category": attrs.get("category"),
            "priority": attrs.get("priority"),
            "sla_hours": attrs.get("sla_hours"),
            "confidence": top_match.score,
            "match_method": "similarity",
            "similar_tickets": [s.concept for s in similar[:3]]
        }
    
    # Low confidence - escalate to human
    print("\n⚠️  Low confidence - escalating to human triage")
    return {
        "team": "Triage Queue",
        "category": "unknown",
        "priority": "medium",
        "sla_hours": 24,
        "confidence": category_results[0].score if category_results else 0,
        "match_method": "escalation",
        "similar_tickets": []
    }

# =============================================================================
# Test Ticket Routing
# =============================================================================

print("\n" + "="*60)
print("TESTING TICKET ROUTING")
print("="*60)

test_tickets = [
    {
        "subject": "I keep getting charged but I cancelled",
        "body": "I cancelled my subscription last month but I'm still being charged"
    },
    {
        "subject": "Application freezes on startup",
        "body": "When I open the app it just shows a white screen and freezes"
    },
    {
        "subject": "Need to reset my password",
        "body": "I forgot my password and the reset email isn't coming through"
    },
    {
        "subject": "Please cancel my account",
        "body": "I no longer need the service, please close my account"
    },
    {
        "subject": "Question about enterprise pricing",
        "body": "We're interested in upgrading to enterprise, what are the options?"
    },
]

for ticket in test_tickets:
    result = route_ticket(ticket["subject"], ticket["body"])
    print(f"\n  → Routed to: {result['team']}")
    print(f"  → Category: {result['category']}")
    print(f"  → Priority: {result['priority']}")
    print(f"  → SLA: {result['sla_hours']} hours")

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("ticket-routing.glyphh")
print("✓ Model exported to ticket-routing.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @ticket-routing.glyphh")

print("\nRoute ticket via API:")
print('  curl -X POST http://localhost:8000/api/v1/ticket-routing/route \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"subject": "Can\\'t log in", "body": "Password not working"}\'')
