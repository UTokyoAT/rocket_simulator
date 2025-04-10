from dataclasses import dataclass
import numpy as np
import quaternion


@dataclass
class SimulationResultRow:
    """
    ある時刻でのロケットの状態を表す
    """

    time: float
    position: np.ndarray
    velocity: np.ndarray
    posture: quaternion.quaternion
    rotation: np.ndarray
    dynamic_pressure: float
    burning: bool
    on_launcher: bool
    velocity_air_body_frame: np.ndarray
    acceleration_body_frame: np.ndarray


@dataclass
class SimulationResult:
    """
    シミュレーションの結果を表すクラス
    """

    result: list[SimulationResultRow]
    """シミュレーションの結果"""

    @classmethod
    def init_empty(cls) -> "SimulationResult":
        """空のシミュレーション結果を初期化する"""
        return cls(result=[])

    def append(self, row: SimulationResultRow):
        """列を追加する

        Args:
            row (SimulationResultRow): 追加する列
        """
        self.result.append(row)

    def join(
        self,
        other: "SimulationResult",
    ) -> "SimulationResult":
        """他のシミュレーション結果と結合する
        このインスタンスが前、otherが後ろに結合される
        このインスタンスの最後の要素は除かれる

        Args:
            other (SimulationResult): 結合するシミュレーション結果

        Returns:
            SimulationResult: 結合したシミュレーション結果
        """
        assert self.result[-1].time == other.result[0].time
        return SimulationResult(self.result[:-1] + other.result)

    def last(self) -> SimulationResultRow:
        """最後の行を取得する

        Returns:
            SimulationResultRow: 最後の行
        """
        return self.result[-1]
