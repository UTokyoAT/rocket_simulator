import unittest

import numpy as np
import pandas as pd

from src.core import gravity_center


class TestGravityCenter(unittest.TestCase):
    def test_thrust_end_time(self) -> None:
        # テスト用の推力データフレームを作成
        thrust_df = pd.DataFrame(
            {"thrust": [100.0, 50.0, 1.0, 0.0, 0.0]},
            index=[0.0, 1.0, 2.0, 3.0, 4.0],
        )

        # 関数をテスト
        result = gravity_center.thrust_end_time(thrust_df)
        self.assertEqual(result, 3.0)
        self.assertIsInstance(result, float)

    def test_create_gravity_center_function_from_dataframe_interpolation(self) -> None:
        # テスト用のデータを作成(3次元ベクトル)
        first_gravity_center = np.array([0.0, 0.0, 0.0])
        end_gravity_center = np.array([1.0, 1.0, 1.0])
        thrust_df = pd.DataFrame(
            {"thrust": [100.0, 50.0, 1.0, 0.0, 0.0]},
            index=[0.0, 1.0, 2.0, 3.0, 4.0],
        )

        # 関数を作成
        gc_func = gravity_center.create_gravity_center_function_from_dataframe(
            first_gravity_center,
            end_gravity_center,
            thrust_df,
        )

        # 補間が正しく機能していることを確認
        np.testing.assert_array_almost_equal(gc_func(0.0), first_gravity_center)
        np.testing.assert_array_almost_equal(gc_func(3.0), end_gravity_center)

        # 中間値の補間を確認
        expected_mid = np.array([0.5, 0.5, 0.5])  # 1.5秒時点では中間値
        np.testing.assert_array_almost_equal(gc_func(1.5), expected_mid)


if __name__ == "__main__":
    unittest.main()
