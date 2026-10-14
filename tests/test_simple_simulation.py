import unittest

import numpy as np

import src.core.quaternion_util as qu
from src.core.simple_simulation import (
    Gravitational_acceleration,
    nongravitational_acceleration_body_frame,
)

POSTURES = [(0, 0, 0), (45, 30, 10), (76, 35, 0), (90, 180, 270)]


class TestNongravitationalAcceleration(unittest.TestCase):
    def test_freefall_acceleration_is_zero(self) -> None:
        for elevation, azimuth, roll in POSTURES:
            posture = qu.from_euler_angle(elevation, azimuth, roll)
            kinematic_acceleration = qu.inertial_to_body(posture, Gravitational_acceleration)
            result = nongravitational_acceleration_body_frame(posture, kinematic_acceleration)
            np.testing.assert_array_almost_equal(result, np.zeros(3))

    def test_rest_acceleration_opposes_gravity(self) -> None:
        for elevation, azimuth, roll in POSTURES:
            posture = qu.from_euler_angle(elevation, azimuth, roll)
            result = nongravitational_acceleration_body_frame(posture, np.zeros(3))
            expected = -qu.inertial_to_body(posture, Gravitational_acceleration)
            np.testing.assert_array_almost_equal(result, expected)
            self.assertAlmostEqual(float(np.linalg.norm(result)), float(np.linalg.norm(Gravitational_acceleration)))


if __name__ == "__main__":
    unittest.main()
