import typing

import numpy as np

from . import air_force, equation_of_motion, ode_solver, quaternion_util, simulation_result
from .config import Config
from .rocket_state import RocketState
from .simulation_context import SimulationContext

Gravitational_acceleration = np.array([0, 0, 9.8])


def to_simulation_result_row(
    time: float,
    state: RocketState,
    context: SimulationContext,
    acceleration_body_frame: np.ndarray,
    *,
    on_launcher: bool,
) -> simulation_result.SimulationResultRow:
    # パラシュートは関係なし
    air_force_result = air_force.calculate(state, context, time, parachute_on=False)
    return simulation_result.SimulationResultRow.from_state(
        time=time,
        state=state,
        context=context,
        acceleration_body_frame=acceleration_body_frame,
        air_force_result=air_force_result,
        on_launcher=on_launcher,
    )


def acceleration_inertial_frame(
    t: float,
    state: RocketState,
    context: SimulationContext,
    *,
    parachute_on: bool,
) -> np.ndarray:
    air_force_result = air_force.calculate(state, context, t, parachute_on=parachute_on)
    thrust = np.array([context.thrust(t), 0, 0])
    force = quaternion_util.sum_vector_inertial_frame(
        [air_force_result.force, thrust],
        [np.zeros(3)],
        state.posture,
    )
    return force / context.mass(t) + Gravitational_acceleration


def angular_acceleration(
    air_force_result: air_force.AirForceResult,
    context: SimulationContext,
    state: RocketState,
) -> np.ndarray:
    return equation_of_motion.angular_acceleration(
        air_force_result.moment,
        context.inertia_tensor,
        state.rotation,
    )


def simulate_launcher(
    first_state: RocketState,
    context: SimulationContext,
    first_time: float,
) -> simulation_result.SimulationResult:
    """ランチャー上でのシミュレーションを行う

    Args:
        first_state (RocketState): 打ち上げ前のロケットの状態
        context (SimulationContext): ロケットの設定
        first_time (float): 初期時刻

    Returns:
        simulation_result.SimulationResult: シミュレーション結果
    """

    def acceleration_body_frame(t: float, state: RocketState) -> np.ndarray:
        acceleration_body_frame_no_constraints = quaternion_util.inertial_to_body(
            state.posture,
            acceleration_inertial_frame(t, state, context, parachute_on=False),
        )
        return np.array([max(0, acceleration_body_frame_no_constraints[0]), 0, 0])

    def derivative(t: float, state: RocketState) -> RocketState:
        actual_acceleration_inertial = quaternion_util.body_to_inertial(
            state.posture,
            acceleration_body_frame(t, state),
        )
        return RocketState.derivative(state, actual_acceleration_inertial, np.zeros(3))

    def end_condition(_: float, state: RocketState) -> bool:
        return np.linalg.norm(state.position, ord=2) > context.launcher_length

    result = ode_solver.runge_kutta4(
        derivative,
        first_state,
        first_time,
        context.dt,
        end_condition,
    )

    result = (
        to_simulation_result_row(
            *row,
            context,
            acceleration_body_frame(*row),
            on_launcher=True,
        )
        for row in result
    )
    return simulation_result.SimulationResult(list(result))


def simulate_flight(
    end_condition: typing.Callable[[float, RocketState], bool],
    *,
    parachute_on: bool,
) -> typing.Callable[
    [RocketState, SimulationContext, float],
    simulation_result.SimulationResult,
]:
    """飛行中のシミュレーションを行う

    Args:
        end_condition (typing.Callable[[float, RocketState], bool]): 終了条件
        parachute_on (bool): パラシュートが開いているか否か

    Returns:
        typing.Callable[[RocketState, SimulationContext, float], simulation_result.SimulationResult]:
            ロケットの初期状態、コンテキスト、初期時刻を受け取り、シミュレーション結果を返す関数
    """

    def body(
        first_state: RocketState,
        context: SimulationContext,
        first_time: float,
    ) -> simulation_result.SimulationResult:
        def derivative(t: float, state: RocketState) -> RocketState:
            # 空気力の計算
            air_force_result = air_force.calculate(state, context, t, parachute_on=parachute_on)
            # 加速度の計算
            acceleration_ = acceleration_inertial_frame(t, state, context, parachute_on=parachute_on)
            angular_acceleration_ = angular_acceleration(
                air_force_result,
                context,
                state,
            )
            return RocketState.derivative(state, acceleration_, angular_acceleration_)

        result = ode_solver.runge_kutta4(
            derivative,
            first_state,
            first_time,
            context.dt,
            end_condition,
        )
        result = (
            to_simulation_result_row(
                *row,
                context,
                quaternion_util.inertial_to_body(
                    row[1].posture,
                    acceleration_inertial_frame(row[0], row[1], context, parachute_on=parachute_on),
                ),
                on_launcher=False,
            )
            for row in result
        )
        return simulation_result.SimulationResult(list(result))

    return body


simulate_on_rise = simulate_flight(lambda _, state: state.velocity[2] > 0, parachute_on=False)


def simulate_waiting_parachute_delay(
    time_fall_start: float,
) -> typing.Callable[
    [RocketState, SimulationContext, float],
    simulation_result.SimulationResult,
]:
    def end_condition(t: float, _: RocketState) -> bool:
        return t > time_fall_start

    return simulate_flight(end_condition, parachute_on=False)


def simulate_fall(
    *,
    parachute_on: bool,
) -> typing.Callable[
    [RocketState, SimulationContext, float],
    simulation_result.SimulationResult,
]:
    def end_condition(_: float, state: RocketState) -> bool:
        return state.position[2] > 0

    return simulate_flight(end_condition, parachute_on=parachute_on)


def simulate(
    config: Config,
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
        context.first_elevation,
        context.first_azimuth,
        context.first_roll,
    )
    first_state = RocketState(np.zeros(3), np.zeros(3), first_posture, np.zeros(3))
    result_launcher = simulate_launcher(first_state, context, 0)
    last = result_launcher.last()
    first_state = last.to_rocket_state()
    result_on_rise = simulate_on_rise(first_state, context, last.time)
    last = result_on_rise.last()
    first_state = last.to_rocket_state()
    result_waiting_parachute_delay = simulate_waiting_parachute_delay(last.time)(
        first_state,
        context,
        last.time,
    )
    last = result_waiting_parachute_delay.last()
    first_state = last.to_rocket_state()
    result_fall_parachute_on = simulate_fall(parachute_on=True)(first_state, context, last.time)
    result_fall_parachute_off = simulate_fall(parachute_on=False)(first_state, context, last.time)
    result_common = result_launcher.join(result_on_rise).join(
        result_waiting_parachute_delay,
    )
    result_parachute_on = result_common.deepcopy().join(result_fall_parachute_on)
    result_parachute_off = result_common.join(result_fall_parachute_off)
    return result_parachute_off, result_parachute_on
