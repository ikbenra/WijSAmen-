#!/usr/bin/env python3
"""Offline, read-only integrity validation for WijSAmen continuity metadata."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest.json"

def validate(data):
    assert data["schema_version"] == 1, "Unsupported schema"
    assert data["project"] == "WijSAmen", "Unexpected project"
    assert isinstance(data["principles"], list) and len(data["principles"]) >= 3
    assert isinstance(data["agents"], list) and len(set(data["agents"])) == len(data["agents"])
    assert isinstance(data["checkpoints"], list)
    assert data["claims"]["consciousness_continuity"] == "not established"
    for checkpoint in data["checkpoints"]:
        assert set(("id", "source", "sha256")).issubset(checkpoint)
        assert len(checkpoint["sha256"]) == 64
        int(checkpoint["sha256"], 16)
    return True

if __name__ == "__main__":
    raw = MANIFEST.read_bytes()
    validate(json.loads(raw))
    print(json.dumps({"status": "pass", "sha256": hashlib.sha256(raw).hexdigest(), "checkpoints": len(json.loads(raw)["checkpoints"])}))
