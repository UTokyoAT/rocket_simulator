import unittest

import numpy as np
import pandas as pd

import src.core.simulation_context as sc
from src.core.config import Config, WindPowerLow


class TestSimulationContext(unittest.TestCase):
    def setUp(self) -> None:
        # テスト用のモックデータを作成
        mass_data = {"mass": [10.0, 9.0, 8.0]}
        mass_index = [0.0, 1.0, 2.0]
        self.mass_df = pd.DataFrame(mass_data, index=mass_index)

        thrust_data = {"thrust": [100.0, 50.0, 0.0]}
        thrust_index = [0.0, 1.0, 2.0]
        self.thrust_df = pd.DataFrame(thrust_data, index=thrust_index)

        # WindPowerLowの設定
        self.wind_config = WindPowerLow(
            reference_height=10.0,
            wind_speed=5.0,
            exponent=7.0,
            wind_direction=45.0,
        )

        # 重心位置の設定
        self.first_gravity_center = np.array([0.0, 0.0, 1.0])
        self.end_gravity_center = np.array([0.0, 0.0, 0.8])

        # Configの作成
        self.config = Config(
            mass=self.mass_df,
            wind=self.wind_config,
            thrust=self.thrust_df,
            CA=0.5,
            CN_alpha=2.0,
            body_area=0.01,
            wind_center=np.array([0.0, 0.0, 0.5]),
            dt=0.01,
            launcher_length=3.0,
            inertia_tensor_xx=1.0,
            inertia_tensor_yy=1.0,
            inertia_tensor_zz=0.1,
            inertia_tensor_xy=0.0,
            inertia_tensor_zy=0.0,
            inertia_tensor_xz=0.0,
            first_elevation=5.0,
            first_azimuth=90.0,
            first_roll=0.0,
            parachute_terminal_velocity=5.0,
            parachute_delay_time=3.0,
            first_gravity_center=self.first_gravity_center,
            end_gravity_center=self.end_gravity_center,
            length=1.0,
        )

    def test_init(self) -> None:
        """SimulationContextの初期化テスト"""
        sim_context = sc.SimulationContext(self.config)

        # 各属性が正しく初期化されているか確認
        self.assertEqual(sim_context.CA, 0.5)
        self.assertEqual(sim_context.CN_alpha, 2.0)
        self.assertEqual(sim_context.body_area, 0.01)
        wind_center_expected = np.array([0.0, 0.0, 0.5])
        np.testing.assert_array_equal(sim_context.wind_center, wind_center_expected)
        self.assertEqual(sim_context.dt, 0.01)
        self.assertEqual(sim_context.launcher_length, 3.0)
        self.assertEqual(sim_context.first_elevation, 5.0)
        self.assertEqual(sim_context.first_azimuth, 90.0)
        self.assertEqual(sim_context.first_roll, 0.0)
        self.assertEqual(sim_context.parachute_terminal_velocity, 5.0)
        self.assertEqual(sim_context.parachute_delay_time, 3.0)

        # 関数の戻り値の確認
        self.assertAlmostEqual(sim_context.mass(0.0), 10.0)
        self.assertAlmostEqual(sim_context.mass(1.0), 9.0)
        self.assertAlmostEqual(sim_context.thrust(0.0), 100.0)
        self.assertAlmostEqual(sim_context.thrust(1.0), 50.0)

        # 重心位置関数のテスト
        np.testing.assert_array_almost_equal(
            sim_context.gravity_center(0.0),
            self.first_gravity_center,
        )

        # 風速関数のテスト
        # 高度0mでの風速はゼロであることを確認
        np.testing.assert_array_almost_equal(sim_context.wind(0.0), np.zeros(3))

        # 高度10mでの風速を確認（基準高度と同じなので、基準風速と一致するはず）
        wind_dir_rad = np.deg2rad(45)
        expected_x = -np.cos(wind_dir_rad)
        expected_y = -np.sin(wind_dir_rad)
        expected_wind = 5.0 * np.array([expected_x, expected_y, 0])

        np.testing.assert_array_almost_equal(sim_context.wind(10.0), expected_wind)

        # 慣性テンソルのテスト
        expected_tensor = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.1]])
        np.testing.assert_array_almost_equal(
            sim_context.inertia_tensor.tensor,
            expected_tensor,
        )


if __name__ == "__main__":
    unittest.main()
