import math
import unittest
import pandas as pd
from narrative_watch_v4 import rsi, buy_signal, narrative_phase

class IndicatorTests(unittest.TestCase):
    def test_insufficient_data(self):
        self.assertTrue(math.isnan(rsi(pd.Series([1., 2.]))))
    def test_rising_series_is_overbought(self):
        self.assertEqual(rsi(pd.Series(range(20), dtype=float)), 100.0)
    def test_falling_series_is_oversold(self):
        self.assertEqual(rsi(pd.Series(range(20, 0, -1), dtype=float)), 0.0)
    def test_flat_series_is_neutral(self):
        self.assertEqual(rsi(pd.Series([4.] * 20)), 50.0)
    def test_missing_indicator_does_not_buy(self):
        self.assertEqual(buy_signal('green', 100, 90, 80, float('nan')), 'HOLD')
    def test_hype_phase(self):
        self.assertEqual(narrative_phase(110, 100, 90, 80), 'Hype')
