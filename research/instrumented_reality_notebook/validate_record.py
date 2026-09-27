#!/usr/bin/env python3
"""Validate an Instrumented Reality Notebook record and emit a hash receipt.

This utility checks documentation completeness. It never authorizes physical
execution or certifies safety.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "instrumented-reality-notebook-v0.1"
EVIDENCE_STATES = {
    "SOURCE_PENDING",
    "OBSERVATION_ONLY",
    "CONTROL_PLAN_FROZEN",
    "OBSERVED_WITH_CONTROLS",
    "INDEPENDENTLY_REPRODUCED",
}
REQUIRED_SECTIONS = (
    "provenance",
    "observation",
    "apparatus_identity",
    "energy_inventory",
    "environment",
    "independent_observation",
    "controls",
    "prediction",
    "authority",
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("record root must be an object")
    return value


def missing_text(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def validate(record: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    blockers: list[str] = []

    if record.get("schema") != SCHEMA:
        errors.append(f"schema must equal {SCHEMA}")
    for field in ("record_id", "title", "evidence_state"):
        if missing_text(record.get(field)):
            errors.append(f"{field} is required")
    for section in REQUIRED_SECTIONS:
        if not isinstance(record.get(section), dict):
            errors.append(f"{section} must be an object")

    state = record.get("evidence_state")
    if state not in EVIDENCE_STATES:
        errors.append("evidence_state is not recognized")

    observation = record.get("observation", {})
    if missing_text(observation.get("literal")):
        errors.append("observation.literal is required")
    if missing_text(observation.get("interpretation")):
        errors.append("observation.interpretation is required and must remain separate")

    prediction = record.get("prediction", {})
    for field in ("measurable_prediction", "alternative_explanation", "disconfirming_outcome"):
        if missing_text(prediction.get(field)):
            errors.append(f"prediction.{field} is required")

    stops = record.get("stop_conditions")
    if not isinstance(stops, list) or not any(isinstance(item, str) and item.strip() for item in stops):
        errors.append("at least one stop condition is required")

    apparatus = record.get("apparatus_identity", {})
    energy = record.get("energy_inventory", {})
    authority = record.get("authority", {})
    if apparatus.get("status") != "EXACT_VERIFIED":
        blockers.append("apparatus identity is not exact and verified")
    if energy.get("state") != "DEENERGIZED_VERIFIED":
        blockers.append("de-energized state is not verified")
    if not energy.get("stored_energy_checked"):
        blockers.append("stored energy has not been checked")
    if authority.get("physical_action_requested"):
        blockers.append("physical action requires separate human authority and competent safety review")
    if authority.get("owner_permission") != "VERIFIED":
        blockers.append("owner permission is not verified")
    if authority.get("competent_safety_review") != "VERIFIED":
        blockers.append("competent safety review is not verified")

    documentation_status = "COMPLETE_FOR_REVIEW" if not errors else "INCOMPLETE"
    receipt_core = {
        "schema": SCHEMA,
        "record_id": record.get("record_id"),
        "record_sha256": hashlib.sha256(canonical_bytes(record)).hexdigest(),
        "documentation_status": documentation_status,
        "errors": errors,
        "physical_action_blockers": blockers,
        "action_gate": "NOT_AUTHORIZED_BY_THIS_TOOL",
    }
    return {**receipt_core, "receipt_sha256": hashlib.sha256(canonical_bytes(receipt_core)).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    receipt = validate(load(args.record))
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{receipt['documentation_status']} / {receipt['action_gate']} / {receipt['receipt_sha256']}")
    return 0 if receipt["documentation_status"] == "COMPLETE_FOR_REVIEW" else 2


if __name__ == "__main__":
    raise SystemExit(main())
