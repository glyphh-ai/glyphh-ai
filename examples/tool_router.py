"""
Tool Router Example (Glyphh)

Route natural language requests to the correct tool/action using pattern recognition,
not hardcoded keyword rules.

Key Principle: Don't hardwire routing rules - let the model learn patterns from:
- Intent phrasing (create/update/search/summarize)
- Entities (calendar/email/jira/slack/github/etc.)
- Required slots (channel, recipients, date/time, project, repo, etc.)
- Policy / permission context (role/segment)
- Tool metadata (requires_auth, domain)

Output:
- EXECUTE: chosen tool + args (if sufficient info)
- ASK: minimal clarifying question(s) tied to missing slots
- AUTH_REQUIRED: connect required provider/app before executing
"""

from glyphh import (
    Encoder, EncoderConfig, Concept, GlyphhModel,
    SimilarityCalculator, LayerConfig, SegmentConfig, Role
)

# -----------------------------------------------------------------------------
# 1) Router Encoder Config
# -----------------------------------------------------------------------------

config = EncoderConfig(
    dimension=10000,
    seed=42,
    layers=[
        LayerConfig(
            name="router",
            similarity_weight=1.0,
            segments=[
                # Natural language intent surface
                SegmentConfig(
                    name="intent",
                    roles=[
                        Role(name="verb", similarity_weight=1.0),         # "schedule", "send", "create", "post"
                        Role(name="object", similarity_weight=0.9),       # "meeting", "email", "ticket", "message"
                        Role(name="domain", similarity_weight=1.0),       # "calendar", "email", "jira", "slack"
                        Role(name="time_ref", similarity_weight=0.7),     # "next week", "tomorrow", "today"
                        Role(name="urgency", similarity_weight=0.5),      # "asap", "urgent"
                    ],
                ),

                # Tool catalog / capability signal
                SegmentConfig(
                    name="tool",
                    roles=[
                        Role(name="tool_id", similarity_weight=1.0),          # canonical tool key
                        Role(name="provider", similarity_weight=0.7),         # "pipedream", "mcp", "openapi"
                        Role(name="tool_domain", similarity_weight=0.9),      # "slack", "gmail", "gcal", "jira"
                        Role(name="requires_auth", similarity_weight=0.6),    # "true/false"
                    ],
                ),

                # Argument/slot signal (what must be present)
                SegmentConfig(
                    name="slots",
                    roles=[
                        Role(name="required_slots", similarity_weight=1.0),   # e.g. "channel,text" or "to,subject,body"
                        Role(name="optional_slots", similarity_weight=0.4),
                        Role(name="slot_values", similarity_weight=0.8),      # partial values if present
                    ],
                ),

                # Governance/policy context
                SegmentConfig(
                    name="policy",
                    roles=[
                        Role(name="user_role", similarity_weight=0.8),        # "admin", "csm", "viewer"
                        Role(name="tenant_segment", similarity_weight=0.6),   # "prod", "dev", "enterprise"
                        Role(name="constraints", similarity_weight=0.8),      # "no_external_email", etc.
                    ],
                )
            ],
        )
    ],
)

encoder = Encoder(config)
calculator = SimilarityCalculator()

print("Tool Router Model")
print("=" * 60)

# -----------------------------------------------------------------------------
# 2) Tool Catalog (minimal) + Slot Requirements
# -----------------------------------------------------------------------------
# In production, you’d ingest these from:
# - Pipedream actions / MCP tool manifests / OpenAPI specs
# and encode them as facts.

TOOL_CATALOG = {
    "slack.post_message": {
        "provider": "pipedream",
        "tool_domain": "slack",
        "requires_auth": True,
        "required_slots": ["channel", "text"],
        "optional_slots": [],
    },
    "gcal.create_event": {
        "provider": "pipedream",
        "tool_domain": "calendar",
        "requires_auth": True,
        "required_slots": ["title", "start_time", "duration_minutes", "timezone"],
        "optional_slots": ["attendees", "location", "description"],
    },
    "gmail.send_email": {
        "provider": "pipedream",
        "tool_domain": "email",
        "requires_auth": True,
        "required_slots": ["to", "subject", "body"],
        "optional_slots": ["cc", "bcc", "attachments"],
    },
    "jira.create_issue": {
        "provider": "pipedream",
        "tool_domain": "jira",
        "requires_auth": True,
        "required_slots": ["project", "issue_type", "summary"],
        "optional_slots": ["description", "priority", "labels", "assignee"],
    },
    "http.request": {
        "provider": "openapi",
        "tool_domain": "http",
        "requires_auth": False,
        "required_slots": ["method", "url"],
        "optional_slots": ["headers", "body"],
    },
}

# -----------------------------------------------------------------------------
# 3) Historical Routing Exemplars (the “training set”)
# -----------------------------------------------------------------------------
# Each exemplar encodes: intent phrasing + tool choice + required slots + policy context.

