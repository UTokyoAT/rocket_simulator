import unittest

import numpy as np

import src.core.equation_of_motion as qom
import src.core.inertia_tensor as it


class TestEquationOfMotion(unittest.TestCase):
    def test_angular_acceleration(self) -> None:
        torque = np.array([1, 2, 3])
        inertia = it.InertiaTensor(1, 2, 3, 0, 0, 0)
        rotation = np.array([4, 5, 6])
        result = qom.angular_acceleration(torque, inertia, rotation)
        expected = np.array([-29, 25, -17 / 3])
        np.testing.assert_array_almost_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
