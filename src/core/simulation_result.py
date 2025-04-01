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


@dataclass
class SimulationResult:
    """
    シミュレーションの結果を表すクラス
    """

    result: list[SimulationResultRow]
    """シミュレーションの結果"""

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
