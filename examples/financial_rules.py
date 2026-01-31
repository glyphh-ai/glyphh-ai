"""
Financial Rules Engine Example

Apply financial rules and calculations with full audit trails
using fact trees and similarity search for rule matching.

Key Principle: Every financial decision is traceable to specific
rules with complete calculation transparency.

This example demonstrates:
1. Creating financial rule concepts with conditions
2. Fact trees for rule hierarchies and dependencies
3. Similarity search for finding applicable rules
4. Audit trail generation for compliance

Use Cases:
- Loan approval workflows
- Credit limit decisions
- Fee calculations
- Regulatory compliance checks
"""

from glyphh import GlyphhModel, Concept, EncoderConfig

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Financial Rule Concepts
# =============================================================================

def create_rule(
    rule_id: str,
    name: str,
    category: str,  # "credit", "fee", "limit", "compliance"
    description: str,
    # Conditions
    conditions: list,
    # Actions
    action_type: str,  # "approve", "deny", "calculate", "flag"
    action_params: dict,
    # Metadata
    effective_date: str,
    expiry_date: str = None,
    priority: int = 0,
    source: str = None,
):
    """Create a financial rule concept."""
    return Concept(
        name=f"rule_{rule_id}",
        attributes={
            "rule_id": rule_id,
            "name": name,
            "category": category,
            "description": description,
            "conditions": conditions,
            "action_type": action_type,
            "action_params": action_params,
            "effective_date": effective_date,
            "expiry_date": expiry_date,
            "priority": priority,
            "source": source,
            # For cortex similarity
            "layer": category,
        }
    )

# =============================================================================
# Create Financial Rules
# =============================================================================

print("Creating financial rules...")

