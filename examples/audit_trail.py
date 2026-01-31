"""
Audit Trail Management Example

Track and analyze system events with temporal patterns to detect
anomalies and maintain compliance audit trails.

Key Principle: Every action is recorded with full context and
linked temporally to enable forensic analysis.

This example demonstrates:
1. Creating audit event concepts with rich metadata
2. Temporal edges for event sequencing
3. Fact trees for event relationship analysis
4. Anomaly detection through pattern matching

Use Cases:
- Security audit logging
- Compliance evidence collection
- Incident investigation
- Change management tracking
"""

from glyphh import GlyphhModel, Concept, EncoderConfig
from glyphh import TemporalEncoder

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Audit Event Concepts
# =============================================================================

def create_audit_event(
    event_id: str,
    timestamp: str,
    # Event classification
    event_type: str,  # "authentication", "authorization", "data_access", "config_change"
    action: str,  # "login", "logout", "read", "write", "delete", "modify"
    status: str,  # "success", "failure", "denied"
    # Actor information
    user_id: str,
    user_role: str,
    ip_address: str,
    user_agent: str = None,
    # Resource information
    resource_type: str = None,
    resource_id: str = None,
    # Context
    session_id: str = None,
    request_id: str = None,
    # Risk indicators
    is_privileged: bool = False,
    is_sensitive: bool = False,
    risk_score: float = 0.0,
):
    """Create an audit event concept."""
    return Concept(
        name=f"event_{event_id}",
        attributes={
            "event_id": event_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "action": action,
            "status": status,
            "user_id": user_id,
            "user_role": user_role,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "session_id": session_id,
            "request_id": request_id,
            "is_privileged": is_privileged,
            "is_sensitive": is_sensitive,
            "risk_score": risk_score,
            # For cortex similarity
            "layer": event_type,
            "role": user_role,
        }
    )

# =============================================================================
# Define Event Pattern Archetypes
# =============================================================================

event_patterns = [
    Concept(
        name="normal_login",
        attributes={
            "pattern_name": "Normal Login",
            "description": "Standard successful authentication",
            "event_type": "authentication",
            "action": "login",
            "status": "success",
            "risk_level": "low",
            "characteristics": ["expected", "routine", "no action needed"]
        }
    ),
    Concept(
        name="failed_login_burst",
        attributes={
            "pattern_name": "Failed Login Burst",
            "description": "Multiple failed login attempts in short period",
            "event_type": "authentication",
            "action": "login",
            "status": "failure",
            "risk_level": "high",
            "characteristics": ["potential attack", "investigate", "consider lockout"]
        }
    ),
    Concept(
        name="privilege_escalation",
        attributes={
            "pattern_name": "Privilege Escalation",
            "description": "User gaining elevated permissions",
            "event_type": "authorization",
            "is_privileged": True,
            "risk_level": "medium",
            "characteristics": ["verify authorization", "document justification"]
        }
    ),
    Concept(
        name="sensitive_data_access",
        attributes={
            "pattern_name": "Sensitive Data Access",
            "description": "Access to sensitive or regulated data",
            "event_type": "data_access",
            "is_sensitive": True,
            "risk_level": "medium",
            "characteristics": ["log for compliance", "verify need-to-know"]
        }
    ),
    Concept(
        name="bulk_data_export",
        attributes={
            "pattern_name": "Bulk Data Export",
            "description": "Large volume data extraction",
            "event_type": "data_access",
            "action": "read",
            "risk_level": "high",
            "characteristics": ["potential exfiltration", "verify authorization", "alert security"]
        }
    ),
    Concept(
        name="config_change",
        attributes={
            "pattern_name": "Configuration Change",
            "description": "System configuration modification",
            "event_type": "config_change",
            "risk_level": "medium",
            "characteristics": ["document change", "verify approval", "test impact"]
        }
    ),
    Concept(
        name="off_hours_access",
        attributes={
            "pattern_name": "Off-Hours Access",
            "description": "System access outside normal business hours",
            "risk_level": "medium",
            "characteristics": ["unusual timing", "verify legitimacy"]
        }
    ),
]

