import unittest
import numpy as np
import src.core.equation_of_motion as qom
import src.core.inertia_tensor as it

class TestEquationOfMotion(unittest.TestCase):
    def test_angular_acceleration(self):
        torque = np.array([1,2,3])
        inertia = it.InertiaTensor(1,2,3,0,0,0)
        rotation = np.array([4,5,6])
        result = qom.angular_acceleration(torque, inertia, rotation)
        self.assertTrue(np.all(np.abs(result - [-29, 25, - 17/3]) < 1e-10))

if __name__ == '__main__':
    unittest.main()