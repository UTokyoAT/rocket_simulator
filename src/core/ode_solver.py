from collections.abc import Callable
from typing import Protocol, TypeVar


class Vector(Protocol):
    """スカラー演算をサポートする型のプロトコル"""

    def __add__(self, other: "Vector") -> "Vector":
        raise NotImplementedError

    def __mul__(self, other: float) -> "Vector":
        raise NotImplementedError


T = TypeVar("T", bound=Vector)  # スカラー演算をサポートする型変数


def runge_kutta4(
    f: Callable[[float, T], T],
    initial_state: T,
    initial_time: float,
    time_step: float,
    end_condition: Callable[[float, T], bool],
) -> list[tuple[float, T]]:
    """Runge-Kutta法による常微分方程式の数値解法

    Args:
        f (Callable[[float, T], T]): 微分を求める式(dy/dt=f(y,t))
        initial_state (T): 初期状態
        initial_time (float): 初期時刻
        time_step (float): 時間の刻み幅
        end_condition (Callable[[float, T], bool]): 終了条件(Trueを返すと終了する)

    Returns:
        List[Tuple[float, T]]: 時刻と状態のリスト
    """
    result = [(initial_time, initial_state)]
    while not end_condition(result[-1][0], result[-1][1]):
        t_n, y_n = result[-1]
        k1 = f(t_n, y_n)
        k2 = f(t_n + time_step / 2, y_n + k1 * (time_step / 2))
        k3 = f(t_n + time_step / 2, y_n + k2 * (time_step / 2))
        k4 = f(t_n + time_step, y_n + k3 * time_step)
        y_n1 = y_n + (k1 + k2 * 2 + k3 * 2 + k4) * (time_step / 6)
        result.append((t_n + time_step, y_n1))
    return result
