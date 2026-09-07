import unittest

import numpy as np
import pandas as pd

from benchmark import baryon_v2, make_split, nfw_v2, burkert_v2, rar_velocity


class BaselineTests(unittest.TestCase):
    def test_split_is_exact_and_order_independent(self):
        names = [f"G{i:03d}" for i in range(175)]
        a = make_split(names)
        b = make_split(list(reversed(names)))
        self.assertTrue(a.equals(b))
        self.assertEqual((a.split == "train").sum(), 35)

    def test_predictions_are_finite_and_nonnegative(self):
        frame = pd.DataFrame({"radius_kpc": [0.5, 2.0], "v_gas": [-2.0, 10.0],
                              "v_disk": [20.0, 15.0], "v_bulge": [0.0, 4.0]})
        self.assertTrue(np.all(baryon_v2(frame) >= 0))
        self.assertTrue(np.all(np.isfinite(rar_velocity(frame, 1.2e-10))))
        for fn in (nfw_v2, burkert_v2):
            values = fn(frame.radius_kpc.to_numpy(), 7.0, 1.0)
            self.assertTrue(np.all(np.isfinite(values)))
            self.assertTrue(np.all(values >= 0))


if __name__ == "__main__":
    unittest.main()
