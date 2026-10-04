from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .models import (
    CoupledAttention,
    NodeState,
    Observation,
    Relation,
    SystemNode,
    VoiceMessage,
)


ATTENTION_STATES = {"watch", "stress"}


class ListeningGraph:
    """Small evidence-aware graph for local and cross-system interpretation."""

    def __init__(self) -> None:
        self.nodes: dict[str, SystemNode] = {}
        self.observations: dict[str, list[Observation]] = defaultdict(list)
        self.relations: list[Relation] = []

    def add_node(self, node: SystemNode) -> None:
        if node.id in self.nodes:
            raise ValueError(f"Duplicate node id: {node.id}")
        if node.parent_id is not None and node.parent_id not in self.nodes:
            raise ValueError(
                f"Parent {node.parent_id!r} must be registered before child {node.id!r}"
            )
        self.nodes[node.id] = node

    def add_relation(self, relation: Relation) -> None:
        if relation.source_id not in self.nodes:
            raise KeyError(f"Unknown source node: {relation.source_id}")
        if relation.target_id not in self.nodes:
            raise KeyError(f"Unknown target node: {relation.target_id}")
        if not 0.0 <= relation.confidence <= 1.0:
            raise ValueError("Relation confidence must be between 0 and 1")
        self.relations.append(relation)

    def ingest(self, observation: Observation) -> None:
        if observation.node_id not in self.nodes:
            raise KeyError(f"Unknown node: {observation.node_id}")
        if not 0.0 <= observation.confidence <= 1.0:
            raise ValueError("Observation confidence must be between 0 and 1")
        if (
            observation.reference_min is not None
            and observation.reference_max is not None
            and observation.reference_min > observation.reference_max
        ):
            raise ValueError("reference_min cannot be greater than reference_max")
        self.observations[observation.node_id].append(observation)

    def latest_by_metric(self, node_id: str) -> dict[str, Observation]:
        self._require_node(node_id)
        latest: dict[str, Observation] = {}
        for obs in self.observations[node_id]:
            previous = latest.get(obs.metric)
            if previous is None or obs.timestamp > previous.timestamp:
                latest[obs.metric] = obs
        return latest

    def state(self, node_id: str) -> NodeState:
        latest = self.latest_by_metric(node_id)
        interpreted = [
            obs for obs in latest.values() if obs.reference_status() != "uninterpreted"
        ]
        out = [
            obs
            for obs in interpreted
            if obs.reference_status() in {"low", "high"}
        ]

        if not interpreted:
            status = "unknown"
        elif not out:
            status = "stable"
        elif len(out) * 2 >= len(interpreted):
            status = "stress"
        else:
            status = "watch"

        return NodeState(
            node_id=node_id,
            status=status,
            latest=latest,
            interpreted_metrics=len(interpreted),
            out_of_range_metrics=len(out),
        )

    def voice(self, node_id: str) -> VoiceMessage:
        node = self._require_node(node_id)
        state = self.state(node_id)
        claims: list[str] = []

        for metric in sorted(state.latest):
            obs = state.latest[metric]
            ref = obs.reference_status()
            confidence = f"{obs.confidence:.0%} confidence"
            if ref == "low":
                claim = (
                    f"{metric} is {obs.value:g} {obs.unit}, below the configured "
                    f"reference range ({confidence}, source: {obs.source})"
                )
            elif ref == "high":
                claim = (
                    f"{metric} is {obs.value:g} {obs.unit}, above the configured "
                    f"reference range ({confidence}, source: {obs.source})"
                )
            elif ref == "within":
                claim = (
                    f"{metric} is {obs.value:g} {obs.unit}, within the configured "
                    f"reference range ({confidence}, source: {obs.source})"
                )
            else:
                claim = (
                    f"{metric} is observed at {obs.value:g} {obs.unit}; no reference "
                    f"interpretation is configured ({confidence}, source: {obs.source})"
                )
            claims.append(claim)

        if claims:
            body = ". ".join(claims) + "."
        else:
            body = "I do not yet have observations to report."

        text = (
            f"[synthetic system voice] I am {node.label}. "
            f"My current interpreted state is {state.status}. {body} "
            "This voice is a translation of structured system data, not evidence "
            "that I possess subjective consciousness."
        )

        return VoiceMessage(
            node_id=node.id,
            label=node.label,
            status=state.status,
            text=text,
            claims=tuple(claims),
        )

    def coupled_attention(self) -> list[CoupledAttention]:
        items: list[CoupledAttention] = []
        for relation in self.relations:
            source = self.state(relation.source_id)
            target = self.state(relation.target_id)
            if source.status in ATTENTION_STATES or target.status in ATTENTION_STATES:
                items.append(
                    CoupledAttention(
                        source_id=relation.source_id,
                        target_id=relation.target_id,
                        mechanism=relation.mechanism,
                        source_status=source.status,
                        target_status=target.status,
                        evidence_level=relation.evidence_level,
                        confidence=relation.confidence,
                    )
                )
        return items

    def synthesize(self, node_ids: Iterable[str] | None = None) -> dict:
        ids = list(node_ids) if node_ids is not None else list(self.nodes)
        states = {node_id: self.state(node_id) for node_id in ids}

        counts = {"unknown": 0, "stable": 0, "watch": 0, "stress": 0}
        for state in states.values():
            counts[state.status] += 1

        selected = set(ids)
        attention = [
            item
            for item in self.coupled_attention()
            if item.source_id in selected and item.target_id in selected
        ]

        return {
            "node_count": len(ids),
            "status_counts": counts,
            "coupled_attention": [
                {
                    "source_id": item.source_id,
                    "target_id": item.target_id,
                    "mechanism": item.mechanism,
                    "source_status": item.source_status,
                    "target_status": item.target_status,
                    "evidence_level": item.evidence_level.value,
                    "confidence": item.confidence,
                    "causality_claimed": False,
                }
                for item in attention
            ],
            "epistemic_note": (
                "Coupled attention marks connected systems that deserve joint review. "
                "It does not by itself establish causality."
            ),
        }

    def children_of(self, node_id: str) -> list[SystemNode]:
        self._require_node(node_id)
        return [node for node in self.nodes.values() if node.parent_id == node_id]

    def _require_node(self, node_id: str) -> SystemNode:
        try:
            return self.nodes[node_id]
        except KeyError as exc:
            raise KeyError(f"Unknown node: {node_id}") from exc
