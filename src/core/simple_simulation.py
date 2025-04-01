import typing as t
import numpy as np
from dataclasses import dataclass
from . import air_force as af
from .rocket_state import RocketState
from . import quaternion_util
from . import ode_solver
from . import equation_of_motion
from .inertia_tensor import InertiaTensor


@dataclass
class Config:
    mass: t.Callable[[float], float]
    """時間->質量"""
    wind: t.Callable[[float], np.ndarray]
    """高度->風速ベクトル"""
    thrust: t.Callable[[float], float]
    """時間->推力"""
    CA: float
    """軸力係数"""
    CN_alpha: float
    """単位なす角あたりの法線力係数"""
    body_area: float
    """断面積"""
    wind_center: np.ndarray
    """風圧中心"""
    dt: float
    """時間刻み"""
    launcher_length: float
    """ランチャーの長さ"""
    inertia_tensor: InertiaTensor
    """慣性テンソル"""
    first_elevation: float
    """初期迎角"""
    first_azimuth: float
    """初期方位角"""
    first_roll: float
    """初期ロール角"""
    propellant_CG_distance: float
    """重心から見た推進剤までの距離"""
    nozzle_CG_distance: float
    """重心から見たノズルまでの距離"""
    m_dot: t.Callable[[float], float]
    """時間->推進剤の質量流量"""
    roll_damping_coefficient: float
    """ロール軸周りの減衰モーメント係数"""
    pitch_damping_coefficient: float
    """ピッチ軸周りの減衰モーメント係数"""
    yaw_damping_coefficient: float
    """ヨー軸周りの減衰モーメント係数"""
    overall_length: float
    """機体の全長"""


def air_force_body_frame(
    rocket_state: RocketState, config: Config
) -> tuple[np.ndarray, np.ndarray]:
    """機体座標系での風圧による力を計算する

    Args:
        rocket_state (RocketState): ロケットの状態
        config (Config): ロケットの設定

    Returns:
        np.ndarray: 機体座標系での風圧による力
    """
    airspeed = quaternion_util.inertial_to_body(
        rocket_state.posture,
        rocket_state.velocity - config.wind(-rocket_state.position[2]),
    )
    angle_of_attack = af.angle_of_attack(airspeed)
    air_density = 1.204
    axial_force = af.axial_force(airspeed, air_density, config.body_area, config.CA)
    CN = af.normal_force_coefficient(angle_of_attack, config.CN_alpha)
    normal_force = af.normal_force(airspeed, air_density, config.body_area, CN)
    air_force = axial_force + normal_force
    moment = af.air_force_moment(
        air_force,
        config.wind_center,
    )
    return air_force, moment


Gravitational_acceleration = np.array([0, 0, 9.8])


def simulate_launcher(
    first_state: RocketState, config: Config, first_time: float
) -> list[tuple[float, RocketState]]:
    """ランチャー上でのシミュレーションを行う

    Args:
        first_state (RocketState): 打ち上げ前のロケットの状態
        config (Config): ロケットの設定
        first_time (float): 初期時刻

    Returns:
        list[tuple[float,RocketState]]: 時刻とロケットの状態の組のリスト
    """

    def derivative(t, state):
        air_force, _ = air_force_body_frame(state, config)
        thrust = np.array([config.thrust(t), 0, 0])
        virtual_force_body = quaternion_util.sum_vector_body_frame(
            [air_force, thrust],
            [Gravitational_acceleration * config.mass(t)],
            state.posture,
        )
        actual_force_inertial = quaternion_util.body_to_inertial(
            state.posture, np.array([max(0, virtual_force_body[0]), 0, 0])
        )
        return RocketState.derivative(
            state, actual_force_inertial / config.mass(t), np.zeros(3)
        )

    def end_condition(t, state):
        return np.linalg.norm(state.position, ord=2) > config.launcher_length

    return ode_solver.runge_kutta4(
        derivative, first_state, first_time, config.dt, end_condition
    )


def simulate_flight(
    first_state: RocketState, config: Config, first_time: float, parachute_on: float
) -> list[tuple[float, RocketState]]:
    """飛行中のシミュレーションを行う

    Args:
        first_state (RocketState): ランチャーから出た瞬間のロケットの状態
        config (Config): ロケットの設定
        first_time (float): ランチャーから出た瞬間の時刻

    Returns:
        list[tuple[float,RocketState]]: 時刻とロケットの状態の組のリスト
    """

    def derivative(t, state):
        air_force, moment = air_force_body_frame(state, config)
        thrust = np.array([config.thrust(t), 0, 0])
        force = quaternion_util.sum_vector_inertial_frame(
            [air_force, thrust], [np.zeros(3)], state.posture
        )
        acceleration = force / config.mass(t) + Gravitational_acceleration
        angular_acceleration = equation_of_motion.angular_acceleration(
            moment, config.inertia_tensor, state.rotation
        )
        return RocketState.derivative(state, acceleration, angular_acceleration)

    def end_condition(t, state):
        if not parachute_on:
            return state.position[2] > 0
        else:
            raise NotImplementedError("パラシュートを開いた時は未実装")

    return ode_solver.runge_kutta4(
        derivative, first_state, first_time, config.dt, end_condition
    )


def simulate(
    config: Config, parachute_on: float
) -> list[list[tuple[float, RocketState]]]:
    """全体のシミュレーションを行う

    Args:
        config (Config): ロケットの設定
        parachute_on (float): パラシュートを開く時刻

    Returns:
        list[list[tuple[float,RocketState]]]: 時刻とロケットの状態の組のリストをモードごとに格納したリスト
    """
    first_posture = quaternion_util.from_euler_angle(
        config.first_elevation, config.first_azimuth, config.first_roll
    )
    first_state = RocketState(np.zeros(3), np.zeros(3), first_posture, np.zeros(3))
    result_launcher = simulate_launcher(first_state, config, 0)
    print("ランチャー上でのシミュレーション終了")
    print(result_launcher[-1][1])
    result_flight = simulate_flight(
        result_launcher[-1][1], config, result_launcher[-1][0], parachute_on
    )
    if parachute_on:
        raise NotImplementedError("パラシュートを開いた時は未実装")
    else:
        return [result_launcher[:-1], result_flight]
