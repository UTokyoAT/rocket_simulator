import unittest

import numpy as np
import quaternion

from src.core import simulation_result


class TestSimulationResult(unittest.TestCase):
    def setUp(self):
        self.row1 = simulation_result.SimulationResultRow(
            time=0.0,
            position=np.array([1.0, 2.0, 3.0]),
            velocity=np.array([4.0, 5.0, 6.0]),
            posture=quaternion.quaternion(0, 0, 0, 1),
            rotation=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            dynamic_pressure=1,
            burning=True,
            on_launcher=True,
            velocity_air_body_frame=np.array([0, 0, 0]),
            acceleration_body_frame=np.array([0, 0, 0]),
        )
        self.row2 = simulation_result.SimulationResultRow(
            time=1.0,
            position=np.array([7.0, 8.0, 9.0]),
            velocity=np.array([10.0, 11.0, 12.0]),
            posture=quaternion.quaternion(1, 1, 1, 1),
            rotation=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            dynamic_pressure=2,
            burning=False,
            on_launcher=False,
            velocity_air_body_frame=np.array([1, 2, 3]),
            acceleration_body_frame=np.array([4, 5, 6]),
        )
        self.row3 = simulation_result.SimulationResultRow(
            time=2.0,
            position=np.array([13.0, 14.0, 15.0]),
            velocity=np.array([16.0, 17.0, 18.0]),
            posture=quaternion.quaternion(1, 2, 3, 4),
            rotation=np.array([[1, 2], [3, 4]]),
            dynamic_pressure=3,
            burning=True,
            on_launcher=True,
            velocity_air_body_frame=np.array([4, 5, 6]),
            acceleration_body_frame=np.array([7, 8, 9]),
        )
        self.sim_result1 = simulation_result.SimulationResult(
            result=[self.row1, self.row2],
        )
        self.sim_result2 = simulation_result.SimulationResult(
            result=[self.row2, self.row3],
        )

    def test_append(self):
        self.sim_result1.append(self.row3)
        self.assertEqual(len(self.sim_result1.result), 3)
        self.assertEqual(self.sim_result1.result[-1], self.row3)

    def test_join(self):
        joined_result = self.sim_result1.join(self.sim_result2)
        self.assertEqual(len(joined_result.result), 3)
        self.assertEqual(joined_result.result[0], self.row1)
        self.assertEqual(joined_result.result[1], self.row2)
        self.assertEqual(joined_result.result[2], self.row3)
        with self.assertRaises(AssertionError):
            self.sim_result1.join(self.sim_result1)

    def test_last(self):
        last_row = self.sim_result1.last()
        self.assertEqual(last_row, self.row2)
        self.assertNotEqual(last_row, self.row1)
        self.assertNotEqual(last_row, self.row3)

    def test_init_empty(self):
        empty_result = simulation_result.SimulationResult.init_empty()
        self.assertEqual(len(empty_result.result), 0)
        self.assertIsInstance(empty_result, simulation_result.SimulationResult)

    def test_deepcopy(self):
        copied_result = self.sim_result1.deepcopy()
        self.assertEqual(len(copied_result.result), 2)
        self.assertEqual(copied_result.result[0].position[0], self.row1.position[0])
        self.assertEqual(copied_result.result[1].velocity[0], self.row2.velocity[0])
        copied_result.result[0].time = 100
        self.assertNotEqual(
            self.sim_result1.result[0].time, copied_result.result[0].time,
        )
