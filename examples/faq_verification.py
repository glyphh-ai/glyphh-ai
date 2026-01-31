"""
FAQ Verification Example

Build an FAQ system where answers can't be wrong - every response is traced
to an approved source with full citation and confidence scoring.

Key Principle: "When your LLM can't afford to be wrong, sidecar it with Glyphh"

This example demonstrates:
1. Creating FAQ concepts with approval metadata
2. Deterministic answer matching using HDC similarity
3. Citation tracking (who approved, when, source)
4. Confidence-based escalation when no confident match
5. Audit trail for compliance

Use Cases:
- Customer support FAQs (legal/compliance requirements)
- Medical information systems (can't give wrong advice)
- Financial services (regulatory requirements)
- HR policy questions (must cite official policy)
"""

from glyphh import GlyphhModel, Concept, EncoderConfig
from glyphh import IntentEncoder, IntentPattern
from datetime import datetime

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define FAQ Concepts with Approval Metadata
# =============================================================================
# Each FAQ has:
# - question: The canonical question
# - answer: The approved answer
# - approved_by: Who approved this answer
# - approved_date: When it was approved
# - source: Official source document
# - category: For filtering/routing

faqs = [
    Concept(
        name="return_policy",
        attributes={
            "question": "What is your return policy?",
            "answer": "Items can be returned within 30 days of purchase with original receipt. Refunds are processed within 5-7 business days.",
            "approved_by": "Legal Team",
            "approved_date": "2025-01-15",
            "source": "Customer Policy Manual v2.3, Section 4.1",
            "category": "returns",
            "keywords": "return refund exchange policy days receipt"
        }
    ),
    Concept(
        name="shipping_times",
        attributes={
            "question": "How long does shipping take?",
            "answer": "Standard shipping: 5-7 business days. Express shipping: 2-3 business days. Overnight: Next business day by 5pm.",
            "approved_by": "Operations Team",
            "approved_date": "2025-01-10",
            "source": "Shipping Guidelines v1.8",
            "category": "shipping",
            "keywords": "shipping delivery time days express overnight standard"
        }
    ),
    Concept(
        name="warranty_coverage",
        attributes={
            "question": "What does the warranty cover?",
            "answer": "Our standard warranty covers manufacturing defects for 1 year from purchase date. It does not cover damage from misuse, accidents, or normal wear.",
            "approved_by": "Legal Team",
            "approved_date": "2025-01-12",
            "source": "Warranty Terms v3.0, Section 2",
            "category": "warranty",
            "keywords": "warranty coverage defect year damage repair replace"
        }
    ),
    Concept(
        name="payment_methods",
        attributes={
            "question": "What payment methods do you accept?",
            "answer": "We accept Visa, Mastercard, American Express, Discover, PayPal, and Apple Pay. All transactions are encrypted and PCI-compliant.",
            "approved_by": "Finance Team",
            "approved_date": "2025-01-08",
            "source": "Payment Processing Policy v2.1",
            "category": "payment",
            "keywords": "payment credit card visa mastercard paypal apple pay"
        }
    ),
    Concept(
        name="account_deletion",
        attributes={
            "question": "How do I delete my account?",
            "answer": "To delete your account, go to Settings > Privacy > Delete Account. Your data will be permanently removed within 30 days per GDPR requirements.",
            "approved_by": "Privacy Officer",
            "approved_date": "2025-01-20",
            "source": "Privacy Policy v4.2, Section 7.3",
            "category": "privacy",
            "keywords": "delete account remove data privacy gdpr"
        }
    ),
    Concept(
        name="price_match",
        attributes={
            "question": "Do you offer price matching?",
            "answer": "Yes, we match prices from authorized retailers within 14 days of purchase. Bring proof of the lower price to any store or contact support.",
            "approved_by": "Sales Team",
            "approved_date": "2025-01-18",
            "source": "Price Match Policy v1.2",
            "category": "pricing",
            "keywords": "price match guarantee lower competitor"
        }
    ),
]

