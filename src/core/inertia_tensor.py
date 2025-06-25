import numpy as np


class InertiaTensor:
    """慣性テンソルを表すクラス"""

    tensor: np.ndarray
    """慣性テンソル"""
    inverse: np.ndarray
    """慣性テンソルの逆行列"""

    def __init__(self, i_xx: float, i_yy: float, i_zz: float, i_xy: float, i_yz: float, i_zx: float) -> None:
        self.tensor = np.array(
            [[i_xx, i_xy, i_zx], [i_xy, i_yy, i_yz], [i_zx, i_yz, i_zz]],
        )
        self.inverse = np.linalg.inv(self.tensor)
