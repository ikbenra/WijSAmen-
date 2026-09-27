#!/usr/bin/env python3
import json
import math
import tempfile
import unittest
from pathlib import Path

from harness import build_receipt, canonical_bytes, sha256_json


def tetra(name: str) -> dict:
    return {
        "name": name,
        "material": {"name": "reference polymer", "density_g_cm3": 1.2},
        "cell": {"dimensions_mm": [10, 10, 10]},
        "nodes": [[0, 0, 0], [10, 0, 0], [0, 10, 0], [0, 0, 10]],
        "edges": [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]],
        "manufacturing": {"minimum_feature_mm": 0.2},
        "load_cases": [{"id": "compression_z", "status": "FROZEN_NOT_RUN"}],
    }


class HarnessTests(unittest.TestCase):
    def test_equal_mass_normalization_and_hash_stability(self):
        receipt = build_receipt(tetra("candidate"), tetra("comparator"), 0.6)
        self.assertEqual(receipt["candidate"]["target_mass_g"], 0.6)
        self.assertEqual(receipt["comparator"]["target_mass_g"], 0.6)
        self.assertEqual(receipt["candidate"]["uniform_radius_mm"], receipt["comparator"]["uniform_radius_mm"])
        core = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
        self.assertEqual(receipt["receipt_sha256"], sha256_json(core))
        self.assertEqual(canonical_bytes(core), canonical_bytes(json.loads(canonical_bytes(core))))

    def test_orientation_tensor_has_unit_trace(self):
        receipt = build_receipt(tetra("candidate"), tetra("comparator"), 0.6)
        tensor = receipt["candidate"]["length_weighted_orientation_tensor"]
        self.assertTrue(math.isclose(sum(tensor[i][i] for i in range(3)), 1.0, rel_tol=1e-12))

    def test_disconnected_geometry_is_flagged(self):
        geometry = tetra("disconnected")
        geometry["nodes"].append([9, 9, 9])
        receipt = build_receipt(geometry, tetra("comparator"), 0.6)
        self.assertIn("geometry has multiple disconnected components", receipt["candidate"]["warnings"])

    def test_cli_inputs_can_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            value = tetra("roundtrip")
            path.write_text(json.dumps(value), encoding="utf-8")
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), value)


if __name__ == "__main__":
    unittest.main()
