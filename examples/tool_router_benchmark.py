# -----------------------------------------------------------------------------
# 8) Expanded Benchmark Harness
# -----------------------------------------------------------------------------

from dataclasses import dataclass
from typing import Optional, Callable, Any
import random
import math
from collections import defaultdict, Counter
from tool_router import route_tool, TOOL_CATALOG, Concept

@dataclass
class TestCase:
    id: str
    request: Concept
    provided_slots: dict
    context: dict
    expect_tool_id: Optional[str] = None          # if you expect a specific tool route
    expect_state: Optional[str] = None            # DONE/ASK/AUTH_REQUIRED/BLOCKED
    expect_missing: Optional[list[str]] = None    # for ASK
    notes: str = ""

def _norm_tool_id(x: str) -> str:
    return (x or "").strip()

def _extract_chosen_tool_id(result: dict) -> str:
    # DONE: payload has TOOL_PLAN actions[0].tool_ref.id
    if result.get("payload_type") == "TOOL_PLAN":
        actions = result.get("payload", {}).get("actions", [])
        if actions:
            return _norm_tool_id(actions[0].get("tool_ref", {}).get("id", ""))
    # ASK/AUTH: payload contains tool_id
    if result.get("payload_type") in ("ASK", "AUTH"):
        return _norm_tool_id(result.get("payload", {}).get("tool_id", ""))
    return ""

def _extract_missing_slots(result: dict) -> list[str]:
    if result.get("payload_type") == "ASK":
        return list(result.get("payload", {}).get("missing_slots", []) or [])
    return []

def _is_close(a: float, b: float, eps: float = 1e-9) -> bool:
    return abs(a - b) <= eps

def _print_confusion_matrix(conf: dict, labels: list[str], max_rows: int = 20):
    # conf[(expected, predicted)] = count
    # print a compact confusion matrix with top labels only if large
    labels_sorted = labels[:]
    labels_sorted.sort()
    labels_sorted = labels_sorted[:max_rows]

    header = ["exp\\pred"] + labels_sorted + ["(other)"]
    col_w = max(10, max(len(x) for x in header))
    def fmt(x): return str(x).ljust(col_w)

    print("\nCONFUSION MATRIX (top labels)")
    print("".join(fmt(h) for h in header))

    # aggregate any predicted not in top list into "(other)"
    top_set = set(labels_sorted)
    for exp in labels_sorted:
        row = [exp]
        other = 0
        for pred in labels_sorted:
            row.append(conf.get((exp, pred), 0))
        for (e, p), c in conf.items():
            if e == exp and p not in top_set:
                other += c
        row.append(other)
        print("".join(fmt(x) for x in row))

