import unittest

import numpy as np

import src.core.ode_solver as s


class TestOdeSolver(unittest.TestCase):
    def test_rk4(self) -> None:
        def f(_: float, y: float) -> float:
            return np.log(2) * y

        result = s.runge_kutta4(f, 1, 0, 0.01, lambda t, _: t >= 1)
        error_threshold = 1e-10
        self.assertTrue(np.abs(result[-1][1] - 2) < error_threshold)
        self.assertTrue(np.abs(result[-1][0] - 1) < error_threshold)


if __name__ == "__main__":
    unittest.main()