rules = [
    # Credit Rules
    create_rule(
        "CR-001", "Minimum Credit Score",
        category="credit",
        description="Minimum credit score requirement for loan approval",
        conditions=[
            {"field": "credit_score", "operator": ">=", "value": 650}
        ],
        action_type="approve",
        action_params={"next_rule": "CR-002"},
        effective_date="2025-01-01",
        priority=1,
        source="Credit Policy v2.0"
    ),
    create_rule(
        "CR-002", "Debt-to-Income Ratio",
        category="credit",
        description="Maximum DTI ratio for loan approval",
        conditions=[
            {"field": "dti_ratio", "operator": "<=", "value": 0.43}
        ],
        action_type="approve",
        action_params={"next_rule": "CR-003"},
        effective_date="2025-01-01",
        priority=2,
        source="Credit Policy v2.0"
    ),
    create_rule(
        "CR-003", "Employment Verification",
        category="credit",
        description="Minimum employment duration requirement",
        conditions=[
            {"field": "employment_months", "operator": ">=", "value": 24}
        ],
        action_type="approve",
        action_params={"approval_tier": "standard"},
        effective_date="2025-01-01",
        priority=3,
        source="Credit Policy v2.0"
    ),
    create_rule(
        "CR-004", "High Credit Score Fast Track",
        category="credit",
        description="Expedited approval for excellent credit",
        conditions=[
            {"field": "credit_score", "operator": ">=", "value": 750},
            {"field": "dti_ratio", "operator": "<=", "value": 0.35}
        ],
        action_type="approve",
        action_params={"approval_tier": "premium", "rate_discount": 0.25},
        effective_date="2025-01-01",
        priority=0,  # Higher priority (checked first)
        source="Credit Policy v2.0"
    ),
    # Fee Rules
    create_rule(
        "FE-001", "Late Payment Fee",
        category="fee",
        description="Fee for payments received after due date",
        conditions=[
            {"field": "days_past_due", "operator": ">", "value": 0}
        ],
        action_type="calculate",
        action_params={
            "fee_type": "late_payment",
            "calculation": "min(balance * 0.05, 50)"
        },
        effective_date="2025-01-01",
        source="Fee Schedule v3.0"
    ),
    create_rule(
        "FE-002", "Overdraft Fee",
        category="fee",
        description="Fee for overdraft transactions",
        conditions=[
            {"field": "balance", "operator": "<", "value": 0}
        ],
        action_type="calculate",
        action_params={
            "fee_type": "overdraft",
            "fee_amount": 35,
            "max_per_day": 3
        },
        effective_date="2025-01-01",
        source="Fee Schedule v3.0"
    ),
    create_rule(
        "FE-003", "Wire Transfer Fee",
        category="fee",
        description="Fee for outgoing wire transfers",
        conditions=[
            {"field": "transaction_type", "operator": "==", "value": "wire_transfer"}
        ],
        action_type="calculate",
        action_params={
            "fee_type": "wire",
            "domestic_fee": 25,
            "international_fee": 45
        },
        effective_date="2025-01-01",
        source="Fee Schedule v3.0"
    ),
    # Limit Rules
    create_rule(
        "LM-001", "Daily ATM Withdrawal Limit",
        category="limit",
        description="Maximum daily ATM withdrawal amount",
        conditions=[
            {"field": "account_type", "operator": "==", "value": "checking"}
        ],
        action_type="limit",
        action_params={
            "limit_type": "atm_withdrawal",
            "standard_limit": 500,
            "premium_limit": 1000
        },
        effective_date="2025-01-01",
        source="Account Limits Policy"
    ),
    create_rule(
        "LM-002", "Daily Transfer Limit",
        category="limit",
        description="Maximum daily external transfer amount",
        conditions=[
            {"field": "transfer_type", "operator": "==", "value": "external"}
        ],
        action_type="limit",
        action_params={
            "limit_type": "external_transfer",
            "standard_limit": 5000,
            "premium_limit": 25000
        },
        effective_date="2025-01-01",
        source="Account Limits Policy"
    ),
    # Compliance Rules
    create_rule(
        "CO-001", "Large Transaction Report",
        category="compliance",
        description="CTR filing requirement for large cash transactions",
        conditions=[
            {"field": "cash_amount", "operator": ">=", "value": 10000}
        ],
        action_type="flag",
        action_params={
            "flag_type": "CTR",
            "report_required": True,
            "deadline_days": 15
        },
        effective_date="2025-01-01",
        source="BSA/AML Regulations"
    ),
    create_rule(
        "CO-002", "Suspicious Activity Detection",
        category="compliance",
        description="SAR filing for suspicious patterns",
        conditions=[
            {"field": "structuring_detected", "operator": "==", "value": True}
        ],
        action_type="flag",
        action_params={
            "flag_type": "SAR",
            "report_required": True,
            "deadline_days": 30,
            "escalate_to": "compliance_officer"
        },
        effective_date="2025-01-01",
        source="BSA/AML Regulations"
    ),
]

for rule in rules:
    glyph = model.encode(rule)
    print(f"  ✓ {rule.attributes['rule_id']}: {rule.attributes['name']}")

# =============================================================================
# Rule Evaluation Functions
# =============================================================================

def evaluate_condition(condition: dict, data: dict) -> bool:
    """Evaluate a single condition against data."""
    field = condition["field"]
    operator = condition["operator"]
    value = condition["value"]
    
    if field not in data:
        return False
    
    actual = data[field]
    
    if operator == ">=":
        return actual >= value
    elif operator == "<=":
        return actual <= value
    elif operator == ">":
        return actual > value
    elif operator == "<":
        return actual < value
    elif operator == "==":
        return actual == value
    elif operator == "!=":
        return actual != value
    
    return False


def find_applicable_rules(category: str, data: dict):
    """
    Find all rules applicable to a given category and data.
    """
    print(f"\n{'='*60}")
    print(f"FINDING APPLICABLE RULES")
    print(f"Category: {category}")
    print('='*60)
    
    # Search for rules in category
    results = model.similarity_search(category, top_k=20)
    
    applicable = []
    for result in results:
        if "rule_id" not in result.attributes:
            continue
        
        attrs = result.attributes
        if attrs["category"] != category:
            continue
        
        # Check all conditions
        conditions_met = True
        for condition in attrs["conditions"]:
            if not evaluate_condition(condition, data):
                conditions_met = False
                break
        
        if conditions_met:
            applicable.append({
                "rule_id": attrs["rule_id"],
                "name": attrs["name"],
                "action_type": attrs["action_type"],
                "action_params": attrs["action_params"],
                "priority": attrs["priority"],
                "source": attrs["source"]
            })
    
    # Sort by priority
    applicable.sort(key=lambda x: x["priority"])
    
    print(f"\nApplicable Rules: {len(applicable)}")
    for rule in applicable:
        print(f"  • {rule['rule_id']}: {rule['name']}")
        print(f"    Action: {rule['action_type']}")
        print(f"    Source: {rule['source']}")
    
    return applicable


