import unittest

from gaia_layer import EvidenceLevel, ListeningGraph, Observation, Relation, SystemNode


class ListeningGraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = ListeningGraph()
        self.graph.add_node(
            SystemNode(id="region", label="Region", kind="region", scale="regional")
        )
        self.graph.add_node(
            SystemNode(
                id="forest",
                label="Forest",
                kind="forest",
                scale="local",
                parent_id="region",
            )
        )
        self.graph.add_node(
            SystemNode(
                id="stream",
                label="Stream",
                kind="stream",
                scale="local",
                parent_id="region",
            )
        )

    def test_stable_state(self) -> None:
        self.graph.ingest(
            Observation(
                node_id="forest",
                metric="soil_moisture",
                value=30,
                unit="%",
                source="sensor",
                reference_min=20,
                reference_max=40,
            )
        )
        self.assertEqual(self.graph.state("forest").status, "stable")

    def test_stress_state(self) -> None:
        self.graph.ingest(
            Observation(
                node_id="forest",
                metric="soil_moisture",
                value=10,
                unit="%",
                source="sensor",
                reference_min=20,
                reference_max=40,
            )
        )
        self.graph.ingest(
            Observation(
                node_id="forest",
                metric="temperature",
                value=35,
                unit="C",
                source="sensor",
                reference_min=5,
                reference_max=30,
            )
        )
        self.assertEqual(self.graph.state("forest").status, "stress")

    def test_voice_keeps_epistemic_boundary(self) -> None:
        voice = self.graph.voice("forest").text
        self.assertIn("synthetic system voice", voice)
        self.assertIn("not evidence", voice)

    def test_relation_becomes_attention_candidate_without_causality(self) -> None:
        self.graph.add_relation(
            Relation(
                source_id="forest",
                target_id="stream",
                mechanism="runoff coupling",
                evidence_level=EvidenceLevel.HYPOTHESIS,
                confidence=0.5,
            )
        )
        self.graph.ingest(
            Observation(
                node_id="forest",
                metric="soil_moisture",
                value=10,
                unit="%",
                source="sensor",
                reference_min=20,
                reference_max=40,
            )
        )
        synthesis = self.graph.synthesize(["forest", "stream"])
        self.assertEqual(len(synthesis["coupled_attention"]), 1)
        self.assertFalse(synthesis["coupled_attention"][0]["causality_claimed"])

    def test_parent_must_exist(self) -> None:
        with self.assertRaises(ValueError):
            self.graph.add_node(
                SystemNode(
                    id="orphan",
                    label="Orphan",
                    kind="forest",
                    scale="local",
                    parent_id="missing",
                )
            )


if __name__ == "__main__":
    unittest.main()
