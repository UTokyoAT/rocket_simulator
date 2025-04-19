import typing as t


def runge_kutta4(
    f: t.Callable[[float, t.Any], t.Any],
    initial_state: t.Any,
    initial_time: float,
    time_step: float,
    end_condition: t.Callable[[float, t.Any], bool],
) -> list[tuple[float, t.Any]]:
    """Runge-Kutta法による常微分方程式の数値解法

    Args:
        f (t.Callable[[float,t.Any],t.Any]): 微分を求める式(dy/dt=f(y,t))
        initial_state (t.Any): 初期状態
        initial_time (float): 初期時刻
        time_step (float): 時間の刻み幅
        end_condition (t.Callable[[float,t.Any],bool]): 終了条件（Trueを返すと終了する）

    Returns:
        list[tuple[float,t.Any]]: 時刻と状態のリスト
    """
    result = [(initial_time, initial_state)]
    while not end_condition(*result[-1]):
        t_n, y_n = result[-1]
        k1 = f(t_n, y_n)
        k2 = f(t_n + time_step / 2, y_n + k1 * (time_step / 2))
        k3 = f(t_n + time_step / 2, y_n + k2 * (time_step / 2))
        k4 = f(t_n + time_step, y_n + k3 * time_step)
        y_n1 = y_n + (k1 + k2 * 2 + k3 * 2 + k4) * (time_step / 6)
        result.append((t_n + time_step, y_n1))
    return result
