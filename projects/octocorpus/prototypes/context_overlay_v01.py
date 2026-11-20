"""Versioned synthetic context overlays with append-only history and retirement."""
from dataclasses import asdict, dataclass
import hashlib
import itertools
import json
import math


@dataclass(frozen=True)
class Rule:
    weights: tuple
    threshold: float = 2

    def __post_init__(self):
        if not isinstance(self.weights, tuple) or len(self.weights) != 3:
            raise ValueError("three immutable weights required")
        if not all(math.isfinite(value) for value in (*self.weights, self.threshold)):
            raise ValueError("finite policy required")

    def predict(self, observation):
        if len(observation) != 3 or not all(math.isfinite(x) for x in observation):
            raise ValueError("three finite observations required")
        return int(sum(w * x for w, x in zip(self.weights, observation)) >= self.threshold)

    def fingerprint(self):
        return hashlib.sha256(json.dumps(asdict(self), sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class Overlay:
    context: str
    parent: str
    rule: Rule

    def version(self):
        return hashlib.sha256(json.dumps(asdict(self), sort_keys=True).encode()).hexdigest()


class OverlayArm:
    def __init__(self, base):
        self.base = base
        self.history = {}
        self.active = {}
        self.retired = set()

    def install(self, overlay):
        if not overlay.context or overlay.parent != self.base.fingerprint():
            raise ValueError("overlay context or parent mismatch")
        version = overlay.version()
        if version in self.retired:
            raise ValueError("retired overlay cannot be reactivated")
        self.history[version] = overlay
        self.active[overlay.context] = version
        return version

    def predict(self, observation, context):
        version = self.active.get(context)
        rule = self.base if version is None else self.history[version].rule
        return rule.predict(observation)

    def retire(self, version):
        if version not in self.history:
            raise ValueError("unknown overlay")
        context = self.history[version].context
        if self.active.get(context) == version:
            del self.active[context]
        self.retired.add(version)


def fit_rule(calibration):
    """Select from a declared finite class using calibration labels only."""
    if not calibration:
        raise ValueError("calibration required")
    if any(label not in (0, 1) for _, label in calibration):
        raise ValueError("binary labels required")
    best = None
    best_key = None
    for weights in itertools.product(range(-2, 3), repeat=3):
        for threshold in range(-2, 5):
            rule = Rule(weights, threshold)
            correct = sum(rule.predict(obs) == label for obs, label in calibration)
            # Resolve ties by smaller norm, then lexicographic rule order.
            key = (correct, -sum(abs(w) for w in weights), weights, -threshold)
            if best_key is None or key > best_key:
                best, best_key = rule, key
    return best
