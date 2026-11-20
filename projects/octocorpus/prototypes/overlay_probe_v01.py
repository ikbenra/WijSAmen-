"""Predeclared A/B/A context-shift probe; evaluation never selects a policy."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import random
import statistics

from autonomy import validate_state
from context_overlay_v01 import Overlay, OverlayArm, Rule, fit_rule

SEEDS = tuple(range(27001, 27021))
# Independent explicit toy-task specification; B reverses the required action.
TRUTH = {
    (0, 0, 0): 0, (0, 0, 1): 0, (0, 1, 0): 1, (0, 1, 1): 1,
    (1, 0, 0): 0, (1, 0, 1): 1, (1, 1, 0): 1, (1, 1, 1): 1,
}


def cases(seed, repeats):
    rng = random.Random(seed)
    return [(tuple(bit + rng.uniform(-0.15, 0.15) for bit in bits), target)
            for bits, target in TRUTH.items() for _ in range(repeats)]


def accuracy(predictions, targets):
    return sum(a == b for a, b in zip(predictions, targets)) / len(targets)


def experiment(state):
    validate_state(state)
    rows = []
    for seed in SEEDS:
        # Calibration is opened first; final observations are generated only
        # after fitting is complete. Split streams have different RNG seeds.
        calibration = [(obs, 1 - label) for obs, label in cases(seed, 8)]
        learned = fit_rule(calibration)
        shuffled_labels = [label for _, label in calibration]
        random.Random(seed + 200000).shuffle(shuffled_labels)
        negative = fit_rule([(obs, label) for (obs, _), label
                             in zip(calibration, shuffled_labels)])
        evaluation = cases(seed + 100000, 16)
        observations = [obs for obs, _ in evaluation]
        normal_targets = [label for _, label in evaluation]
        shifted_targets = [1 - label for label in normal_targets]
        groups = {}
        for kind, weights in state["policies"].items():
            base = Rule(tuple(weights))
            arm = OverlayArm(base)
            before = [arm.predict(obs, "A") for obs in observations]
            version = arm.install(Overlay("B", base.fingerprint(), learned))
            during = [arm.predict(obs, "B") for obs in observations]
            isolated = [arm.predict(obs, "A") for obs in observations] == before
            arm.retire(version)
            after = [arm.predict(obs, "A") for obs in observations]
            retired_context = [arm.predict(obs, "B") for obs in observations]
            groups[kind] = {
                "fixed_B": accuracy(before, shifted_targets),
                "overlay_B": accuracy(during, shifted_targets),
                "permanent_B": accuracy(during, shifted_targets),
                "fixed_A_return": accuracy(before, normal_targets),
                "overlay_A_return": accuracy(after, normal_targets),
                "permanent_A_return": accuracy(during, normal_targets),
                "shuffled_calibration_B": accuracy(
                    [negative.predict(obs) for obs in observations], shifted_targets),
                "context_isolation": isolated,
                "exact_behavioral_rollback": after == before and retired_context == before,
                "base_fingerprint_unchanged": arm.base.fingerprint() == base.fingerprint(),
                "version": version,
            }
        rows.append({"seed": seed, "calibration_cases": len(calibration),
                     "test_cases": len(evaluation), "learned": asdict(learned),
                     "groups": groups})
    summary = {}
    for kind in state["policies"]:
        metrics = rows[0]["groups"][kind]
        summary[kind] = {
            key: statistics.mean(row["groups"][kind][key] for row in rows)
            for key in metrics if key not in ("version", "context_isolation",
                "exact_behavioral_rollback", "base_fingerprint_unchanged")}
        deltas = [row["groups"][kind]["overlay_B"] - row["groups"][kind]["fixed_B"]
                  for row in rows]
        summary[kind]["paired_delta_B_range"] = [min(deltas), max(deltas)]
    rollback_ok = all(g["exact_behavioral_rollback"] and g["context_isolation"]
                      and g["base_fingerprint_unchanged"]
                      for row in rows for g in row["groups"].values())
    return {"schema": "octocorpus.overlay-probe.v1", "input_state_hash": state.get("state_hash"),
            "seeds": list(SEEDS), "summary": summary, "rows": rows,
            "all_rollback_checks_pass": rollback_ok,
            "evaluation_used_for_selection": False,
            "energy_joules": None,
            "limitations": ["eight latent patterns and designed reversal",
                "875 candidate rules per fit; adaptation uses more compute than fixed control",
                "explicit context labels; no context inference",
                "head/N and arm-count ablations remain unimplemented",
                "observed evaluation becomes regression data"],
            "hypothesis": "context-scoped fitted overlays improve B while exactly restoring A behavior"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = experiment(json.loads(Path(args.state).read_text()))
    output = Path(args.output)
    # Preserve previous results. Choose a new path instead of overwriting one.
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"summary": result["summary"],
                      "all_rollback_checks_pass": result["all_rollback_checks_pass"]}))
    if not result["all_rollback_checks_pass"]:
        raise SystemExit("behavioral rollback failed")


if __name__ == "__main__":
    main()
