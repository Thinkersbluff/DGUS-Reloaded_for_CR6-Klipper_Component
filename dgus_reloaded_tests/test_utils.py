import sys
from unittest.mock import MagicMock

# Mock 'mcu' module to prevent import errors when running outside Klipper/hardware
sys.modules['mcu'] = MagicMock()

import os
# Ensure bin/ is importable no matter test runner (unittest/pytest)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dgus_reloaded.bin import t5uid1_utils

import unittest
import decimal

class TestT5UID1Utils(unittest.TestCase):

    def test_round_up(self):
        # Test rounding up to nearest hundredth
        self.assertEqual(
            t5uid1_utils.round_up(3.14159, '0.01'),
            decimal.Decimal('3.15')
        )
        # Test rounding up to nearest whole number
        self.assertEqual(
            t5uid1_utils.round_up(2.001, '1'),
            decimal.Decimal('3')
        )
        # Test rounding up to nearest tenth
        self.assertEqual(
            t5uid1_utils.round_up(2.301, '0.1'),
            decimal.Decimal('2.4')
        )

    def test_bitwise_and(self):
        self.assertEqual(t5uid1_utils.bitwise_and(0b1010, 0b1100), 0b1000)
        self.assertEqual(t5uid1_utils.bitwise_and(0b1111, 0b0000), 0b0000)

    def test_bitwise_or(self):
        self.assertEqual(t5uid1_utils.bitwise_or(0b1010, 0b1100), 0b1110)
        self.assertEqual(t5uid1_utils.bitwise_or(0b0001, 0b0010), 0b0011)

if __name__ == '__main__':
    unittest.main()