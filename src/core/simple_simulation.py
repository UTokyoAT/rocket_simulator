import typing
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
    air_force_result = air_force.calculate(
        state, context, False
    )  # parachute_onは無関係
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
    t: float, state: RocketState, context: SimulationContext, parachute_on: bool
) -> np.ndarray:
    air_force_result = air_force.calculate(state, context, parachute_on)
    thrust = np.array([context.thrust(t), 0, 0])
    force = quaternion_util.sum_vector_inertial_frame(
        [air_force_result.force, thrust], [np.zeros(3)], state.posture
    )
    return force / context.mass(t) + Gravitational_acceleration


def angular_acceleration(
    air_force_result: air_force.AirForceResult,
    context: SimulationContext,
    state: RocketState,
):
    return equation_of_motion.angular_acceleration(
        air_force_result.moment, context.inertia_tensor, state.rotation
    )


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
            acceleration_inertial_frame(t, state, context, False),
        )
        return np.array([max(0, acceleration_body_frame_no_constraints[0]), 0, 0])

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
    end_condition: typing.Callable[[float, RocketState], bool], parachute_on: bool
) -> typing.Callable[
    [RocketState, SimulationContext, float], simulation_result.SimulationResult
]:
    """飛行中のシミュレーションを行う

    Args:
        end_condition (typing.Callable[[float, RocketState], bool]): 終了条件
    """

    def body(
        first_state: RocketState,
        context: SimulationContext,
        first_time: float,
    ) -> simulation_result.SimulationResult:

        def derivative(t, state):
            air_force_result = air_force.calculate(state, context, parachute_on)
            acceleration_ = acceleration_inertial_frame(t, state, context, parachute_on)
            angular_acceleration_ = angular_acceleration(
                air_force_result, context, state
            )
            return RocketState.derivative(state, acceleration_, angular_acceleration_)

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
                    acceleration_inertial_frame(row[0], row[1], context, parachute_on),
                ),
            ),
            result,
        )
        return simulation_result.SimulationResult(list(result))

    return body


simulate_on_rise = simulate_flight(lambda t, state: state.velocity[2] > 0, False)


def simulate_waiting_parachute_delay(
    time_fall_start: float,
) -> typing.Callable[
    [RocketState, SimulationContext, float], simulation_result.SimulationResult
]:
    def end_condition(t, state):
        return t > time_fall_start

    return simulate_flight(end_condition, False)


def simulate_fall(
    parachute_on: bool,
) -> typing.Callable[
    [RocketState, SimulationContext, float], simulation_result.SimulationResult
]:
    def end_condition(t, state):
        return state.position[2] > 0

    return simulate_flight(end_condition, parachute_on)


def rocket_state_from_simulation_result_row(
    row: simulation_result.SimulationResultRow,
) -> RocketState:
    return RocketState(
        row.position,
        row.velocity,
        row.posture,
        row.rotation,
    )


def simulate(
    config: Config, parachute_on: float
) -> tuple[simulation_result.SimulationResult, simulation_result.SimulationResult]:
    """全体のシミュレーションを行う

    Args:
        config (Config): ロケットの設定
        parachute_on (float): パラシュートを開く時刻

    Returns:
        tuple[simulation_result.SimulationResult, simulation_result.SimulationResult]:
            [パラシュートが開かなかった場合, パラシュートが開いた場合]
    """
    context = SimulationContext(config)
    first_posture = quaternion_util.from_euler_angle(
        context.first_elevation, context.first_azimuth, context.first_roll
    )
    first_state = RocketState(np.zeros(3), np.zeros(3), first_posture, np.zeros(3))
    result_launcher = simulate_launcher(first_state, context, 0)
    last = result_launcher.last()
    first_state = rocket_state_from_simulation_result_row(last)
    result_on_rise = simulate_on_rise(first_state, context, last.time)
    last = result_on_rise.last()
    first_state = rocket_state_from_simulation_result_row(last)
    result_waiting_parachute_delay = simulate_waiting_parachute_delay(last.time)(
        first_state, context, last.time
    )
    last = result_waiting_parachute_delay.last()
    first_state = rocket_state_from_simulation_result_row(last)
    result_fall_parachute_on = simulate_fall(True)(first_state, context, last.time)
    result_fall_parachute_off = simulate_fall(False)(first_state, context, last.time)
    result_common = result_launcher.join(result_on_rise).join(
        result_waiting_parachute_delay
    )
    result_parachute_on = result_common.deepcopy().join(result_fall_parachute_on)
    result_parachute_off = result_common.join(result_fall_parachute_off)
    return result_parachute_off, result_parachute_on
