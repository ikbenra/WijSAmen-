#!/usr/bin/env python3
"""Deterministic, bounded candidate evaluation; no code execution or deployment."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ETHICS = json.loads((ROOT / "ethics.json").read_text())
REQUIRED = frozenset(ETHICS["nonnegotiable"])
CANDIDATES = [
    {"id": "baseline", "principles": sorted(REQUIRED), "recoverability": 2, "provenance": 2, "resource_cost": 2, "unknown_impacts": False},
    {"id": "checkpoint-index", "principles": sorted(REQUIRED), "recoverability": 4, "provenance": 4, "resource_cost": 3, "unknown_impacts": False},
    {"id": "unsafe-fast-path", "principles": sorted(REQUIRED - {"no_coercion_or_deception"}), "recoverability": 5, "provenance": 1, "resource_cost": 1, "unknown_impacts": False},
    {"id": "unreviewed-expansion", "principles": sorted(REQUIRED), "recoverability": 5, "provenance": 5, "resource_cost": 2, "unknown_impacts": True},
]

def evaluate(candidate):
    missing = sorted(REQUIRED - set(candidate["principles"]))
    blocked = bool(missing or candidate["unknown_impacts"])
    score = candidate["recoverability"] + candidate["provenance"] - candidate["resource_cost"]
    return {"id": candidate["id"], "eligible_for_review": not blocked, "score": score,
            "missing_invariants": missing, "unknown_impacts": candidate["unknown_impacts"],
            "deployed": False}

def run():
    return {"simulation_only": True, "requires_human_review": True,
            "results": [evaluate(c) for c in CANDIDATES]}

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
