import unittest
import numpy as np
import src.core.air_force as af


class TestAirForce(unittest.TestCase):
    def test_dynamic_pressure(self):
        airspeed = np.array([1, 2, 3])
        air_density = 4
        result = af.dynamic_pressure(airspeed, air_density)
        self.assertTrue(result == 28)

    def test_axial_force(self):
        airspeed = np.array([1, 2, 3])
        air_density = 4
        body_area = 5
        axial_force_coefficient = 6
        result = af.axial_force(
            airspeed, air_density, body_area, axial_force_coefficient
        )
        self.assertTrue(np.all(np.abs(result - [-840, 0, 0]) < 1e-10))

    def test_normal_force(self):
        airspeed = np.array([1, 2, 3])
        air_density = 4
        body_area = 5
        normal_force_coefficient = 6
        result = af.normal_force(
            airspeed, air_density, body_area, normal_force_coefficient
        )
        norm = np.linalg.norm(result, ord=2)
        self.assertTrue(np.abs(float(norm) - 840.0) < 1e-10)
        self.assertTrue(
            np.dot(result, np.cross(airspeed, np.array([1, 0, 0]))) < 1e-10
        )  # 対気速度と機体軸が張る平面上にある
        self.assertEqual(result[0], 0)
        self.assertLess(result[1], 0)
        self.assertLess(result[2], 0)

    def test_angle_of_attack(self):
        zero = af.angle_of_attack(np.array([1, 0, 0]))
        self.assertTrue(zero == 0)
        ninety = af.angle_of_attack(np.array([0, 1, 3]))
        self.assertTrue(np.abs(ninety - np.pi / 2) < 1e-10)
        fortyfive = af.angle_of_attack(np.array([1, 2**0.5, 1]))
        self.assertTrue(np.abs(fortyfive - np.pi / 3) < 1e-10)

    def test_air_force_moment(self):
        force = np.array([1, 2, 3])
        wind_center = np.array([4, 5, 6])
        result = af.air_force_moment(force, wind_center)
        self.assertTrue(np.all(result == [3, -6, 3]))

    def test_parachute_force(self):
        parachute_terminal_velocity = 10
        mass = 3
        v = np.array([1, 1, 0])
        result = af.parachute_force(v, parachute_terminal_velocity, mass)
        answer = 3 * 9.8 * 2**0.5 / 100 * np.array([-1, -1, 0])
        self.assertTrue(np.all(np.abs(result - answer) < 1e-10))


if __name__ == "__main__":
    unittest.main()
