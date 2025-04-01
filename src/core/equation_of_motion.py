import numpy as np
from . import inertia_tensor as it


def angular_acceleration(
    moment: np.ndarray, inertia: it.InertiaTensor, rotation
) -> np.ndarray:
    """慣性系での角加速度を計算する

    Args:
        moment (np.ndarray): 静止系でのトルク
        inertia_inverse (np.ndarray): 慣性テンソルの逆行列
        rotation (np.ndarray): 剛体系での角速度

    Returns:
        np.ndarray: 慣性系での角加速度
    """
    return inertia.inverse @ (moment - np.cross(rotation, inertia.tensor @ rotation))