print("Encoding event patterns...")
for pattern in event_patterns:
    glyph = model.encode(pattern)
    print(f"  ✓ {pattern.name}: {pattern.attributes['pattern_name']}")

# =============================================================================
# Create Sample Audit Events
# =============================================================================

print("\nCreating audit events...")

# Normal user session
normal_session = [
    create_audit_event(
        "E001", "2025-01-30T09:00:00Z",
        event_type="authentication", action="login", status="success",
        user_id="user_123", user_role="analyst", ip_address="10.0.1.50",
        session_id="sess_abc123"
    ),
    create_audit_event(
        "E002", "2025-01-30T09:05:00Z",
        event_type="data_access", action="read", status="success",
        user_id="user_123", user_role="analyst", ip_address="10.0.1.50",
        resource_type="report", resource_id="report_456",
        session_id="sess_abc123"
    ),
    create_audit_event(
        "E003", "2025-01-30T17:30:00Z",
        event_type="authentication", action="logout", status="success",
        user_id="user_123", user_role="analyst", ip_address="10.0.1.50",
        session_id="sess_abc123"
    ),
]

# Suspicious activity pattern
suspicious_session = [
    create_audit_event(
        "E010", "2025-01-30T02:00:00Z",
        event_type="authentication", action="login", status="failure",
        user_id="admin_001", user_role="admin", ip_address="203.0.113.50",
        risk_score=0.3
    ),
    create_audit_event(
        "E011", "2025-01-30T02:00:05Z",
        event_type="authentication", action="login", status="failure",
        user_id="admin_001", user_role="admin", ip_address="203.0.113.50",
        risk_score=0.5
    ),
    create_audit_event(
        "E012", "2025-01-30T02:00:10Z",
        event_type="authentication", action="login", status="failure",
        user_id="admin_001", user_role="admin", ip_address="203.0.113.50",
        risk_score=0.7
    ),
    create_audit_event(
        "E013", "2025-01-30T02:00:15Z",
        event_type="authentication", action="login", status="success",
        user_id="admin_001", user_role="admin", ip_address="203.0.113.50",
        is_privileged=True, risk_score=0.8
    ),
    create_audit_event(
        "E014", "2025-01-30T02:01:00Z",
        event_type="data_access", action="read", status="success",
        user_id="admin_001", user_role="admin", ip_address="203.0.113.50",
        resource_type="customer_pii", resource_id="bulk_export",
        is_sensitive=True, is_privileged=True, risk_score=0.9
    ),
]

# Encode all events
all_events = normal_session + suspicious_session
for event in all_events:
    glyph = model.encode(event)
    print(f"  ✓ {event.name}: {event.attributes['action']} ({event.attributes['status']})")

# =============================================================================
# Create Temporal Edges
# =============================================================================

print("\nCreating temporal edges...")

temporal_encoder = TemporalEncoder(config)

# Link normal session events
for i in range(len(normal_session) - 1):
    edge = temporal_encoder.create_edge(
        from_concept=normal_session[i],
        to_concept=normal_session[i + 1],
        edge_type="session_sequence"
    )
    print(f"  ✓ Normal: {normal_session[i].attributes['event_id']} → {normal_session[i+1].attributes['event_id']}")

# Link suspicious session events
for i in range(len(suspicious_session) - 1):
    edge = temporal_encoder.create_edge(
        from_concept=suspicious_session[i],
        to_concept=suspicious_session[i + 1],
        edge_type="session_sequence"
    )
    print(f"  ✓ Suspicious: {suspicious_session[i].attributes['event_id']} → {suspicious_session[i+1].attributes['event_id']}")

# =============================================================================
# Audit Analysis Functions
# =============================================================================

