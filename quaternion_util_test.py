import unittest
import numpy as np
import quaternion as quart
import app.core.quaternion_util as qu

class TestQuaternionUtil(unittest.TestCase):
    def test_inertial_to_body(self):
        q = quart.quaternion(1,1,0,0)#　ノルムが1である必要はない
        v = np.array([0,1,0])
        v2 = qu.inertial_to_body(q, v)
        self.assertTrue(np.all(np.abs(v2- [0,0,-1]) < 1e-10))

    def test_body_to_inertial(self):
        q = quart.quaternion(1,1,0,0)
        v = np.array([0,1,0])
        v2 = qu.body_to_inertial(q, v)
        self.assertTrue(np.all(np.abs(v2 - [0,0,1]) < 1e-10))

    def test_from_euler_angle(self):
        q = qu.from_euler_angle(60, 60, 10)
        v = qu.body_to_inertial(q, np.array([1,0,0]))
        v_correct = np.array([1/4,3**0.5/4,-3**0.5/2])
        self.assertTrue(np.all(np.abs(v - v_correct) < 1e-10))

    def test_sum_vector_inertial_frame(self):
        q = quart.quaternion(1,1,0,0)
        body_vec = [np.array([0,1,0]), np.array([0,1,0])]
        inertial_vec = [np.array([0,0,1]), np.array([0,0,1])]
        result = qu.sum_vector_inertial_frame(body_vec, inertial_vec, q)
        self.assertTrue(np.all(np.abs(result - [0,0,4]) < 1e-10))

    def test_sum_vector_body_frame(self):
        q = quart.quaternion(1,1,0,0)
        body_vec = [np.array([0,1,0]), np.array([0,1,0])]
        inertial_vec = [np.array([0,0,1]), np.array([0,0,1])]
        result = qu.sum_vector_body_frame(body_vec, inertial_vec, q)
        self.assertTrue(np.all(np.abs(result - [0,4,0]) < 1e-10))


if __name__ == '__main__':
    unittest.main()