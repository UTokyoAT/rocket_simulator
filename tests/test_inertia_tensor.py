import unittest
import numpy as np
import src.core.inertia_tensor as it


class TestInertiaTensor(unittest.TestCase):
    def test_init(self):
        tensor = it.InertiaTensor(1, 2, 3, 4, 5, 6)
        self.assertTrue(np.all(tensor.tensor == [[1, 4, 6], [4, 2, 5], [6, 5, 3]]))

    def test_inverse(self):
        tensor = it.InertiaTensor(1, 2, 3, 4, 5, 6)
        i = np.array([[1, 4, 6], [4, 2, 5], [6, 5, 3]])
        self.assertTrue(np.all(np.abs(tensor.inverse @ i - np.eye(3)) < 1e-10))


if __name__ == "__main__":
    unittest.main()
