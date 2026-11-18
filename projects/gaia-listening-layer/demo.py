from pprint import pprint

from gaia_layer import EvidenceLevel, ListeningGraph, Observation, Relation, SystemNode


def build_demo() -> ListeningGraph:
    graph = ListeningGraph()

    graph.add_node(
        SystemNode(
            id="region-demo",
            label="Demo-regio",
            kind="region",
            scale="regional",
            interests=("water balance", "thermal resilience", "biodiversity"),
        )
    )
    graph.add_node(
        SystemNode(
            id="forest-a",
            label="Bos A",
            kind="forest",
            scale="local",
            parent_id="region-demo",
            interests=("soil moisture", "canopy health", "biodiversity"),
        )
    )
    graph.add_node(
        SystemNode(
            id="stream-b",
            label="Beek B",
            kind="stream",
            scale="local",
            parent_id="region-demo",
            interests=("flow", "water quality", "temperature"),
        )
    )

    graph.add_relation(
        Relation(
            source_id="forest-a",
            target_id="stream-b",
            mechanism="water retention and runoff coupling",
            evidence_level=EvidenceLevel.HYPOTHESIS,
            confidence=0.65,
            bidirectional=True,
        )
    )

    graph.ingest(
        Observation(
            node_id="forest-a",
            metric="soil_moisture",
            value=17.0,
            unit="%",
            source="demo_sensor",
            confidence=0.92,
            reference_min=22.0,
            reference_max=45.0,
        )
    )
    graph.ingest(
        Observation(
            node_id="forest-a",
            metric="canopy_temperature",
            value=31.5,
            unit="C",
            source="demo_sensor",
            confidence=0.88,
            reference_min=10.0,
            reference_max=29.0,
        )
    )
    graph.ingest(
        Observation(
            node_id="stream-b",
            metric="water_temperature",
            value=21.0,
            unit="C",
            source="demo_sensor",
            confidence=0.90,
            reference_min=5.0,
            reference_max=20.0,
        )
    )
    graph.ingest(
        Observation(
            node_id="stream-b",
            metric="flow_index",
            value=0.72,
            unit="ratio",
            source="demo_model",
            confidence=0.70,
            reference_min=0.60,
            reference_max=1.20,
            evidence_level=EvidenceLevel.DERIVED,
        )
    )

    return graph


if __name__ == "__main__":
    graph = build_demo()

    print("\n--- LOCAL VOICES ---\n")
    print(graph.voice("forest-a").text)
    print()
    print(graph.voice("stream-b").text)

    print("\n--- SYSTEMS-OF-SYSTEMS SYNTHESIS ---\n")
    pprint(graph.synthesize(["forest-a", "stream-b"]))
