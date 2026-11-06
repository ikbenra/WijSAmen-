from pprint import pprint

from gaia_layer import EvidenceLevel, ListeningGraph, Observation, Relation, SystemNode


def build_mobile_city_demo() -> ListeningGraph:
    graph = ListeningGraph()

    graph.add_node(
        SystemNode(
            id="sea-region",
            label="Sea Region",
            kind="marine_region",
            scale="regional",
            interests=("habitat health", "light", "oxygen", "mobility corridors"),
        )
    )
    graph.add_node(
        SystemNode(
            id="sea-cell-a",
            label="Sea Cell A",
            kind="marine_cell",
            scale="local",
            parent_id="sea-region",
            interests=("underwater light", "oxygen", "temperature"),
        )
    )
    graph.add_node(
        SystemNode(
            id="mobile-city-01",
            label="Mobile City 01",
            kind="mobile_floating_city",
            scale="local",
            parent_id="sea-region",
            interests=("habitability", "energy", "mobility", "ecological compatibility"),
            metadata={
                "mobility": {
                    "can_reposition": True,
                    "coordination_mode": "federated",
                },
                "light_management": {
                    "controllable": True,
                    "strategy": "openings_and_light_corridors",
                },
            },
        )
    )

    graph.add_relation(
        Relation(
            source_id="mobile-city-01",
            target_id="sea-cell-a",
            mechanism="shadow and light availability coupling",
            evidence_level=EvidenceLevel.HYPOTHESIS,
            confidence=0.70,
        )
    )
    graph.add_relation(
        Relation(
            source_id="sea-cell-a",
            target_id="mobile-city-01",
            mechanism="ecological carrying constraints inform position planning",
            evidence_level=EvidenceLevel.DERIVED,
            confidence=0.75,
        )
    )

    graph.ingest(
        Observation(
            node_id="sea-cell-a",
            metric="underwater_light",
            value=38.0,
            unit="percent_of_open_water_reference",
            source="demo_light_sensor",
            confidence=0.95,
            reference_min=45.0,
            reference_max=100.0,
        )
    )
    graph.ingest(
        Observation(
            node_id="sea-cell-a",
            metric="dissolved_oxygen",
            value=7.8,
            unit="mg/L",
            source="demo_oxygen_sensor",
            confidence=0.93,
            reference_min=6.0,
            reference_max=10.0,
        )
    )
    graph.ingest(
        Observation(
            node_id="mobile-city-01",
            metric="current_light_transmission",
            value=42.0,
            unit="percent",
            source="city_control_system",
            confidence=0.99,
            reference_min=35.0,
            reference_max=100.0,
            evidence_level=EvidenceLevel.DERIVED,
        )
    )

    return graph


if __name__ == "__main__":
    graph = build_mobile_city_demo()

    print("\n--- SEA VOICE ---\n")
    print(graph.voice("sea-cell-a").text)

    print("\n--- CITY VOICE ---\n")
    print(graph.voice("mobile-city-01").text)

    print("\n--- COUPLED SYNTHESIS ---\n")
    pprint(graph.synthesize(["sea-cell-a", "mobile-city-01"]))

    print(
        "\nInterpretation: the low underwater-light observation makes this city/sea "
        "relationship an attention candidate. A later mobility planner may simulate "
        "repositioning or increased light transmission, but v0.1 does not choose or "
        "execute physical movement."
    )