routing_exemplars = [
    # Slack message posting
    Concept(
        name="route_slack_post_001",
        attributes={
            "verb": "post",
            "object": "message",
            "domain": "slack",
            "time_ref": "none",
            "urgency": "none",
            "tool_id": "slack.post_message",
            "provider": "pipedream",
            "tool_domain": "slack",
            "requires_auth": "true",
            "required_slots": "channel,text",
            "optional_slots": "",
            "slot_values": "channel=#csm-alerts",
            "user_role": "csm",
            "tenant_segment": "prod",
            "constraints": "",
        },
    ),

    # Calendar scheduling
    Concept(
        name="route_calendar_create_001",
        attributes={
            "verb": "schedule",
            "object": "meeting",
            "domain": "calendar",
            "time_ref": "next_week",
            "urgency": "none",
            "tool_id": "gcal.create_event",
            "provider": "pipedream",
            "tool_domain": "calendar",
            "requires_auth": "true",
            "required_slots": "title,start_time,duration_minutes,timezone",
            "optional_slots": "attendees,location,description",
            "slot_values": "duration_minutes=30",
            "user_role": "manager",
            "tenant_segment": "prod",
            "constraints": "",
        },
    ),

    # Jira ticket creation
    Concept(
        name="route_jira_create_001",
        attributes={
            "verb": "create",
            "object": "ticket",
            "domain": "jira",
            "time_ref": "none",
            "urgency": "urgent",
            "tool_id": "jira.create_issue",
            "provider": "pipedream",
            "tool_domain": "jira",
            "requires_auth": "true",
            "required_slots": "project,issue_type,summary",
            "optional_slots": "description,priority,labels,assignee",
            "slot_values": "issue_type=bug",
            "user_role": "engineer",
            "tenant_segment": "prod",
            "constraints": "",
        },
    ),

    # Simple HTTP call (no auth)
    Concept(
        name="route_http_request_001",
        attributes={
            "verb": "fetch",
            "object": "url",
            "domain": "http",
            "time_ref": "none",
            "urgency": "none",
            "tool_id": "http.request",
            "provider": "openapi",
            "tool_domain": "http",
            "requires_auth": "false",
            "required_slots": "method,url",
            "optional_slots": "headers,body",
            "slot_values": "method=GET",
            "user_role": "admin",
            "tenant_segment": "dev",
            "constraints": "",
        },
    ),
]

print("\nEncoding routing exemplars...")
exemplar_glyphs = []
for ex in routing_exemplars:
    glyph = encoder.encode(ex)
    exemplar_glyphs.append(glyph)
    print(f"  ✓ {ex.name}")

# -----------------------------------------------------------------------------
# 4) Router Helpers (slot checks + auth checks)
# -----------------------------------------------------------------------------

def _missing_slots(tool_id: str, provided: dict) -> list[str]:
    required = TOOL_CATALOG[tool_id]["required_slots"]
    missing = []
    for slot in required:
        if slot not in provided or provided.get(slot) in (None, "", []):
            missing.append(slot)
    return missing

def _requires_auth(tool_id: str) -> bool:
    return bool(TOOL_CATALOG[tool_id]["requires_auth"])

def _build_ask(missing: list[str]) -> dict:
    # Keep it simple: minimal clarifying question
    if not missing:
        return {}
    if len(missing) == 1:
        q = f"What is the value for `{missing[0]}`?"
    else:
        q = "I need a bit more info: " + ", ".join([f"`{m}`" for m in missing]) + "."
    return {"question": q, "missing_slots": missing}

# -----------------------------------------------------------------------------
# 5) Route Function (Similarity → Tool Plan → State)
# -----------------------------------------------------------------------------

