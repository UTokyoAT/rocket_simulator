import unittest
from app.core.rocket_state import RocketState
import numpy as np
import quaternion as quart

class TestRocketState(unittest.TestCase):
    def setUp(self):
        self.rs1 = RocketState(np.array([1,2,3]), np.array([2,3,4]), quart.quaternion(1,2,3,4), np.array([4,5,6]))
        self.rs2 = RocketState(np.array([5,6,7]), np.array([6,7,8]), quart.quaternion(5,6,7,8), np.array([8,9,10]))

    def assertRocketStateEqual(self, rs, position, velocity, posture, rotation):
        self.assertTrue(np.array_equal(rs.position, position))
        self.assertTrue(np.array_equal(rs.velocity, velocity))
        self.assertTrue(np.array_equal(rs.posture, posture))
        self.assertTrue(np.array_equal(rs.rotation, rotation))

    def test_add(self):
        result = self.rs1 + self.rs2
        self.assertRocketStateEqual(result, [6,8,10], [8,10,12], quart.quaternion(6,8,10,12), [12,14,16])

    def test_mul(self):
        result = self.rs1 * 2
        self.assertRocketStateEqual(result, [2,4,6], [4,6,8], quart.quaternion(2,4,6,8), [8,10,12])

if __name__ == '__main__':
    unittest.main()