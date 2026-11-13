import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from autonomy import evolve, initial, save_state, validate_state
from evaluate_autonomy import ORACLE, evaluate, trials


class CheckpointAuditTests(unittest.TestCase):
    def test_optimizer_preserves_callers_snapshot(self):
        original = initial()
        snapshot = copy.deepcopy(original)
        result = evolve(original)
        self.assertEqual(original, snapshot)
        self.assertGreater(result["generation"], 0)

    def test_tampering_is_rejected_before_evolution(self):
        state = evolve(initial())
        state["policies"]["C"][0] = 1
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            evolve(state)

    def test_old_checkpoint_and_atomic_resume(self):
        state = evolve(initial())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            save_state(path, state)
            restored = json.loads(path.read_text())
            validate_state(restored)
            self.assertEqual(evolve(restored), evolve(state))

    def test_interrupted_replace_keeps_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            save_state(path, evolve(initial(), 1))
            previous = path.read_bytes()
            with patch("autonomy.os.replace", side_effect=OSError("interrupted")):
                with self.assertRaises(OSError):
                    save_state(path, evolve(initial()))
            self.assertEqual(path.read_bytes(), previous)
            self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_invalid_checkpoint_and_budget(self):
        state = initial()
        state["policies"]["Si"] = [2, 0]
        with self.assertRaises(ValueError):
            evolve(state)
        for steps in (0, -1, 101, True, 1.5):
            with self.subTest(steps=steps), self.assertRaises(ValueError):
                evolve(initial(), steps)

    def test_audit_is_read_only_and_separate_from_optimizer(self):
        state = evolve(initial())
        original = copy.deepcopy(state)
        result = evaluate(state)
        self.assertEqual(state, original)
        self.assertEqual(result, evaluate(state))
        self.assertEqual(result["total_cases"], 5120)
        self.assertFalse(result["selection_feedback"])

    def test_independent_cases_preserve_latent_labels(self):
        cases = trials(13001)
        self.assertEqual(len(cases), 256)
        self.assertNotEqual(cases, trials(13002))
        self.assertEqual(sum(label for _, label in cases), 160)
        for observation, label in cases:
            self.assertNotIn(observation, ORACLE)
            bits = tuple(int(value > 0.5) for value in observation)
            self.assertEqual(label, ORACLE[bits])

    def test_fixed_policy_ablation_is_a_zero_delta_control(self):
        report = evaluate(initial())
        for group in report["summary"].values():
            self.assertEqual(group["mean_delta"], 0)
            self.assertEqual(group["worse_seeds"], 0)


if __name__ == "__main__":
    unittest.main()
