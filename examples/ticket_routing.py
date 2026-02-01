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

from glyphh import (
    Encoder, EncoderConfig, Concept, GlyphhModel,
    SimilarityCalculator, LayerConfig, SegmentConfig, Role,
    IntentEncoder, IntentPattern
)

# Configure encoder with explicit structure
config = EncoderConfig(
    dimension=10000,
    seed=42,
    layers=[
        LayerConfig(
            name="ticket",
            similarity_weight=1.0,
            segments=[
                SegmentConfig(
                    name="classification",
                    roles=[
                        Role(name="category", similarity_weight=1.0),
                        Role(name="team", similarity_weight=0.8),
                        Role(name="priority", similarity_weight=0.9),
                        Role(name="keywords", similarity_weight=0.7),
                        Role(name="description", similarity_weight=0.6),
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
print("\nEncoding support categories...")
category_glyphs = {}
for category in categories:
    glyph = encoder.encode(category)
    category_glyphs[category.name] = (category, glyph)
    print(f"  ✓ {category.name} → {category.attributes['team']}")

# =============================================================================
# Define Historical Tickets for Pattern Learning
# =============================================================================

historical_tickets = [
    Concept(
        name="ticket_001",
        attributes={
            "category": "account",
            "team": "Account Services",
            "priority": "high",
            "keywords": "login password",
            "description": "Can't log into my account - password is wrong"
        }
    ),
    Concept(
        name="ticket_002",
        attributes={
            "category": "billing",
            "team": "Finance Support",
            "priority": "medium",
            "keywords": "charged twice subscription",
            "description": "Double charged on credit card for monthly subscription"
        }
    ),
    Concept(
        name="ticket_003",
        attributes={
            "category": "technical",
            "team": "Technical Support",
            "priority": "high",
            "keywords": "crash export error",
            "description": "App crashes when clicking export button"
        }
    ),
    Concept(
        name="ticket_004",
        attributes={
            "category": "product",
            "team": "Product Team",
            "priority": "low",
            "keywords": "feature dark mode",
            "description": "Would love to see dark mode option"
        }
    ),
    Concept(
        name="ticket_005",
        attributes={
            "category": "retention",
            "team": "Retention Team",
            "priority": "urgent",
            "keywords": "cancel subscription",
            "description": "Want to cancel my subscription immediately"
        }
    ),
]

print("\nEncoding historical tickets...")
ticket_glyphs = {}
for ticket in historical_tickets:
    glyph = encoder.encode(ticket)
    ticket_glyphs[ticket.name] = (ticket, glyph)
    print(f"  ✓ {ticket.name}: {ticket.attributes['description'][:40]}...")

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

# =============================================================================
# Ticket Routing Function
# =============================================================================

def route_ticket(subject: str, body: str, confidence_threshold: float = 0.7):
    """
    Route a support ticket to the appropriate team.
    
    Uses intent matching first, then falls back to similarity search
    against historical tickets and category definitions.
    """
    ticket_text = f"{subject} {body}"
    
    print(f"\n{'='*60}")
    print(f"ROUTING TICKET")
    print(f"Subject: {subject}")
    print('='*60)
    
    # Try intent matching first
    intent_match = intent_encoder.match_intent(ticket_text)
    
    if intent_match and intent_match.confidence > confidence_threshold:
        template = intent_match.structured_query
        print(f"\n✓ Intent Match: {intent_match.intent_type}")
        print(f"  Confidence: {intent_match.confidence:.2f}")
        
        return {
            "team": template.get("team", "Triage Queue"),
            "category": template.get("category", "unknown"),
            "priority": template.get("priority", "medium"),
            "sla_hours": 24,
            "confidence": intent_match.confidence,
            "match_method": "intent",
            "similar_tickets": []
        }
    
    # Fall back to similarity search
    print("\n? No strong intent match, using similarity search...")
    
    # Create a ticket concept for similarity matching
    ticket_concept = Concept(
        name="incoming_ticket",
        attributes={
            "category": "unknown",
            "team": "unknown",
            "priority": "medium",
            "keywords": ticket_text,
            "description": ticket_text
        }
    )
    ticket_glyph = encoder.encode(ticket_concept)
    
    # Find most similar category
    best_match = None
    best_score = 0
    for cat_name, (cat_concept, cat_glyph) in category_glyphs.items():
        result = calculator.compute_similarity(
            ticket_glyph, cat_glyph,
            edge_type="neural_cortex"
        )
        if result.score > best_score:
            best_score = result.score
            best_match = cat_concept
    
    if best_match and best_score >= confidence_threshold:
        attrs = best_match.attributes
        print(f"\n✓ Category Match: {best_match.name}")
        print(f"  Confidence: {best_score:.2f}")
        
        return {
            "team": attrs.get("team"),
            "category": attrs.get("category"),
            "priority": attrs.get("priority"),
            "sla_hours": attrs.get("sla_hours"),
            "confidence": best_score,
            "match_method": "similarity",
            "similar_tickets": []
        }
    
    # Low confidence - escalate to human
    print("\n⚠️  Low confidence - escalating to human triage")
    return {
        "team": "Triage Queue",
        "category": "unknown",
        "priority": "medium",
        "sla_hours": 24,
        "confidence": best_score if best_match else 0,
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
# Package and Export Model
# =============================================================================

print("\n" + "="*60)
print("PACKAGING MODEL")
print("="*60)

# Collect all glyphs
all_glyphs = [glyph for _, glyph in category_glyphs.values()]
all_glyphs.extend([glyph for _, glyph in ticket_glyphs.values()])

model = GlyphhModel(
    name="ticket-routing",
    version="1.0.0",
    encoder_config=config,
    glyphs=all_glyphs,
    metadata={
        "domain": "support",
        "description": "Support ticket routing model",
        "num_categories": len(categories),
        "num_historical_tickets": len(historical_tickets)
    }
)

model.to_file("ticket-routing.glyphh")
print("✓ Model exported to ticket-routing.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @ticket-routing.glyphh")

print("\nRoute ticket via API:")
print('  curl -X POST http://localhost:8000/api/v1/ticket-routing/route \\')
print('    -H "Content-Type: application/json" \\')
print("    -d '{\"subject\": \"Cannot log in\", \"body\": \"Password not working\"}'")

# Cleanup
import os
if os.path.exists("ticket-routing.glyphh"):
    os.remove("ticket-routing.glyphh")