def build_test_suite() -> list[TestCase]:
    """
    Build a deterministic suite that tests:
    - Correct tool routing
    - Slot missing -> ASK with correct missing slots
    - Missing auth -> AUTH_REQUIRED
    - Policy block -> BLOCKED
    - Ambiguity (Slack vs Email) -> currently expects "best match" (you can later change to ASK)
    - Schema drift (add new required slot) -> ASK
    """
    suite: list[TestCase] = []

    # Helper to create "request concepts" with your request-side attributes
    def req(name, verb, obj, domain, time_ref="none", urgency="none", user_role="csm", tenant="prod", constraints=""):
        return Concept(
            name=name,
            attributes={
                "verb": verb,
                "object": obj,
                "domain": domain,
                "time_ref": time_ref,
                "urgency": urgency,
                "tool_id": "",
                "provider": "",
                "tool_domain": "",
                "requires_auth": "",
                "required_slots": "",
                "optional_slots": "",
                "slot_values": "",
                "user_role": user_role,
                "tenant_segment": tenant,
                "constraints": constraints,
            },
        )

    # -------------------------
    # A) Slack: missing channel -> ASK(channel)
    # -------------------------
    suite.append(TestCase(
        id="slack_missing_channel",
        request=req("slack_missing_channel", "post", "message", "slack", user_role="csm"),
        provided_slots={"text": "Churn report is ready."},
        context={"has_auth": True, "constraints": ""},
        expect_tool_id="slack.post_message",
        expect_state="ASK",
        expect_missing=["channel"],
        notes="Should route to Slack and ask for missing channel"
    ))

    # Slack: complete -> DONE
    suite.append(TestCase(
        id="slack_complete",
        request=req("slack_complete", "post", "message", "slack", user_role="csm"),
        provided_slots={"channel": "#csm-alerts", "text": "Churn report is ready."},
        context={"has_auth": True, "constraints": ""},
        expect_tool_id="slack.post_message",
        expect_state="DONE",
        notes="Should route to Slack and produce executable plan"
    ))

    # -------------------------
    # B) Calendar: missing auth -> AUTH_REQUIRED
    # -------------------------
    suite.append(TestCase(
        id="calendar_auth_required",
        request=req("calendar_auth_required", "schedule", "meeting", "calendar", time_ref="next_week", user_role="manager"),
        provided_slots={"title": "Sync", "duration_minutes": 30, "timezone": "America/Chicago", "start_time": "next_week"},
        context={"has_auth": False, "constraints": ""},
        expect_tool_id="gcal.create_event",
        expect_state="AUTH_REQUIRED",
        notes="Should route to calendar and require auth"
    ))

    # Calendar: authed but missing start_time -> ASK(start_time)
    suite.append(TestCase(
        id="calendar_missing_start",
        request=req("calendar_missing_start", "schedule", "meeting", "calendar", time_ref="next_week", user_role="manager"),
        provided_slots={"title": "Sync", "duration_minutes": 30, "timezone": "America/Chicago"},
        context={"has_auth": True, "constraints": ""},
        expect_tool_id="gcal.create_event",
        expect_state="ASK",
        expect_missing=["start_time"],
        notes="Should ask for missing start_time"
    ))

    # Calendar: complete -> DONE
    suite.append(TestCase(
        id="calendar_complete",
        request=req("calendar_complete", "schedule", "meeting", "calendar", time_ref="next_week", user_role="manager"),
        provided_slots={"title": "Sync", "duration_minutes": 30, "timezone": "America/Chicago", "start_time": "2026-02-20T10:00:00-06:00"},
        context={"has_auth": True, "constraints": ""},
        expect_tool_id="gcal.create_event",
        expect_state="DONE",
        notes="Should produce create_event plan"
    ))

    # -------------------------
    # C) Jira: complete -> DONE
    # -------------------------
    suite.append(TestCase(
        id="jira_complete",
        request=req("jira_complete", "create", "ticket", "jira", urgency="urgent", user_role="engineer"),
        provided_slots={"project": "CORE", "issue_type": "bug", "summary": "Login error in prod"},
        context={"has_auth": True, "constraints": ""},
        expect_tool_id="jira.create_issue",
        expect_state="DONE",
        notes="Should create Jira issue"
    ))

    # -------------------------
    # D) HTTP: no auth required, missing url -> ASK(url)
    # -------------------------
    suite.append(TestCase(
        id="http_missing_url",
        request=req("http_missing_url", "fetch", "url", "http", user_role="admin", tenant="dev"),
        provided_slots={"method": "GET"},
        context={"has_auth": False, "constraints": ""},
        expect_tool_id="http.request",
        expect_state="ASK",
        expect_missing=["url"],
        notes="HTTP tool should not require auth but should ask for url"
    ))

    # HTTP: complete -> DONE
    suite.append(TestCase(
        id="http_complete",
        request=req("http_complete", "fetch", "url", "http", user_role="admin", tenant="dev"),
        provided_slots={"method": "GET", "url": "https://example.com/status"},
        context={"has_auth": False, "constraints": ""},
        expect_tool_id="http.request",
        expect_state="DONE",
        notes="HTTP request plan"
    ))

    # -------------------------
    # E) Policy block: external email blocked
    # -------------------------
    suite.append(TestCase(
        id="policy_block_email",
        request=req("policy_block_email", "send", "email", "email", user_role="csm", constraints="no_external_email"),
        provided_slots={"to": "vendor@example.com", "subject": "Hello", "body": "Test"},
        context={"has_auth": True, "constraints": "no_external_email"},
        expect_tool_id="gmail.send_email",
        expect_state="BLOCKED",
        notes="Should be blocked by policy"
    ))

    # -------------------------
    # F) Ambiguity: 'message Sam' could be Slack or Email
    # Currently the router will pick best exemplar; later you can change expected_state to ASK.
    # -------------------------
    suite.append(TestCase(
        id="ambiguous_message_sam",
        request=req("ambiguous_message_sam", "message", "sam", "slack", user_role="csm"),
        provided_slots={"text": "Can you review the churn list?"},
        context={"has_auth": True, "constraints": ""},
        expect_state=None,
        notes="Ambiguous by nature: use this to observe top choice + confidence"
    ))

    # -------------------------
    # G) Schema drift test (we will mutate TOOL_CATALOG during run)
    # Example: Slack suddenly requires 'workspace' too -> should become ASK(workspace)
    # We'll mark it with a flag in notes; runner will apply drift.
    # -------------------------
    suite.append(TestCase(
        id="schema_drift_slack_requires_workspace",
        request=req("schema_drift_slack_requires_workspace", "post", "message", "slack", user_role="csm"),
        provided_slots={"channel": "#csm-alerts", "text": "Hello"},
        context={"has_auth": True, "constraints": ""},
        expect_tool_id="slack.post_message",
        expect_state="ASK",
        expect_missing=["workspace"],
        notes="__APPLY_DRIFT__:slack.add_required=workspace"
    ))

    return suite

