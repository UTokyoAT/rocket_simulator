import src.core.ode_solver as s
import unittest
import numpy as np


class TestOdeSolver(unittest.TestCase):
    def test_rk4(self):
        def f(t, y):
            return np.log(2) * y

        result = s.runge_kutta4(f, 1, 0, 0.01, lambda t, y: t >= 1)
        self.assertTrue(np.abs(result[-1][1] - 2) < 1e-10)
        self.assertTrue(np.abs(result[-1][0] - 1) < 1e-10)


if __name__ == "__main__":
    unittest.main()
