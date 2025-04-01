import src.core.interpolation as i
import unittest
import numpy as np
import pandas as pd

class TestInterpolation(unittest.TestCase):
    def test_linear_interpolation(self):
        df = pd.DataFrame({'b':[2,3,4]}, index=[1,2,3])
        f = i.df_to_function_1d(df)
        self.assertTrue(np.abs(f(1.5) - 2.5) < 1e-10)

if __name__ == '__main__':
    unittest.main()