def analyze_event(event: Concept):
    """
    Analyze an audit event for risk and pattern matching.
    """
    print(f"\n{'='*60}")
    print(f"EVENT ANALYSIS: {event.attributes['event_id']}")
    print('='*60)
    
    attrs = event.attributes
    print(f"Type: {attrs['event_type']}")
    print(f"Action: {attrs['action']}")
    print(f"Status: {attrs['status']}")
    print(f"User: {attrs['user_id']} ({attrs['user_role']})")
    
    # Find matching patterns
    results = model.similarity_search(event, top_k=3)
    
    patterns = []
    for result in results:
        if "pattern_name" in result.attributes:
            patterns.append({
                "pattern": result.attributes["pattern_name"],
                "risk_level": result.attributes["risk_level"],
                "confidence": result.score,
                "characteristics": result.attributes.get("characteristics", [])
            })
    
    if patterns:
        print(f"\nMatched Patterns:")
        for p in patterns:
            risk_icon = "🔴" if p["risk_level"] == "high" else "🟡" if p["risk_level"] == "medium" else "🟢"
            print(f"  {risk_icon} {p['pattern']} ({p['confidence']:.2f})")
            print(f"     {', '.join(p['characteristics'])}")
    
    return patterns


def investigate_session(session_id: str, events: list):
    """
    Investigate all events in a session for anomalies.
    """
    print(f"\n{'='*60}")
    print(f"SESSION INVESTIGATION: {session_id}")
    print('='*60)
    
    session_events = [e for e in events if e.attributes.get("session_id") == session_id]
    
    if not session_events:
        # Check by user pattern
        session_events = events
    
    print(f"\nEvents in session: {len(session_events)}")
    
    risk_scores = []
    for event in session_events:
        patterns = analyze_event(event)
        if patterns:
            risk_scores.append(max(p["confidence"] for p in patterns if p["risk_level"] == "high"))
    
    overall_risk = max(risk_scores) if risk_scores else 0
    
    print(f"\n{'='*60}")
    print(f"SESSION RISK ASSESSMENT")
    print('='*60)
    print(f"Overall Risk Score: {overall_risk:.2f}")
    
    if overall_risk > 0.7:
        print("⚠️  HIGH RISK - Immediate investigation required")
    elif overall_risk > 0.4:
        print("⚡ MEDIUM RISK - Review recommended")
    else:
        print("✓ LOW RISK - Normal activity")
    
    return overall_risk


def get_user_activity(user_id: str, events: list):
    """
    Get activity summary for a specific user.
    """
    user_events = [e for e in events if e.attributes.get("user_id") == user_id]
    
    print(f"\n{'='*60}")
    print(f"USER ACTIVITY: {user_id}")
    print('='*60)
    print(f"Total Events: {len(user_events)}")
    
    # Summarize by type
    by_type = {}
    for event in user_events:
        t = event.attributes["event_type"]
        by_type[t] = by_type.get(t, 0) + 1
    
    print("\nBy Event Type:")
    for t, count in by_type.items():
        print(f"  • {t}: {count}")
    
    # Check for sensitive access
    sensitive = [e for e in user_events if e.attributes.get("is_sensitive")]
    if sensitive:
        print(f"\n⚠️  Sensitive Data Access: {len(sensitive)} events")
    
    return user_events

# =============================================================================
# Test Audit Analysis
# =============================================================================

print("\n" + "="*60)
print("TESTING AUDIT ANALYSIS")
print("="*60)

# Analyze individual events
for event in suspicious_session:
    analyze_event(event)

# Investigate suspicious session
print("\n" + "="*60)
print("SESSION INVESTIGATION")
print("="*60)

investigate_session("suspicious", suspicious_session)

# Get user activity
get_user_activity("admin_001", all_events)

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("audit-trail.glyphh")
print("✓ Model exported to audit-trail.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @audit-trail.glyphh")

print("\nAnalyze event via API:")
print('  curl -X POST http://localhost:8000/api/v1/audit-trail/analyze \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"event_id": "E014", "event_type": "data_access", ...}\'')

print("\n" + "="*60)
print("KEY CAPABILITIES")
print("="*60)
print("""
1. PATTERN DETECTION
   - Match events to known risk patterns
   - Identify anomalies automatically
   
2. TEMPORAL ANALYSIS
   - Track event sequences
   - Detect suspicious timing patterns
   
3. SESSION INVESTIGATION
   - Analyze complete user sessions
   - Calculate session risk scores
   
4. COMPLIANCE READY
   - Full audit trail with context
   - Evidence for compliance reviews
""")
