import numpy as np


class InertiaTensor:
    """慣性テンソルを表すクラス"""

    tensor: np.ndarray
    """慣性テンソル"""
    inverse: np.ndarray
    """慣性テンソルの逆行列"""

    def __init__(self, I_xx: float, I_yy: float, I_zz: float, I_xy, I_yz, I_zx):

        self.tensor = np.array(
            [[I_xx, I_xy, I_zx], [I_xy, I_yy, I_yz], [I_zx, I_yz, I_zz]]
        )
        self.inverse = np.linalg.inv(self.tensor)
