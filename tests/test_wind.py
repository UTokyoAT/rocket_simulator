import unittest

import numpy as np

import src.core.wind as w


class TestWind(unittest.TestCase):
    def test_init(self) -> None:
        wind = w.wind_velocity_power(2, 3, 5, 30)
        wind_10 = wind(10)
        expected = 4.139188984383644 * np.array([-((3) ** 0.5) / 2, -0.5, 0])
        np.testing.assert_array_almost_equal(wind_10, expected)


if __name__ == "__main__":
    unittest.main()