def evaluate_credit_application(application: dict):
    """
    Evaluate a credit application against all credit rules.
    """
    print(f"\n{'='*60}")
    print(f"CREDIT APPLICATION EVALUATION")
    print('='*60)
    
    print(f"\nApplication Data:")
    for key, value in application.items():
        print(f"  {key}: {value}")
    
    # Find applicable credit rules
    applicable_rules = find_applicable_rules("credit", application)
    
    # Build audit trail
    audit_trail = []
    decision = "pending"
    approval_tier = None
    rate_discount = 0
    
    for rule in applicable_rules:
        audit_entry = {
            "rule_id": rule["rule_id"],
            "rule_name": rule["name"],
            "result": "passed",
            "source": rule["source"]
        }
        
        if rule["action_type"] == "approve":
            if "approval_tier" in rule["action_params"]:
                approval_tier = rule["action_params"]["approval_tier"]
            if "rate_discount" in rule["action_params"]:
                rate_discount = rule["action_params"]["rate_discount"]
            decision = "approved"
        
        audit_trail.append(audit_entry)
    
    # Check for any failed rules
    all_rules = model.similarity_search("credit", top_k=20)
    for result in all_rules:
        if "rule_id" not in result.attributes:
            continue
        attrs = result.attributes
        if attrs["category"] != "credit":
            continue
        
        # Check if this rule was not in applicable (meaning conditions failed)
        if not any(r["rule_id"] == attrs["rule_id"] for r in applicable_rules):
            for condition in attrs["conditions"]:
                if not evaluate_condition(condition, application):
                    audit_trail.append({
                        "rule_id": attrs["rule_id"],
                        "rule_name": attrs["name"],
                        "result": "failed",
                        "failed_condition": condition,
                        "source": attrs["source"]
                    })
                    decision = "denied"
                    break
    
    print(f"\n{'='*60}")
    print(f"DECISION: {decision.upper()}")
    print('='*60)
    
    if decision == "approved":
        print(f"  Approval Tier: {approval_tier}")
        if rate_discount > 0:
            print(f"  Rate Discount: {rate_discount}%")
    
    print(f"\nAudit Trail:")
    for entry in audit_trail:
        status_icon = "✓" if entry["result"] == "passed" else "✗"
        print(f"  {status_icon} {entry['rule_id']}: {entry['rule_name']} - {entry['result'].upper()}")
        if entry["result"] == "failed" and "failed_condition" in entry:
            cond = entry["failed_condition"]
            print(f"      Failed: {cond['field']} {cond['operator']} {cond['value']}")
    
    return {
        "decision": decision,
        "approval_tier": approval_tier,
        "rate_discount": rate_discount,
        "audit_trail": audit_trail
    }


def calculate_fees(transaction: dict):
    """
    Calculate applicable fees for a transaction.
    """
    print(f"\n{'='*60}")
    print(f"FEE CALCULATION")
    print('='*60)
    
    print(f"\nTransaction Data:")
    for key, value in transaction.items():
        print(f"  {key}: {value}")
    
    # Find applicable fee rules
    applicable_rules = find_applicable_rules("fee", transaction)
    
    total_fees = 0
    fee_breakdown = []
    
    for rule in applicable_rules:
        params = rule["action_params"]
        fee_amount = 0
        
        if "fee_amount" in params:
            fee_amount = params["fee_amount"]
        elif "calculation" in params:
            # Simple calculation parsing
            calc = params["calculation"]
            if "balance" in calc and "balance" in transaction:
                # Example: min(balance * 0.05, 50)
                fee_amount = min(abs(transaction["balance"]) * 0.05, 50)
        elif "domestic_fee" in params:
            if transaction.get("destination") == "domestic":
                fee_amount = params["domestic_fee"]
            else:
                fee_amount = params["international_fee"]
        
        if fee_amount > 0:
            fee_breakdown.append({
                "rule_id": rule["rule_id"],
                "fee_type": params.get("fee_type", "unknown"),
                "amount": fee_amount
            })
            total_fees += fee_amount
    
    print(f"\nFee Breakdown:")
    for fee in fee_breakdown:
        print(f"  • {fee['fee_type']}: ${fee['amount']:.2f}")
        print(f"    Rule: {fee['rule_id']}")
    
    print(f"\nTotal Fees: ${total_fees:.2f}")
    
    return {
        "total_fees": total_fees,
        "breakdown": fee_breakdown
    }