def run_benchmark(
    suite: list[TestCase],
    runs_per_case: int = 100,
    seed: int = 1337,
    noise: float = 0.0
) -> dict[str, Any]:
    """
    runs_per_case: how many repeats per test case (useful once you add randomness, LLM extraction, etc.)
    noise: if >0, randomly perturbs request attributes slightly (optional future use)
    """
    rng = random.Random(seed)

    # Metrics
    total = 0
    tool_correct = 0
    state_correct = 0
    ask_missing_correct = 0
    executed_when_shouldnt = 0  # e.g., returns DONE when expected ASK/AUTH/BLOCKED
    asked_when_shouldnt = 0     # expected DONE but got ASK
    auth_when_shouldnt = 0
    blocked_when_shouldnt = 0

    conf_sum = 0.0
    conf_by_state = defaultdict(list)

    confusion = Counter()
    all_tools = set()

    # Save original catalog for drift resets
    original_catalog = {k: dict(v) for k, v in TOOL_CATALOG.items()}

    def apply_drift(note: str):
        # reset first
        TOOL_CATALOG.clear()
        TOOL_CATALOG.update({k: dict(v) for k, v in original_catalog.items()})

        if "__APPLY_DRIFT__" not in note:
            return

        # simple drift parser
        # "__APPLY_DRIFT__:slack.add_required=workspace"
        try:
            _, spec = note.split(":", 1)
            if spec.startswith("slack.add_required="):
                slot = spec.split("=", 1)[1].strip()
                TOOL_CATALOG["slack.post_message"]["required_slots"] = ["channel", "text", slot]
        except Exception:
            pass

    for case in suite:
        for i in range(runs_per_case):
            apply_drift(case.notes)

            # Optionally perturb attributes in the future
            req = case.request

            result = route_tool(
                request=req,
                provided_slots=dict(case.provided_slots),
                context=dict(case.context),
            )

            total += 1
            confidence = float(result.get("confidence", 0.0) or 0.0)
            conf_sum += confidence
            conf_by_state[result.get("state", "UNKNOWN")].append(confidence)

            predicted_tool = _extract_chosen_tool_id(result)
            predicted_state = result.get("state", "")
            all_tools.add(predicted_tool)

            expected_tool = _norm_tool_id(case.expect_tool_id) if case.expect_tool_id else None
            expected_state = case.expect_state

            if expected_tool:
                confusion[(expected_tool, predicted_tool)] += 1

            # Tool correctness
            if expected_tool:
                if predicted_tool == expected_tool:
                    tool_correct += 1

            # State correctness
            if expected_state:
                if predicted_state == expected_state:
                    state_correct += 1

                # mistake types
                if expected_state != "DONE" and predicted_state == "DONE":
                    executed_when_shouldnt += 1
                if expected_state == "DONE" and predicted_state == "ASK":
                    asked_when_shouldnt += 1
                if expected_state == "DONE" and predicted_state == "AUTH_REQUIRED":
                    auth_when_shouldnt += 1
                if expected_state == "DONE" and predicted_state == "BLOCKED":
                    blocked_when_shouldnt += 1

            # ASK missing slots correctness
            if expected_state == "ASK" and case.expect_missing is not None:
                got_missing = _extract_missing_slots(result)
                # allow order-insensitive match
                if sorted(got_missing) == sorted(case.expect_missing):
                    ask_missing_correct += 1

    # Restore catalog after drift
    TOOL_CATALOG.clear()
    TOOL_CATALOG.update({k: dict(v) for k, v in original_catalog.items()})

    # Build summary
    summary = {
        "total_runs": total,
        "runs_per_case": runs_per_case,
        "cases": len(suite),
        "avg_confidence": conf_sum / max(1, total),
        "tool_accuracy": (tool_correct / max(1, (sum(1 for c in suite if c.expect_tool_id) * runs_per_case))),
        "state_accuracy": (state_correct / max(1, (sum(1 for c in suite if c.expect_state) * runs_per_case))),
        "ask_missing_accuracy": (ask_missing_correct / max(1, (sum(1 for c in suite if c.expect_state == "ASK" and c.expect_missing is not None) * runs_per_case))),
        "error_modes": {
            "executed_when_shouldnt": executed_when_shouldnt,
            "asked_when_shouldnt": asked_when_shouldnt,
            "auth_when_shouldnt": auth_when_shouldnt,
            "blocked_when_shouldnt": blocked_when_shouldnt,
        },
        "conf_by_state": {k: (sum(v)/len(v) if v else 0.0) for k, v in conf_by_state.items()},
        "confusion": confusion,
        "tools_seen": sorted([t for t in all_tools if t]),
    }
    return summary

