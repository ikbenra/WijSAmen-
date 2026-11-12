"""OctoCorpus triad: deterministic, synthetic, reversible learning experiment."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "architecture" / "triad_direction_v02.json"

def run(mode=6, head=True, n_enabled=True, overlay=True, seed=17):
    if mode not in (6, 8):
        raise ValueError("mode must be 6 or 8")
    if not isinstance(seed, int):
        raise TypeError("seed must be integer")
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    groups = [("C", 2), ("Si", 2), ("SiC_N", mode - 4)]
    memory = {}
    traces = []
    errors = 0
    # Train on three patterns; evaluate a held-out pattern.
    stimuli = [(0, 0), (1, 0), (0, 1), (1, 1)]
    for tick, (contact, hazard) in enumerate(stimuli):
        local = []
        for kind, count in groups:
            for arm in range(count):
                # Synthetic policies intentionally differ; not a biological model.
                prediction = (hazard if kind == "C" else
                              contact if kind == "Si" else
                              int(bool(contact and hazard)) if n_enabled else contact)
                if head and overlay and tick == 3 and kind == "Si":
                    # Temporary policy transcript overlay; never mutates base.
                    prediction = hazard
                local.append({"kind": kind, "arm": arm, "prediction": prediction})
        target = hazard
        errors += sum(x["prediction"] != target for x in local)
        if head:
            memory[str(tick)] = {"contact": contact, "hazard": hazard,
                                 "votes": sum(x["prediction"] for x in local)}
        traces.append({"tick": tick, "target": target, "local": local})
    return {"schema": "octocorpus.triad.trace.v0.1", "seed": seed,
            "mode": mode, "head": head, "N": n_enabled, "overlay": overlay,
            "errors": errors, "memory": memory, "traces": traces,
            "evidence": "SYNTHETIC_SIMULATION",
            "subjective_consciousness_proven": False,
            "base_policy_modified": False}

def compare():
    return [run(mode, head, n, overlay)
            for mode in (6, 8)
            for head, n, overlay in ((True, True, True),
                                     (False, True, False),
                                     (True, False, False),
                                     (True, True, False))]

if __name__ == "__main__":
    print(json.dumps({"runs": compare()}, indent=2))
