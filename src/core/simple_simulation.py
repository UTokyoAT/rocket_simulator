import numpy as np
from . import air_force as af
from .rocket_state import RocketState
from . import quaternion_util
from . import ode_solver
from . import equation_of_motion
from . import simulation_result
from .simulation_context import SimulationContext


def air_force_body_frame(
    rocket_state: RocketState, context: SimulationContext
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
        rocket_state.velocity - context.wind(-rocket_state.position[2]),
    )
    angle_of_attack = af.angle_of_attack(airspeed)
    air_density = 1.204
    axial_force = af.axial_force(airspeed, air_density, context.body_area, context.CA)
    CN = af.normal_force_coefficient(angle_of_attack, context.CN_alpha)
    normal_force = af.normal_force(airspeed, air_density, context.body_area, CN)
    air_force = axial_force + normal_force
    moment = af.air_force_moment(
        air_force,
        context.wind_center,
    )
    return air_force, moment


Gravitational_acceleration = np.array([0, 0, 9.8])


def to_simulation_result_row(
    time: float, state: RocketState
) -> simulation_result.SimulationResultRow:
    return simulation_result.SimulationResultRow(
        time=time,
        position=state.position,
        velocity=state.velocity,
        posture=state.posture,
        rotation=state.rotation,
    )


def simulate_launcher(
    first_state: RocketState, context: SimulationContext, first_time: float
) -> simulation_result.SimulationResult:
    """ランチャー上でのシミュレーションを行う

    Args:
        first_state (RocketState): 打ち上げ前のロケットの状態
        config (Config): ロケットの設定
        first_time (float): 初期時刻

    Returns:
        simulation_result.SimulationResult: 時刻とロケットの状態の組のリスト
    """

    def derivative(t, state):
        air_force, _ = air_force_body_frame(state, context)
        thrust = np.array([context.thrust(t), 0, 0])
        virtual_force_body = quaternion_util.sum_vector_body_frame(
            [air_force, thrust],
            [Gravitational_acceleration * context.mass(t)],
            state.posture,
        )
        actual_force_inertial = quaternion_util.body_to_inertial(
            state.posture, np.array([max(0, virtual_force_body[0]), 0, 0])
        )
        return RocketState.derivative(
            state, actual_force_inertial / context.mass(t), np.zeros(3)
        )

    def end_condition(t, state):
        return np.linalg.norm(state.position, ord=2) > context.launcher_length

    result = ode_solver.runge_kutta4(
        derivative, first_state, first_time, context.dt, end_condition
    )
    result = map(lambda row: to_simulation_result_row(*row), result)
    return simulation_result.SimulationResult(list(result))


def simulate_flight(
    first_state: RocketState,
    context: SimulationContext,
    first_time: float,
    parachute_on: float,
) -> simulation_result.SimulationResult:
    """飛行中のシミュレーションを行う

    Args:
        first_state (RocketState): ランチャーから出た瞬間のロケットの状態
        config (Config): ロケットの設定
        first_time (float): ランチャーから出た瞬間の時刻

    Returns:
        simulation_result.SimulationResult: 時刻とロケットの状態の組のリスト
    """

    def derivative(t, state):
        air_force, moment = air_force_body_frame(state, context)
        thrust = np.array([context.thrust(t), 0, 0])
        force = quaternion_util.sum_vector_inertial_frame(
            [air_force, thrust], [np.zeros(3)], state.posture
        )
        acceleration = force / context.mass(t) + Gravitational_acceleration
        angular_acceleration = equation_of_motion.angular_acceleration(
            moment, context.inertia_tensor, state.rotation
        )
        return RocketState.derivative(state, acceleration, angular_acceleration)

    def end_condition(t, state):
        if not parachute_on:
            return state.position[2] > 0
        else:
            raise NotImplementedError("パラシュートを開いた時は未実装")

    result = ode_solver.runge_kutta4(
        derivative, first_state, first_time, context.dt, end_condition
    )
    result = map(lambda row: to_simulation_result_row(*row), result)
    return simulation_result.SimulationResult(list(result))


def simulate(context: SimulationContext, parachute_on: float) -> simulation_result.SimulationResult:
    """全体のシミュレーションを行う

    Args:
        config (Config): ロケットの設定
        parachute_on (float): パラシュートを開く時刻

    Returns:
        simulation_result.SimulationResult: 時刻とロケットの状態の組のリストをモードごとに格納したリスト
    """
    first_posture = quaternion_util.from_euler_angle(
        context.first_elevation, context.first_azimuth, context.first_roll
    )
    first_state = RocketState(np.zeros(3), np.zeros(3), first_posture, np.zeros(3))
    result_launcher = simulate_launcher(first_state, context, 0)
    print("ランチャー上でのシミュレーション終了")
    print(result_launcher.last())
    last = result_launcher.last()
    first_state = RocketState(
        last.position,
        last.velocity,
        last.posture,
        last.rotation,
    )
    result_flight = simulate_flight(first_state, context, last.time, parachute_on)
    if parachute_on:
        raise NotImplementedError("パラシュートを開いた時は未実装")
    else:
        return result_launcher.join(result_flight)
