from dataclasses import dataclass

import numpy as np
import quaternion as quart

from . import quaternion_util


@dataclass
class RocketState:
    """ある時刻におけるロケットの状態を表すクラス"""

    position: np.ndarray
    """慣性系でのロケットの位置"""
    velocity: np.ndarray
    """慣性系でのロケットの速度"""
    posture: quart.quaternion
    """慣性系でのロケットの姿勢"""
    rotation: np.ndarray
    """剛体系でのロケットの角速度"""

    def __add__(self, other: "RocketState") -> "RocketState":
        return RocketState(
            self.position + other.position,
            self.velocity + other.velocity,
            self.posture + other.posture,
            self.rotation + other.rotation,
        )

    def __mul__(self, other: float) -> "RocketState":
        return RocketState(
            self.position * other,
            self.velocity * other,
            self.posture * other,
            self.rotation * other,
        )

    @classmethod
    def derivative(
        cls,
        rocket_state: "RocketState",
        acceleration: np.ndarray,
        angular_acceleration: np.ndarray,
    ) -> "RocketState":
        """時間微分を計算する

        Args:
            rocket_state (RocketState): ロケットの状態
            acceleration (np.ndarray): 慣性系での加速度
            angular_acceleration (np.ndarray): 剛体系での角加速度
        """
        dq_dt = quaternion_util.quaternion_derivative(
            rocket_state.posture,
            rocket_state.rotation,
        )
        return RocketState(
            rocket_state.velocity,
            acceleration,
            dq_dt,
            angular_acceleration,
        )
