import unittest

import numpy as np
import quaternion as quart  # ty: ignore

from src.core.rocket_state import RocketState


class TestRocketState(unittest.TestCase):
    def setUp(self) -> None:
        self.rs1 = RocketState(
            np.array([1, 2, 3]),
            np.array([2, 3, 4]),
            quart.quaternion(1, 2, 3, 4),
            np.array([4, 5, 6]),
        )
        self.rs2 = RocketState(
            np.array([5, 6, 7]),
            np.array([6, 7, 8]),
            quart.quaternion(5, 6, 7, 8),
            np.array([8, 9, 10]),
        )

    def assert_rocket_state_equal(
        self,
        rs: RocketState,
        position: np.ndarray,
        velocity: np.ndarray,
        posture: quart.quaternion,
        rotation: np.ndarray,
    ) -> None:
        np.testing.assert_array_equal(rs.position, position)
        np.testing.assert_array_equal(rs.velocity, velocity)
        np.testing.assert_array_equal(rs.posture, posture)
        np.testing.assert_array_equal(rs.rotation, rotation)

    def test_add(self) -> None:
        result = self.rs1 + self.rs2
        self.assert_rocket_state_equal(
            result,
            [6, 8, 10],
            [8, 10, 12],
            quart.quaternion(6, 8, 10, 12),
            [12, 14, 16],
        )

    def test_mul(self) -> None:
        result = self.rs1 * 2
        self.assert_rocket_state_equal(
            result,
            [2, 4, 6],
            [4, 6, 8],
            quart.quaternion(2, 4, 6, 8),
            [8, 10, 12],
        )


if __name__ == "__main__":
    unittest.main()