def route_tool(request: Concept, provided_slots: dict, context: dict):
    """
    Route a request to a tool based on similarity to exemplars.
    Returns a MCP-ready envelope-ish dict with:
    - state: DONE/ASK/AUTH_REQUIRED
    - confidence
    - payload: tool_plan or ask/auth instruction
    """
    print(f"\n{'='*60}")
    print(f"TOOL ROUTING: {request.name}")
    print('='*60)

    req_glyph = encoder.encode(request)

    # Similarity to exemplars
    scores = []
    for glyph in exemplar_glyphs:
        result = calculator.compute_similarity(req_glyph, glyph, edge_type="neural_cortex")
        scores.append(result.score)

    # Pick best exemplar / tool
    best_idx = max(range(len(scores)), key=lambda i: scores[i])
    best_score = scores[best_idx]
    best_exemplar = routing_exemplars[best_idx]
    tool_id = best_exemplar.attributes["tool_id"]

    # Normalize confidence to 0..1 (assuming similarity is already 0..1-ish)
    confidence = float(best_score)

    print(f"\nBest match: {best_exemplar.name}")
    print(f"Chosen tool: {tool_id}")
    print(f"Confidence: {confidence:.3f}")

    # 1) Policy gate placeholder (optional): block/ask if constraints mismatch
    # (In production, you’d evaluate policy facts here.)
    constraints = context.get("constraints", "")
    if "no_external_email" in constraints and tool_id == "gmail.send_email":
        return {
            "state": "BLOCKED",
            "confidence": confidence,
            "payload_type": "TOOL_PLAN",
            "payload": {"reason": "Policy blocks external email for this user/context."},
        }

    # 2) Auth check
    if _requires_auth(tool_id):
        # Here, the runtime would check if user has a connected account.
        # For demo, we accept context["has_auth"] boolean.
        if not context.get("has_auth", False):
            return {
                "state": "AUTH_REQUIRED",
                "confidence": confidence,
                "payload_type": "AUTH",
                "payload": {
                    "provider": TOOL_CATALOG[tool_id]["provider"],
                    "app": TOOL_CATALOG[tool_id]["tool_domain"],
                    "tool_id": tool_id,
                    "auth_hint": "Connect the required account via runtime auth service, then retry with session_id.",
                },
            }

    # 3) Slot completeness
    missing = _missing_slots(tool_id, provided_slots)
    if missing:
        ask = _build_ask(missing)
        return {
            "state": "ASK",
            "confidence": confidence,
            "payload_type": "ASK",
            "payload": {
                "tool_id": tool_id,
                "required_slots": TOOL_CATALOG[tool_id]["required_slots"],
                "provided_slots": list(provided_slots.keys()),
                **ask,
            },
        }

    # 4) EXECUTE-ready plan
    plan = {
        "plan_id": f"plan_{request.name}",
        "actions": [
            {
                "tool_ref": {
                    "provider": TOOL_CATALOG[tool_id]["provider"],
                    "id": tool_id,
                },
                "args": provided_slots,
            }
        ],
    }

    return {
        "state": "DONE",
        "confidence": confidence,
        "payload_type": "TOOL_PLAN",
        "payload": plan,
    }

# -----------------------------------------------------------------------------
# 6) Test Routing
# -----------------------------------------------------------------------------

print("\n" + "="*60)
print("TESTING TOOL ROUTING")
print("="*60)

test_requests = [
    # Slack request (missing channel -> ASK)
    Concept(
        name="req_001",
        attributes={
            "verb": "post",
            "object": "message",
            "domain": "slack",
            "time_ref": "none",
            "urgency": "none",
            # tool fields can be blank for the request; exemplars carry tool facts
            "tool_id": "",
            "provider": "",
            "tool_domain": "",
            "requires_auth": "",
            "required_slots": "",
            "optional_slots": "",
            "slot_values": "",
            "user_role": "csm",
            "tenant_segment": "prod",
            "constraints": "",
        },
    ),

    # Calendar scheduling (no auth -> AUTH_REQUIRED)
    Concept(
        name="req_002",
        attributes={
            "verb": "schedule",
            "object": "meeting",
            "domain": "calendar",
            "time_ref": "next_week",
            "urgency": "none",
            "tool_id": "",
            "provider": "",
            "tool_domain": "",
            "requires_auth": "",
            "required_slots": "",
            "optional_slots": "",
            "slot_values": "",
            "user_role": "manager",
            "tenant_segment": "prod",
            "constraints": "",
        },
    ),
]

# 1) Slack ASK case
result_1 = route_tool(
    request=test_requests[0],
    provided_slots={"text": "Churn report is ready."},   # missing channel
    context={"has_auth": True, "constraints": ""},
)
print("\nRESULT:", result_1)

# 2) Calendar AUTH_REQUIRED case
result_2 = route_tool(
    request=test_requests[1],
    provided_slots={"title": "Sync", "duration_minutes": 30, "timezone": "America/Chicago", "start_time": "next_week"},
    context={"has_auth": False, "constraints": ""},
)
print("\nRESULT:", result_2)

# -----------------------------------------------------------------------------
# 7) Export Model
# -----------------------------------------------------------------------------

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model = GlyphhModel(
    name="tool-router-model",
    version="1.0.0",
    encoder_config=config,
    glyphs=exemplar_glyphs,
    metadata={
        "domain": "agent_tooling",
        "description": "Tool routing using exemplar similarity + slot completeness + auth gating",
        "outputs": ["TOOL_PLAN", "ASK", "AUTH_REQUIRED"],
    }
)

model.to_file("tool-router-model.glyphh")
print("✓ Model exported to tool-router-model.glyphh")

# Cleanup
import os
if os.path.exists("tool-router-model.glyphh"):
    os.remove("tool-router-model.glyphh")

print("\n" + "="*60)
print("KEY PRINCIPLES")
print("="*60)
print("""
1. NO KEYWORD ROUTING - Let exemplars define routing patterns
2. TOOL FACTS AS DATA - Tool requirements are encoded (slots/auth/provider)
3. CORTEX SIMILARITY - Match requests to known successful routes
4. SAFE EXECUTION - ASK when slots missing, AUTH_REQUIRED when unconnected
5. TRACEABLE - Best exemplar match provides explainability via fact tree
""")
