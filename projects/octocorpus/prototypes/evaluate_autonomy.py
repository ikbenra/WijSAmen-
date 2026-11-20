"""Post-selection synthetic robustness audit. Scores never select policies.

The independent truth table specifies the existing toy task. Unseen continuous
observations jitter the eight binary patterns, preserving their latent labels.
This measures distribution-shift robustness, not a new biological capability.
Once observed, this audit is a regression suite, not a reusable blind test.
"""
import argparse
import copy
import hashlib
import json
import math
import random
import statistics
from pathlib import Path

from autonomy import BASE, KINDS, validate_state

# Independent task specification, intentionally not imported from examples().
ORACLE = {
    (0, 0, 0): 0, (0, 0, 1): 0, (0, 1, 0): 1, (0, 1, 1): 1,
    (1, 0, 0): 0, (1, 0, 1): 1, (1, 1, 0): 1, (1, 1, 1): 1,
}
SEEDS = tuple(range(13001, 13021))


def trials(seed):
    generator = random.Random(seed)
    cases = []
    for bits, target in ORACLE.items():
        for _ in range(32):
            observation = tuple(bit + generator.uniform(-0.2, 0.2) for bit in bits)
            cases.append((observation, target))
    generator.shuffle(cases)
    return cases


def accuracy(weights, cases):
    correct = 0
    for observation, target in cases:
        prediction = int(math.fsum(weight * value for weight, value in zip(weights, observation)) >= 2)
        correct += prediction == target
    return correct / len(cases)


def evaluate(state):
    """Freeze a validated snapshot before opening any post-selection cases."""
    validate_state(state)
    frozen = copy.deepcopy(state)
    policy_bytes = json.dumps(frozen["policies"], sort_keys=True).encode()
    rows = []
    for seed in SEEDS:
        cases = trials(seed)
        shuffled = [target for _, target in cases]
        random.Random(seed + 100000).shuffle(shuffled)
        negative = [(obs, target) for (obs, _), target in zip(cases, shuffled)]
        by_kind = {}
        for kind in KINDS:
            learned = accuracy(frozen["policies"][kind], cases)
            baseline = accuracy(BASE[kind], cases)
            by_kind[kind] = {
                "frozen_accuracy": learned,
                "fixed_accuracy": baseline,
                "delta": learned - baseline,
                "shuffled_label_accuracy": accuracy(frozen["policies"][kind], negative),
            }
        rows.append({"seed": seed, "cases": len(cases), "groups": by_kind})
    summaries = {}
    for kind in KINDS:
        deltas = [row["groups"][kind]["delta"] for row in rows]
        mean = statistics.mean(deltas)
        # Descriptive normal approximation across seed means, not IID examples.
        half_width = 1.96 * statistics.stdev(deltas) / math.sqrt(len(deltas))
        summaries[kind] = {
            "mean_delta": mean,
            "approx_95_interval": [mean - half_width, mean + half_width],
            "worse_seeds": sum(delta < 0 for delta in deltas),
        }
    return {
        "schema": "octocorpus.postselection-audit.v1",
        "policy_sha256": hashlib.sha256(policy_bytes).hexdigest(),
        "generation": frozen["generation"],
        "selection_feedback": False,
        "training_validation_gate": "legacy two-point selection gate",
        "scope": "synthetic amplitude shift; independent labels, same toy semantics",
        "energy": {"measured_joules": None, "model": "not estimated"},
        "ablation": "fixed initial policy (optimizer disabled)",
        "n_and_overlay_ablation": "not implemented in this optimizer",
        "constant_zero_accuracy": 3 / 8,
        "constant_one_accuracy": 5 / 8,
        "total_cases": sum(row["cases"] for row in rows),
        "summary": summaries,
        "rows": rows,
        "limitations": ["one task truth table", "seeds vary sensor amplitudes only",
                        "normal intervals are descriptive", "future tuning requires a new final suite"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    state = json.loads(Path(args.state).read_text(encoding="utf-8"))
    result = evaluate(state)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("policy_sha256", "total_cases", "summary")}))


if __name__ == "__main__":
    main()