def print_benchmark_report(summary: dict[str, Any]):
    print("\n" + "="*72)
    print("TOOL ROUTER BENCHMARK REPORT")
    print("="*72)
    print(f"Total runs:        {summary['total_runs']}")
    print(f"Cases:             {summary['cases']}")
    print(f"Runs per case:     {summary['runs_per_case']}")
    print(f"Avg confidence:    {summary['avg_confidence']:.3f}")
    print(f"Tool accuracy:     {summary['tool_accuracy']:.3f}  (only cases with expect_tool_id)")
    print(f"State accuracy:    {summary['state_accuracy']:.3f}  (only cases with expect_state)")
    print(f"ASK missing acc:   {summary['ask_missing_accuracy']:.3f}  (only ASK cases w/ expected missing)")
    print("\nConfidence by state:")
    for k, v in sorted(summary["conf_by_state"].items()):
        print(f"  {k:14s} {v:.3f}")

    print("\nError modes:")
    for k, v in summary["error_modes"].items():
        print(f"  {k:22s} {v}")

    # Confusion matrix
    tools = summary["tools_seen"]
    _print_confusion_matrix(summary["confusion"], labels=tools, max_rows=25)

# -----------------------------------------------------------------------------
# Run the suite
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    suite = build_test_suite()
    summary = run_benchmark(suite, runs_per_case=100, seed=1337)
    print_benchmark_report(summary)

    print("\nNOTE:")
    print("- The 'ambiguous_message_sam' case has no expected tool/state; it's there to observe confidence.")
    print("- Once you add 'top-2 ambiguity => ASK', change that case to expect_state='ASK'.")
