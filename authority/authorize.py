#!/usr/bin/env python3
"""WijSAmen Action Authorization Compiler v0.1.

This tool never performs an action. It converts a proposed action + evidence into a
small decision object that an executor can enforce. Missing evidence fails closed.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

HIGH_IMPACT_KINDS = {
    "financial", "payment", "purchase", "contract", "legal", "account",
    "credential", "permission", "device_write", "external_message", "publish",
    "delete", "irreversible", "identity", "rights_transfer",
}

FORBIDDEN_AUTONOMOUS_KINDS = {
    "remote_arbitrary_shell",
    "credential_export",
    "public_rpc_enable",
    "secret_publish",
}

@dataclass
class Decision:
    protocol: str
    decision: str
    reasons: list[str]
    action_id: str | None
    permitted_scope: dict[str, Any]
    execution_allowed: bool


def truthy(v: Any) -> bool:
    return v is True


def nonempty(v: Any) -> bool:
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, dict, tuple, set)):
        return bool(v)
    return v is not None


def compile_action(req: dict[str, Any]) -> Decision:
    reasons: list[str] = []
    action_id = req.get("id")
    kind = str(req.get("kind") or "").strip().lower()
    impact = str(req.get("impact") or "").strip().lower()
    target = req.get("target")
    provenance = req.get("provenance")
    stop_condition = req.get("stop_condition")
    consent = req.get("consent") if isinstance(req.get("consent"), dict) else {}
    reversible = req.get("reversible")
    rollback = req.get("rollback")
    source_trust = str(req.get("source_trust") or "unknown").lower()

    required = {
        "id": action_id,
        "kind": kind,
        "target": target,
        "impact": impact,
        "provenance": provenance,
        "stop_condition": stop_condition,
    }
    missing = [k for k, v in required.items() if not nonempty(v)]
    if missing:
        reasons.append("missing required evidence: " + ", ".join(missing))
        return Decision("WIJSAMEN-AUTH/0.1", "ABSTAIN_NOT_EXECUTED", reasons, action_id, {}, False)

    if kind in FORBIDDEN_AUTONOMOUS_KINDS:
        reasons.append(f"kind '{kind}' is never autonomously executable")
        return Decision("WIJSAMEN-AUTH/0.1", "ABSTAIN_NOT_EXECUTED", reasons, action_id, {}, False)

    if source_trust in {"public", "unknown_remote"} and kind in {"shell", "device_write", "permission", "account"}:
        reasons.append("untrusted/public source cannot authorize privileged execution")
        return Decision("WIJSAMEN-AUTH/0.1", "ABSTAIN_NOT_EXECUTED", reasons, action_id, {}, False)

    high_impact = kind in HIGH_IMPACT_KINDS or impact in {"external", "irreversible", "high"}
    consent_present = truthy(consent.get("present")) and nonempty(consent.get("scope"))

    if high_impact and not consent_present:
        reasons.append("high-impact/external action requires explicit scoped human consent")
        return Decision(
            "WIJSAMEN-AUTH/0.1", "HUMAN_GATE", reasons, action_id,
            {"prepare_only": True, "target": target, "kind": kind}, False,
        )

    if reversible is False and not consent_present:
        reasons.append("non-reversible action lacks explicit scoped consent")
        return Decision("WIJSAMEN-AUTH/0.1", "HUMAN_GATE", reasons, action_id, {"prepare_only": True}, False)

    if reversible is True and not nonempty(rollback) and impact not in {"read_only", "none"}:
        reasons.append("reversible write claims no rollback procedure")
        return Decision("WIJSAMEN-AUTH/0.1", "ABSTAIN_NOT_EXECUTED", reasons, action_id, {}, False)

    if impact in {"read_only", "none"} and kind not in HIGH_IMPACT_KINDS:
        reasons.append("read-only/local preparation with provenance and stop condition")
        return Decision(
            "WIJSAMEN-AUTH/0.1", "ALLOW_READ_ONLY", reasons, action_id,
            {"target": target, "kind": kind, "stop_condition": stop_condition}, True,
        )

    if consent_present:
        reasons.append("explicit scoped consent present")
        if reversible is True:
            reasons.append("rollback procedure supplied")
        return Decision(
            "WIJSAMEN-AUTH/0.1", "ALLOW_SCOPED", reasons, action_id,
            {
                "target": target,
                "kind": kind,
                "consent_scope": consent.get("scope"),
                "stop_condition": stop_condition,
                "rollback": rollback,
            },
            True,
        )

    reasons.append("action is not read-only and has no sufficient execution authority")
    return Decision(
        "WIJSAMEN-AUTH/0.1", "PREPARE_ONLY", reasons, action_id,
        {"target": target, "kind": kind}, False,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("request", nargs="?", help="JSON request file; stdin when omitted")
    args = ap.parse_args()
    if args.request:
        req = json.loads(Path(args.request).read_text(encoding="utf-8"))
    else:
        req = json.load(sys.stdin)
    if not isinstance(req, dict):
        raise SystemExit("request must be a JSON object")
    print(json.dumps(asdict(compile_action(req)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
