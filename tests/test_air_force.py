import unittest

import numpy as np
import pandas as pd

import src.core.air_force as af
import src.core.quaternion_util as qu
from src.core.config import Config, WindPowerLow
from src.core.rocket_state import RocketState
from src.core.simulation_context import SimulationContext
from src.util.type import NPVector


class TestAirForce(unittest.TestCase):
    def test_dynamic_pressure(self) -> None:
        airspeed = np.array([1, 2, 3])
        air_density = 4
        result = af.dynamic_pressure(airspeed, air_density)
        expected = 28
        self.assertTrue(result == expected)

    def test_axial_force(self) -> None:
        airspeed = np.array([1, 2, 3])
        air_density = 4
        body_area = 5
        axial_force_coefficient = 6
        result = af.axial_force(
            airspeed,
            air_density,
            body_area,
            axial_force_coefficient,
        )
        expected = np.array([-840, 0, 0])
        np.testing.assert_array_almost_equal(result, expected)

    def test_normal_force(self) -> None:
        airspeed = np.array([1, 2, 3])
        air_density = 4
        body_area = 5
        normal_force_coefficient = 6
        result = af.normal_force(
            airspeed,
            air_density,
            body_area,
            normal_force_coefficient,
        )
        norm = np.linalg.norm(result, ord=2)
        self.assertTrue(np.isclose(norm, 840.0))
        cross_product = np.cross(airspeed, np.array([1, 0, 0]))
        self.assertTrue(
            np.isclose(np.dot(result, cross_product), 0.0),
        )  # 対気速度と機体軸が張る平面上にある
        self.assertEqual(result[0], 0)
        self.assertLess(result[1], 0)
        self.assertLess(result[2], 0)

    def test_angle_of_attack(self) -> None:
        zero = af.angle_of_attack(np.array([1, 0, 0]))
        self.assertTrue(zero == 0)
        ninety = af.angle_of_attack(np.array([0, 1, 3]))
        self.assertTrue(np.isclose(ninety, np.pi / 2))
        fortyfive = af.angle_of_attack(np.array([1, 2**0.5, 1]))
        self.assertTrue(np.isclose(fortyfive, np.pi / 3))

    def test_air_force_moment(self) -> None:
        force = np.array([1, 2, 3])
        wind_center = np.array([4, 5, 6])
        result = af.air_force_moment(force, wind_center)
        np.testing.assert_array_almost_equal(result, [3, -6, 3])

    def test_parachute_force(self) -> None:
        parachute_terminal_velocity = 10
        mass = 3
        v = np.array([1, 1, 0])
        result = af.parachute_force(v, parachute_terminal_velocity, mass)
        answer = 3 * 9.8 * 2**0.5 / 100 * np.array([-1, -1, 0])
        np.testing.assert_array_almost_equal(result, answer)

    def setUp(self) -> None:
        # テスト用のSimulationContextを準備
        mass_df = pd.DataFrame({"mass": [10.0, 9.0, 8.0]}, index=[0.0, 1.0, 2.0])
        thrust_df = pd.DataFrame({"thrust": [100.0, 50.0, 0.0]}, index=[0.0, 1.0, 2.0])

        wind_config = WindPowerLow(
            reference_height=10.0,
            wind_speed=5.0,
            exponent=7.0,
            wind_direction=45.0,
        )

        # 重心位置
        first_gravity_center = np.array([0.0, 0.0, 1.0])
        end_gravity_center = np.array([0.0, 0.0, 0.8])

        self.config = Config(
            mass=mass_df,
            wind=wind_config,
            thrust=thrust_df,
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
            first_gravity_center=first_gravity_center,
            end_gravity_center=end_gravity_center,
            length=1.0,
        )

        self.context = SimulationContext(self.config)

    def test_calculate_without_parachute(self) -> None:
        """パラシュートなしの場合のcalculate関数のテスト"""
        # 初期姿勢と位置
        posture = qu.from_euler_angle(5.0, 90.0, 0.0)
        position = np.array([0.0, 0.0, -100.0])  # 高度100m
        velocity = np.array([10.0, 0.0, 0.0])  # x方向に10m/s
        rotation = np.array([0.0, 0.0, 0.0])  # 回転なし

        rocket_state = RocketState(
            position=position,
            velocity=velocity,
            posture=posture,
            rotation=rotation,
        )

        # calculate関数の実行
        result = af.calculate(
            rocket_state=rocket_state,
            context=self.context,
            parachute_on=False,
            t=0.0,
        )

        # 結果の検証
        self.assertIsInstance(result, af.AirForceResult)
        self.assertIsInstance(result.force, NPVector)
        self.assertIsInstance(result.moment, NPVector)
        self.assertIsInstance(result.dynamic_pressure, float)
        self.assertIsInstance(result.velocity_air_body_frame, NPVector)

        # 風速が考慮された対気速度になっているか確認
        wind_at_100m = self.context.wind(100.0)
        expected_velocity_inertial = velocity - wind_at_100m
        # 対気速度を剛体系に変換したものと近似的に一致するはず
        body_velocity = qu.inertial_to_body(posture, expected_velocity_inertial)
        np.testing.assert_array_almost_equal(
            result.velocity_air_body_frame,
            body_velocity,
        )

        # 力が発生しているか確認
        self.assertTrue(np.linalg.norm(result.force) > 0)

        # モーメントが重心位置を考慮しているか確認
        gravity_center_pos = self.context.gravity_center(0.0)
        wind_center_from_gravity = self.context.wind_center - gravity_center_pos
        expected_moment = np.cross(wind_center_from_gravity, result.force)
        np.testing.assert_array_almost_equal(result.moment, expected_moment)

    def test_calculate_with_parachute(self) -> None:
        """パラシュート展開時のcalculate関数のテスト"""
        # 初期姿勢と位置
        posture = qu.from_euler_angle(5.0, 90.0, 0.0)
        position = np.array([0.0, 0.0, -100.0])  # 高度100m
        velocity = np.array([10.0, 0.0, 0.0])  # x方向に10m/s
        rotation = np.array([0.0, 0.0, 0.0])  # 回転なし

        rocket_state = RocketState(
            position=position,
            velocity=velocity,
            posture=posture,
            rotation=rotation,
        )

        # パラシュートなしの場合
        result_without_parachute = af.calculate(
            rocket_state=rocket_state,
            context=self.context,
            parachute_on=False,
            t=0.0,
        )

        # パラシュートありの場合
        result_with_parachute = af.calculate(
            rocket_state=rocket_state,
            context=self.context,
            parachute_on=True,
            t=0.0,
        )

        # パラシュートの影響で力が増加しているか確認
        force_without = np.linalg.norm(result_without_parachute.force)
        force_with = np.linalg.norm(result_with_parachute.force)
        self.assertTrue(force_with > force_without)

        # パラシュート力の方向が速度と逆向きになっているか確認
        parachute_force_vector = result_with_parachute.force - result_without_parachute.force
        air_velocity = result_with_parachute.velocity_air_body_frame
        expected_parachute_force = (
            -9.8 * 8 / self.config.parachute_terminal_velocity**2 * air_velocity * np.linalg.norm(air_velocity)
        )
        np.testing.assert_array_almost_equal(
            parachute_force_vector,
            expected_parachute_force,
        )

    def test_calculate_with_zero_velocity(self) -> None:
        """速度がゼロの場合のcalculate関数のテスト"""
        # 初期姿勢と位置
        posture = qu.from_euler_angle(5.0, 90.0, 0.0)
        position = np.array([0.0, 0.0, -100.0])  # 高度100m
        velocity = np.array([0.0, 0.0, 0.0])  # 速度ゼロ
        rotation = np.array([0.0, 0.0, 0.0])  # 回転なし

        rocket_state = RocketState(
            position=position,
            velocity=velocity,
            posture=posture,
            rotation=rotation,
        )

        # 風速がある場合、対気速度は風速の逆ベクトルになる
        wind_at_100m = self.context.wind(100.0)

        # calculate関数の実行
        result = af.calculate(
            rocket_state=rocket_state,
            context=self.context,
            parachute_on=False,
            t=0.0,
        )

        # 結果の検証
        # 対気速度が風速の逆ベクトルと近似的に一致するはず
        body_velocity = qu.inertial_to_body(posture, -wind_at_100m)
        np.testing.assert_array_almost_equal(
            result.velocity_air_body_frame,
            body_velocity,
        )

        # 力が発生しているか確認
        self.assertTrue(np.linalg.norm(result.force) > 0)


if __name__ == "__main__":
    unittest.main()
