import app.core.wind as w
import unittest
import numpy as np

class TestWind(unittest.TestCase):
    def test_init(self):
        wind = w.wind_velocity_power(2,3,5,30)
        wind_10 = wind(10)
        self.assertTrue(np.all(np.abs(wind_10 - 4.139188984383644 * np.array([-(3)**0.5/2,-0.5,0])) < 1e-10))

if __name__ == '__main__':
    unittest.main()