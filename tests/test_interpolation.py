import src.core.interpolation as i
import unittest
import numpy as np
import pandas as pd


class TestInterpolation(unittest.TestCase):
    def test_linear_interpolation(self):
        df = pd.DataFrame({"b": [2, 3, 4]}, index=[1, 2, 3])
        f = i.df_to_function_1d(df)
        self.assertTrue(np.abs(f(1.5) - 2.5) < 1e-10)

    def test_linear_interpolation_array(self):
        # テスト用データフレーム（値がnp.ndarray）を作成
        df = pd.DataFrame(
            {
                "gravity_center": [
                    np.array([1.0, 0.0, 0.0]),
                    np.array([2.0, 0.0, 0.0]),
                    np.array([3.0, 0.0, 0.0]),
                ]
            },
            index=[1, 2, 3],
        )

        # 配列を返す関数を取得
        f = i.df_to_function_1d_array(df)

        # 補間結果がnumpy配列であることを確認
        result = f(1.5)
        self.assertIsInstance(result, np.ndarray)

        # 値が正しく補間されていることを確認
        expected = np.array([1.5, 0.0, 0.0])
        np.testing.assert_array_almost_equal(result, expected)

        # 整数インデックスでの補間を確認
        np.testing.assert_array_almost_equal(f(1), np.array([1.0, 0.0, 0.0]))
        np.testing.assert_array_almost_equal(f(2), np.array([2.0, 0.0, 0.0]))
        np.testing.assert_array_almost_equal(f(3), np.array([3.0, 0.0, 0.0]))

        # 範囲外の値で例外が発生することを確認
        with self.assertRaises(ValueError):
            f(0)  # 下限値より小さい値

        with self.assertRaises(ValueError):
            f(4)  # 上限値より大きい値


if __name__ == "__main__":
    unittest.main()
