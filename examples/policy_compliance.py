"""
Policy Compliance Example

Verify that actions, content, or decisions comply with organizational
policies using fact trees and similarity search.

Key Principle: Every compliance check returns a traceable decision
with citations to specific policy sections.

This example demonstrates:
1. Creating policy concepts with hierarchical structure
2. Fact trees for policy relationship navigation
3. Similarity search for finding applicable policies
4. Compliance verification with audit trails

Use Cases:
- Content moderation compliance
- HR policy verification
- Financial regulation checks
- Data handling compliance
"""

from glyphh import GlyphhModel, Concept, EncoderConfig

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Policy Hierarchy
# =============================================================================

# Top-level policy domains
policy_domains = [
    Concept(
        name="data_privacy",
        attributes={
            "domain": "Data Privacy",
            "description": "Policies governing personal data handling",
            "regulations": ["GDPR", "CCPA", "HIPAA"],
            "owner": "Privacy Officer",
            "last_updated": "2025-01-15",
            "version": "3.0"
        }
    ),
    Concept(
        name="information_security",
        attributes={
            "domain": "Information Security",
            "description": "Policies for protecting company information",
            "regulations": ["SOC2", "ISO27001"],
            "owner": "CISO",
            "last_updated": "2025-01-10",
            "version": "2.5"
        }
    ),
    Concept(
        name="acceptable_use",
        attributes={
            "domain": "Acceptable Use",
            "description": "Policies for appropriate use of company resources",
            "regulations": [],
            "owner": "HR Director",
            "last_updated": "2024-12-01",
            "version": "4.0"
        }
    ),
    Concept(
        name="financial_controls",
        attributes={
            "domain": "Financial Controls",
            "description": "Policies for financial transactions and approvals",
            "regulations": ["SOX", "GAAP"],
            "owner": "CFO",
            "last_updated": "2025-01-20",
            "version": "2.0"
        }
    ),
]

print("Encoding policy domains...")
for domain in policy_domains:
    glyph = model.encode(domain)
    print(f"  ✓ {domain.name}: {domain.attributes['domain']}")

# =============================================================================
# Define Specific Policy Rules
# =============================================================================

policy_rules = [
    # Data Privacy Rules
    Concept(
        name="pii_collection",
        attributes={
            "rule_id": "DP-001",
            "domain": "data_privacy",
            "title": "PII Collection Requirements",
            "description": "Personal data may only be collected with explicit consent",
            "requirements": [
                "Obtain explicit consent before collection",
                "Document purpose of collection",
                "Provide opt-out mechanism",
                "Retain only for stated purpose"
            ],
            "severity": "critical",
            "source": "Privacy Policy v3.0, Section 2.1"
        }
    ),
    Concept(
        name="data_retention",
        attributes={
            "rule_id": "DP-002",
            "domain": "data_privacy",
            "title": "Data Retention Limits",
            "description": "Personal data must be deleted after retention period",
            "requirements": [
                "Maximum retention: 3 years for customer data",
                "Maximum retention: 7 years for financial records",
                "Automated deletion after retention period",
                "Document retention justification"
            ],
            "severity": "high",
            "source": "Privacy Policy v3.0, Section 4.2"
        }
    ),
    Concept(
        name="data_transfer",
        attributes={
            "rule_id": "DP-003",
            "domain": "data_privacy",
            "title": "Cross-Border Data Transfer",
            "description": "Data transfers outside region require safeguards",
            "requirements": [
                "Standard contractual clauses required",
                "Adequacy decision verification",
                "Document transfer mechanism",
                "Notify data subjects"
            ],
            "severity": "critical",
            "source": "Privacy Policy v3.0, Section 5.1"
        }
    ),
    # Information Security Rules
    Concept(
        name="password_policy",
        attributes={
            "rule_id": "IS-001",
            "domain": "information_security",
            "title": "Password Requirements",
            "description": "Minimum password complexity and rotation",
            "requirements": [
                "Minimum 12 characters",
                "Include uppercase, lowercase, numbers, symbols",
                "No password reuse for 12 cycles",
                "90-day rotation for privileged accounts"
            ],
            "severity": "high",
            "source": "Security Policy v2.5, Section 3.1"
        }
    ),
    Concept(
        name="access_control",
        attributes={
            "rule_id": "IS-002",
            "domain": "information_security",
            "title": "Access Control Requirements",
            "description": "Principle of least privilege for all access",
            "requirements": [
                "Role-based access control",
                "Quarterly access reviews",
                "Immediate revocation on termination",
                "MFA for sensitive systems"
            ],
            "severity": "critical",
            "source": "Security Policy v2.5, Section 4.1"
        }
    ),
    # Financial Controls
    Concept(
        name="expense_approval",
        attributes={
            "rule_id": "FC-001",
            "domain": "financial_controls",
            "title": "Expense Approval Thresholds",
            "description": "Approval requirements based on expense amount",
            "requirements": [
                "Under $500: Self-approval",
                "$500-$5000: Manager approval",
                "$5000-$25000: Director approval",
                "Over $25000: VP approval"
            ],
            "severity": "medium",
            "source": "Financial Policy v2.0, Section 2.3"
        }
    ),
    Concept(
        name="vendor_payment",
        attributes={
            "rule_id": "FC-002",
            "domain": "financial_controls",
            "title": "Vendor Payment Requirements",
            "description": "Requirements for processing vendor payments",
            "requirements": [
                "Valid W-9 on file",
                "Approved purchase order",
                "Three-way match verification",
                "Dual approval for payments over $10000"
            ],
            "severity": "high",
            "source": "Financial Policy v2.0, Section 3.1"
        }
    ),
]