# Encode FAQs
print("Encoding FAQ concepts...")
for faq in faqs:
    glyph = model.encode(faq)
    print(f"  ✓ {faq.name}: {faq.attributes['question'][:50]}...")

# =============================================================================
# Set up Intent Patterns for FAQ Queries
# =============================================================================

intent_encoder = IntentEncoder(config)

# Pattern for FAQ lookup
intent_encoder.add_pattern(IntentPattern(
    intent_type="faq_lookup",
    example_phrases=[
        "what is",
        "how do i",
        "how long",
        "do you",
        "can i",
        "what does",
        "where can",
        "when will",
    ],
    query_template={
        "operation": "similarity_search",
        "entity_type": "faq",
        "top_k": 3
    }
))

model.intent_encoder = intent_encoder

# =============================================================================
# FAQ Query Function with Verification
# =============================================================================

def query_faq(question: str, confidence_threshold: float = 0.75):
    """
    Query the FAQ system with full verification and citation.
    
    Returns:
    - answer: The approved answer (or escalation message)
    - confidence: How confident we are in the match
    - citation: Full source citation
    - escalate: Whether to escalate to human
    """
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print('='*60)
    
    # Search for matching FAQs
    results = model.similarity_search(question, top_k=3)
    
    if not results:
        return {
            "answer": None,
            "confidence": 0.0,
            "citation": None,
            "escalate": True,
            "reason": "No matching FAQs found"
        }
    
    top_match = results[0]
    
    # Check confidence threshold
    if top_match.score < confidence_threshold:
        print(f"\n⚠️  Low confidence match ({top_match.score:.2f} < {confidence_threshold})")
        print(f"   Best match: {top_match.concept}")
        print(f"   → Escalating to human agent")
        return {
            "answer": None,
            "confidence": top_match.score,
            "citation": None,
            "escalate": True,
            "reason": f"Confidence {top_match.score:.2f} below threshold {confidence_threshold}"
        }
    
    # High confidence - return verified answer
    faq = top_match.attributes
    
    print(f"\n✓ Matched: {top_match.concept} (confidence: {top_match.score:.2f})")
    print(f"\nAnswer:")
    print(f"  {faq['answer']}")
    print(f"\nCitation:")
    print(f"  Source: {faq['source']}")
    print(f"  Approved by: {faq['approved_by']}")
    print(f"  Approved date: {faq['approved_date']}")
    
    return {
        "answer": faq['answer'],
        "confidence": top_match.score,
        "citation": {
            "source": faq['source'],
            "approved_by": faq['approved_by'],
            "approved_date": faq['approved_date'],
            "canonical_question": faq['question']
        },
        "escalate": False,
        "reason": None
    }

# =============================================================================
# Test FAQ Queries
# =============================================================================

print("\n" + "="*60)
print("TESTING FAQ VERIFICATION SYSTEM")
print("="*60)

# Test queries - some should match, some should escalate
test_queries = [
    # Should match with high confidence
    "What's your return policy?",
    "How long does shipping take?",
    "What payment methods do you accept?",
    
    # Should match but different phrasing
    "Can I get a refund?",
    "Do you take credit cards?",
    
    # Should escalate - no confident match
    "What's the CEO's email address?",
    "Can I get a discount for bulk orders?",
]

for query in test_queries:
    result = query_faq(query)

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("faq-model.glyphh")
print("✓ Model exported to faq-model.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @faq-model.glyphh")

print("\nQuery via API:")
print('  curl -X POST http://localhost:8000/api/v1/faq-model/query \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"query": "What is your return policy?"}\'')

print("\n" + "="*60)
print("KEY BENEFITS")
print("="*60)
print("""
1. DETERMINISTIC: Same question always gets same answer
2. TRACEABLE: Every answer has full citation and approval chain
3. AUDITABLE: Know who approved what and when
4. SAFE: Low-confidence matches escalate to humans
5. COMPLIANT: Meets regulatory requirements for accuracy

When your LLM can't afford to be wrong, sidecar it with Glyphh.
""")