def check_compliance(transaction: dict):
    """
    Check transaction for compliance requirements.
    """
    print(f"\n{'='*60}")
    print(f"COMPLIANCE CHECK")
    print('='*60)
    
    # Find applicable compliance rules
    applicable_rules = find_applicable_rules("compliance", transaction)
    
    flags = []
    for rule in applicable_rules:
        params = rule["action_params"]
        flags.append({
            "rule_id": rule["rule_id"],
            "flag_type": params.get("flag_type"),
            "report_required": params.get("report_required", False),
            "deadline_days": params.get("deadline_days"),
            "escalate_to": params.get("escalate_to")
        })
    
    if flags:
        print(f"\n⚠️  COMPLIANCE FLAGS RAISED: {len(flags)}")
        for flag in flags:
            print(f"\n  🚩 {flag['flag_type']}")
            print(f"     Rule: {flag['rule_id']}")
            print(f"     Report Required: {flag['report_required']}")
            if flag['deadline_days']:
                print(f"     Deadline: {flag['deadline_days']} days")
            if flag['escalate_to']:
                print(f"     Escalate To: {flag['escalate_to']}")
    else:
        print(f"\n✓ No compliance flags")
    
    return flags

# =============================================================================
# Test Financial Rules
# =============================================================================

print("\n" + "="*60)
print("TESTING FINANCIAL RULES ENGINE")
print("="*60)

# Test credit application - should approve
good_application = {
    "credit_score": 720,
    "dti_ratio": 0.35,
    "employment_months": 36,
    "loan_amount": 25000
}
evaluate_credit_application(good_application)

# Test credit application - excellent credit
excellent_application = {
    "credit_score": 780,
    "dti_ratio": 0.28,
    "employment_months": 60,
    "loan_amount": 50000
}
evaluate_credit_application(excellent_application)

# Test credit application - should deny
poor_application = {
    "credit_score": 580,
    "dti_ratio": 0.55,
    "employment_months": 12,
    "loan_amount": 15000
}
evaluate_credit_application(poor_application)

# Test fee calculation
late_payment = {
    "days_past_due": 5,
    "balance": 1500
}
calculate_fees(late_payment)

# Test wire transfer fee
wire_transfer = {
    "transaction_type": "wire_transfer",
    "destination": "international",
    "amount": 5000
}
calculate_fees(wire_transfer)

# Test compliance check
large_cash = {
    "cash_amount": 15000,
    "transaction_type": "deposit"
}
check_compliance(large_cash)

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("financial-rules.glyphh")
print("✓ Model exported to financial-rules.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @financial-rules.glyphh")

print("\nEvaluate application via API:")
print('  curl -X POST http://localhost:8000/api/v1/financial-rules/evaluate \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"credit_score": 720, "dti_ratio": 0.35, ...}\'')

print("\n" + "="*60)
print("KEY FEATURES")
print("="*60)
print("""
1. RULE-BASED DECISIONS
   - Configurable conditions and actions
   - Priority-based rule ordering
   
2. FULL AUDIT TRAIL
   - Every decision traceable to rules
   - Compliance-ready documentation
   
3. FLEXIBLE CALCULATIONS
   - Fee calculations with formulas
   - Limit enforcement
   
4. COMPLIANCE INTEGRATION
   - Automatic flagging for reporting
   - Escalation workflows
""")
