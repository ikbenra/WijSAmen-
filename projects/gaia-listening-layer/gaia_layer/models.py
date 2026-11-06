from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class EvidenceLevel(str, Enum):
    OBSERVED = "observed"
    DERIVED = "derived"
    HYPOTHESIS = "hypothesis"
    SIMULATED = "simulated"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class SystemNode:
    id: str
    label: str
    kind: str
    scale: str
    parent_id: str | None = None
    interests: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Observation:
    node_id: str
    metric: str
    value: float
    unit: str
    source: str
    timestamp: str = field(default_factory=utc_now_iso)
    confidence: float = 1.0
    reference_min: float | None = None
    reference_max: float | None = None
    evidence_level: EvidenceLevel = EvidenceLevel.OBSERVED
    metadata: dict[str, Any] = field(default_factory=dict)

    def reference_status(self) -> str:
        if self.reference_min is None and self.reference_max is None:
            return "uninterpreted"
        if self.reference_min is not None and self.value < self.reference_min:
            return "low"
        if self.reference_max is not None and self.value > self.reference_max:
            return "high"
        return "within"


@dataclass(frozen=True)
class Relation:
    source_id: str
    target_id: str
    mechanism: str
    evidence_level: EvidenceLevel = EvidenceLevel.HYPOTHESIS
    confidence: float = 0.5
    bidirectional: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NodeState:
    node_id: str
    status: str
    latest: dict[str, Observation]
    interpreted_metrics: int
    out_of_range_metrics: int


@dataclass(frozen=True)
class VoiceMessage:
    node_id: str
    label: str
    status: str
    text: str
    claims: tuple[str, ...]


@dataclass(frozen=True)
class CoupledAttention:
    source_id: str
    target_id: str
    mechanism: str
    source_status: str
    target_status: str
    evidence_level: EvidenceLevel
    confidence: float
