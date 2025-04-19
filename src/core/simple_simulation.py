import numpy as np
from . import air_force
from .rocket_state import RocketState
from . import quaternion_util
from . import ode_solver
from . import equation_of_motion
from . import simulation_result
from .simulation_context import SimulationContext
from .config import Config


Gravitational_acceleration = np.array([0, 0, 9.8])


def to_simulation_result_row(
    time: float,
    state: RocketState,
    context: SimulationContext,
    on_launcher: bool,
    acceleration_body_frame: np.ndarray,
) -> simulation_result.SimulationResultRow:
    air_force_result = air_force.calculate(state, context)
    return simulation_result.SimulationResultRow(
        time=time,
        position=state.position,
        velocity=state.velocity,
        posture=state.posture,
        rotation=state.rotation,
        dynamic_pressure=air_force_result.dynamic_pressure,
        burning=context.thrust(time) > 1e-10,
        on_launcher=on_launcher,
        velocity_air_body_frame=air_force_result.velocity_air_body_frame,
        acceleration_body_frame=acceleration_body_frame,
    )


def acceleration_inertial_frame(
    t: float, state: RocketState, context: SimulationContext
) -> np.ndarray:
    air_force_result = air_force.calculate(state, context)
    thrust = np.array([context.thrust(t), 0, 0])
    force = quaternion_util.sum_vector_inertial_frame(
        [air_force_result.force, thrust], [np.zeros(3)], state.posture
    )
    return force / context.mass(t) + Gravitational_acceleration


def simulate_launcher(
    first_state: RocketState, context: SimulationContext, first_time: float
) -> simulation_result.SimulationResult:
    """ランチャー上でのシミュレーションを行う

    Args:
        first_state (RocketState): 打ち上げ前のロケットの状態
        context (SimulationContext): ロケットの設定
        first_time (float): 初期時刻

    Returns:
        simulation_result.SimulationResult: 時刻とロケットの状態の組のリスト
    """

    def acceleration_body_frame(t: float, state: RocketState) -> np.ndarray:
        acceleration_body_frame_no_constraints = quaternion_util.inertial_to_body(
            state.posture,
            acceleration_inertial_frame(t, state, context),
        )
        return np.array(
            [max(0, acceleration_body_frame_no_constraints[0]), 0, 0]
        )

    def derivative(t, state):
        actual_acceleration_inertial = quaternion_util.body_to_inertial(
            state.posture, acceleration_body_frame(t, state)
        )
        return RocketState.derivative(state, actual_acceleration_inertial, np.zeros(3))

    def end_condition(t, state):
        return np.linalg.norm(state.position, ord=2) > context.launcher_length

    result = ode_solver.runge_kutta4(
        derivative, first_state, first_time, context.dt, end_condition
    )

    result = map(
        lambda row: to_simulation_result_row(
            *row, context, True, acceleration_body_frame(*row)
        ),
        result,
    )
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
        context (SimulationContext): ロケットの設定
        first_time (float): ランチャーから出た瞬間の時刻

    Returns:
        simulation_result.SimulationResult: 時刻とロケットの状態の組のリスト
    """

    def derivative(t, state):
        air_force_result = air_force.calculate(state, context)
        acceleration_ = acceleration_inertial_frame(t, state, context)
        angular_acceleration = equation_of_motion.angular_acceleration(
            air_force_result.moment, context.inertia_tensor, state.rotation
        )
        return RocketState.derivative(state, acceleration_, angular_acceleration)

    def end_condition(t, state):
        if not parachute_on:
            return state.position[2] > 0
        else:
            raise NotImplementedError("パラシュートを開いた時は未実装")

    result = ode_solver.runge_kutta4(
        derivative, first_state, first_time, context.dt, end_condition
    )
    result = map(
        lambda row: to_simulation_result_row(
            *row,
            context,
            False,
            quaternion_util.inertial_to_body(
                row[1].posture,
                acceleration_inertial_frame(row[0], row[1], context)
            ),
        ),
        result,
    )
    return simulation_result.SimulationResult(list(result))


def simulate(config: Config, parachute_on: float) -> simulation_result.SimulationResult:
    """全体のシミュレーションを行う

    Args:
        config (Config): ロケットの設定
        parachute_on (float): パラシュートを開く時刻

    Returns:
        simulation_result.SimulationResult: 時刻とロケットの状態の組のリストをモードごとに格納したリスト
    """
    context = SimulationContext(config)
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
