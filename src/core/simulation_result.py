from dataclasses import dataclass
import copy
import numpy as np
import quaternion
import pandas as pd


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

    def to_df_row(self) -> list:
        """DataFrame用の行に変換する

        Returns:
            list: DataFrameの行
        """
        return [
            self.time,
            *self.position,
            *self.velocity,
            self.posture.w,
            self.posture.x,
            self.posture.y,
            self.posture.z,
            *self.rotation,
            self.dynamic_pressure,
            self.burning,
            self.on_launcher,
            *self.velocity_air_body_frame,
            *self.acceleration_body_frame,
        ]


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

    def deepcopy(self) -> "SimulationResult":
        """シミュレーション結果をディープコピーする

        Returns:
            SimulationResult: ディープコピーしたシミュレーション結果
        """
        return copy.deepcopy(self)

    def last(self) -> SimulationResultRow:
        """最後の行を取得する

        Returns:
            SimulationResultRow: 最後の行
        """
        return self.result[-1]

    def to_df(self) -> pd.DataFrame:
        """DataFrameに変換する

        Returns:
            pd.DataFrame: DataFrame
        """
        df = pd.DataFrame([row.to_df_row() for row in self.result])
        df.columns = [
            "time",
            "position_n",
            "position_e",
            "position_d",
            "velocity_n",
            "velocity_e",
            "velocity_d",
            "posture_w",
            "posture_x",
            "posture_y",
            "posture_z",
            "rotation_n",
            "rotation_e",
            "rotation_d",
            "dynamic_pressure",
            "burning",
            "on_launcher",
            "velocity_air_body_frame_x",
            "velocity_air_body_frame_y",
            "velocity_air_body_frame_z",
            "acceleration_body_frame_x",
            "acceleration_body_frame_y",
            "acceleration_body_frame_z",
        ]
        return df
