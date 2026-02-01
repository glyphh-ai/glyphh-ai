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

from glyphh import (
    Encoder, EncoderConfig, Concept, GlyphhModel,
    SimilarityCalculator, LayerConfig, SegmentConfig, Role
)

# Configure encoder with FAQ-specific structure
config = EncoderConfig(
    dimension=10000,
    seed=42,
    layers=[
        LayerConfig(
            name="content",
            similarity_weight=1.0,
            segments=[
                SegmentConfig(
                    name="faq",
                    roles=[
                        Role(name="question", similarity_weight=1.0),
                        Role(name="answer", similarity_weight=0.8),
                        Role(name="category", similarity_weight=0.6),
                        Role(name="keywords", similarity_weight=0.9),
                    ]
                )
            ]
        ),
        LayerConfig(
            name="metadata",
            similarity_weight=0.2,
            segments=[
                SegmentConfig(
                    name="approval",
                    roles=[
                        Role(name="approved_by"),
                        Role(name="source"),
                    ]
                )
            ]
        )
    ]
)

# Create encoder
encoder = Encoder(config)
calculator = SimilarityCalculator()

# =============================================================================
# Define FAQ Concepts with Approval Metadata
# =============================================================================

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
glyphs = []
faq_data = {}  # Store FAQ data for lookup
for faq in faqs:
    glyph = encoder.encode(faq)
    glyphs.append(glyph)
    faq_data[glyph.name] = faq.attributes
    print(f"  ✓ {faq.name}: {faq.attributes['question'][:50]}...")

# =============================================================================
# FAQ Query Function with Verification
# =============================================================================

def query_faq(question: str, confidence_threshold: float = 0.3):
    """
    Query the FAQ system with full verification and citation.
    """
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print('='*60)
    
    # Encode the query as a concept
    query_concept = Concept(
        name="query",
        attributes={
            "question": question,
            "answer": "",
            "category": "",
            "keywords": question,
        }
    )
    query_glyph = encoder.encode(query_concept)
    
    # Find best matching FAQ
    best_match = None
    best_score = 0.0
    
    for glyph in glyphs:
        result = calculator.compute_similarity(
            query_glyph, glyph,
            edge_type="neural_cortex"
        )
        if result.score > best_score:
            best_score = result.score
            best_match = glyph
    
    if best_match is None or best_score < confidence_threshold:
        print(f"\n⚠️  Low confidence match ({best_score:.2f} < {confidence_threshold})")
        print(f"   → Escalating to human agent")
        return {
            "answer": None,
            "confidence": best_score,
            "escalate": True,
        }
    
    # High confidence - return verified answer
    faq = faq_data[best_match.name]
    
    print(f"\n✓ Matched: {best_match.name} (confidence: {best_score:.2f})")
    print(f"\nAnswer:")
    print(f"  {faq['answer']}")
    print(f"\nCitation:")
    print(f"  Source: {faq['source']}")
    print(f"  Approved by: {faq['approved_by']}")
    print(f"  Approved date: {faq['approved_date']}")
    
    return {
        "answer": faq['answer'],
        "confidence": best_score,
        "citation": {
            "source": faq['source'],
            "approved_by": faq['approved_by'],
            "approved_date": faq['approved_date'],
        },
        "escalate": False,
    }

# =============================================================================
# Test FAQ Queries
# =============================================================================

print("\n" + "="*60)
print("TESTING FAQ VERIFICATION SYSTEM")
print("="*60)

test_queries = [
    "What's your return policy?",
    "How long does shipping take?",
    "What payment methods do you accept?",
    "Can I get a refund?",
]

for query in test_queries:
    result = query_faq(query)

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model = GlyphhModel(
    name="faq-model",
    version="1.0.0",
    encoder_config=config,
    glyphs=glyphs,
    metadata={
        "domain": "customer_support",
        "description": "FAQ verification model with citations",
    }
)

model.to_file("faq-model.glyphh")
print("✓ Model exported to faq-model.glyphh")

print("\nDeploy to runtime:")
print("  glyphh runtime deploy faq-model.glyphh")

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

# Cleanup
import os
if os.path.exists("faq-model.glyphh"):
    os.remove("faq-model.glyphh")
