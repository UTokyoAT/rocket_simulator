import numpy as np

from src.util.type import NPVector

from . import inertia_tensor as it


def angular_acceleration(
    moment: NPVector,
    inertia: it.InertiaTensor,
    rotation: NPVector,
) -> NPVector:
    """慣性系での角加速度を計算する

    Args:
        moment (NPVector): 静止系でのトルク
        inertia (it.InertiaTensor): 慣性テンソル
        rotation (NPVector): 剛体系での角速度

    Returns:
        NPVector: 慣性系での角加速度
    """
    return inertia.inverse @ (moment - np.cross(rotation, inertia.tensor @ rotation))