print("\nEncoding policy rules...")
for rule in policy_rules:
    glyph = model.encode(rule)
    print(f"  ✓ {rule.attributes['rule_id']}: {rule.attributes['title']}")

# =============================================================================
# Compliance Check Functions
# =============================================================================

def check_compliance(action_description: str, context: dict = None):
    """
    Check if an action complies with applicable policies.
    
    Returns:
    - compliant: Boolean indicating compliance
    - applicable_rules: List of relevant policy rules
    - violations: List of potential violations
    - recommendations: Suggested actions
    """
    print(f"\n{'='*60}")
    print(f"COMPLIANCE CHECK")
    print(f"Action: {action_description}")
    print('='*60)
    
    # Create a concept for the action
    action_concept = Concept(
        name="action_check",
        attributes={
            "description": action_description,
            **(context or {})
        }
    )
    
    # Find applicable policy rules
    results = model.similarity_search(action_concept, top_k=5)
    
    applicable_rules = []
    violations = []
    recommendations = []
    
    for result in results:
        if "rule_id" in result.attributes:
            rule = result.attributes
            applicable_rules.append({
                "rule_id": rule["rule_id"],
                "title": rule["title"],
                "relevance": result.score,
                "severity": rule["severity"],
                "source": rule["source"]
            })
            
            # Check for potential violations based on context
            if context:
                for req in rule.get("requirements", []):
                    # Simplified violation check
                    if rule["severity"] == "critical" and result.score > 0.7:
                        recommendations.append(f"Review {rule['rule_id']}: {req}")
    
    # Determine overall compliance
    critical_rules = [r for r in applicable_rules if r["severity"] == "critical"]
    compliant = len(violations) == 0
    
    print(f"\nApplicable Rules ({len(applicable_rules)}):")
    for rule in applicable_rules[:3]:
        severity_icon = "🔴" if rule["severity"] == "critical" else "🟡" if rule["severity"] == "high" else "🟢"
        print(f"  {severity_icon} {rule['rule_id']}: {rule['title']}")
        print(f"     Relevance: {rule['relevance']:.2f} | Source: {rule['source']}")
    
    if recommendations:
        print(f"\nRecommendations:")
        for rec in recommendations[:3]:
            print(f"  • {rec}")
    
    print(f"\nCompliance Status: {'✓ COMPLIANT' if compliant else '✗ REVIEW REQUIRED'}")
    
    return {
        "compliant": compliant,
        "applicable_rules": applicable_rules,
        "violations": violations,
        "recommendations": recommendations
    }


def get_policy_tree(domain_name: str):
    """
    Get the policy hierarchy for a domain as a fact tree.
    """
    print(f"\n{'='*60}")
    print(f"POLICY TREE: {domain_name}")
    print('='*60)
    
    # Find the domain
    domain_results = model.similarity_search(domain_name, top_k=1)
    
    if not domain_results:
        return None
    
    domain = domain_results[0]
    
    # Find all rules in this domain
    rule_results = model.similarity_search(
        domain,
        top_k=20,
        filters={"domain": domain_name}
    )
    
    rules = []
    for result in rule_results:
        if "rule_id" in result.attributes:
            rules.append({
                "rule_id": result.attributes["rule_id"],
                "title": result.attributes["title"],
                "severity": result.attributes["severity"]
            })
    
    print(f"\nDomain: {domain.attributes.get('domain', domain_name)}")
    print(f"Owner: {domain.attributes.get('owner', 'Unknown')}")
    print(f"Version: {domain.attributes.get('version', 'Unknown')}")
    print(f"\nRules ({len(rules)}):")
    for rule in rules:
        severity_icon = "🔴" if rule["severity"] == "critical" else "🟡" if rule["severity"] == "high" else "🟢"
        print(f"  {severity_icon} {rule['rule_id']}: {rule['title']}")
    
    return {
        "domain": domain.attributes,
        "rules": rules
    }

# =============================================================================
# Test Compliance Checks
# =============================================================================

print("\n" + "="*60)
print("TESTING COMPLIANCE CHECKS")
print("="*60)

# Test various actions
test_actions = [
    {
        "description": "Collecting customer email addresses for marketing",
        "context": {"data_type": "email", "purpose": "marketing"}
    },
    {
        "description": "Transferring customer data to EU data center",
        "context": {"data_type": "customer_pii", "destination": "EU"}
    },
    {
        "description": "Processing vendor payment of $15,000",
        "context": {"amount": 15000, "type": "vendor_payment"}
    },
    {
        "description": "Granting database admin access to new employee",
        "context": {"access_level": "admin", "system": "database"}
    },
]

for action in test_actions:
    result = check_compliance(action["description"], action["context"])

# =============================================================================
# Display Policy Trees
# =============================================================================

print("\n" + "="*60)
print("POLICY HIERARCHY")
print("="*60)

for domain in ["data_privacy", "information_security", "financial_controls"]:
    get_policy_tree(domain)

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("policy-compliance.glyphh")
print("✓ Model exported to policy-compliance.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @policy-compliance.glyphh")

print("\nCheck compliance via API:")
print('  curl -X POST http://localhost:8000/api/v1/policy-compliance/check \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"action": "Collecting customer emails", "context": {...}}\'')

print("\n" + "="*60)
print("KEY BENEFITS")
print("="*60)
print("""
1. TRACEABLE DECISIONS
   - Every check cites specific policy sections
   - Full audit trail for compliance reviews
   
2. HIERARCHICAL POLICIES
   - Navigate from domains to specific rules
   - Understand policy relationships
   
3. CONTEXT-AWARE
   - Consider action context in checks
   - Relevant rules surface automatically
   
4. SEVERITY-BASED
   - Critical rules highlighted
   - Prioritized recommendations
""")
