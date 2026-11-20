from dataclasses import FrozenInstanceError
import unittest

from context_overlay_v01 import Overlay, OverlayArm, Rule, fit_rule
from overlay_probe_v01 import cases


class ContextOverlayTests(unittest.TestCase):
    def setUp(self):
        self.base = Rule((1, 2, 1), 2)
        self.arm = OverlayArm(self.base)
        self.overlay = Overlay("B", self.base.fingerprint(), Rule((-1, -2, -1), -1))

    def test_action_changes_and_rollback_restores_both_contexts(self):
        observations = [(0, 0, 0), (0, 1, 0), (1, 0, 1), (0.9, 0.9, 0.1)]
        before = [self.arm.predict(x, "B") for x in observations]
        version = self.arm.install(self.overlay)
        during = [self.arm.predict(x, "B") for x in observations]
        self.assertNotEqual(before, during)
        self.assertEqual([self.arm.predict(x, "A") for x in observations], before)
        self.arm.retire(version)
        for context in ("A", "B"):
            self.assertEqual([self.arm.predict(x, context) for x in observations], before)
        self.assertIn(version, self.arm.history)
        self.assertIn(version, self.arm.retired)

    def test_replayed_retired_version_cannot_reactivate(self):
        version = self.arm.install(self.overlay)
        self.arm.retire(version)
        self.arm.retire(version)
        with self.assertRaisesRegex(ValueError, "retired"):
            self.arm.install(self.overlay)

    def test_retiring_old_version_preserves_new_version(self):
        old = self.arm.install(self.overlay)
        newer = Overlay("B", self.base.fingerprint(), Rule((0, 0, 0), 0))
        current = self.arm.install(newer)
        self.arm.retire(old)
        self.assertEqual(self.arm.active["B"], current)
        self.assertEqual(len(self.arm.history), 2)

    def test_wrong_parent_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "parent"):
            self.arm.install(Overlay("B", Rule((0, 1, 0)).fingerprint(), self.overlay.rule))
        self.assertEqual(self.arm.history, {})

    def test_base_and_overlay_rules_are_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.base.threshold = 7
        with self.assertRaises(ValueError):
            Rule([1, 2, 1])
        with self.assertRaises(ValueError):
            Rule((1, float("nan"), 1))
        with self.assertRaises(ValueError):
            self.base.predict((0, 1))

    def test_calibration_fit_handles_independently_written_labels(self):
        # NAND(hazard OR (contact AND persistence)) on explicit binary examples.
        calibration = [((0, 0, 0), 1), ((0, 0, 1), 1), ((0, 1, 0), 0),
                       ((0, 1, 1), 0), ((1, 0, 0), 1), ((1, 0, 1), 0),
                       ((1, 1, 0), 0), ((1, 1, 1), 0)]
        rule = fit_rule(calibration)
        self.assertEqual([rule.predict(obs) for obs, _ in calibration],
                         [target for _, target in calibration])
        self.assertEqual(fit_rule(calibration), rule)

    def test_split_observations_are_disjoint_and_balanced_by_pattern(self):
        calibration = cases(27001, 8)
        final = cases(127001, 16)
        self.assertTrue(set(obs for obs, _ in calibration).isdisjoint(obs for obs, _ in final))
        self.assertEqual(len(calibration), 64)
        self.assertEqual(len(final), 128)
        self.assertEqual(sum(target for _, target in final), 80)

    def test_empty_or_invalid_calibration_is_rejected(self):
        with self.assertRaises(ValueError):
            fit_rule([])
        with self.assertRaises(ValueError):
            fit_rule([((0, 0, 0), 5)])


if __name__ == "__main__":
    unittest.main()
