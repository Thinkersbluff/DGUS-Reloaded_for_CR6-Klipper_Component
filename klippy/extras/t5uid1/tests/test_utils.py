import unittest
import decimal
from ..bin.t5uid1_utils import round_up, bitwise_and, bitwise_or

class TestT5UID1Utils(unittest.TestCase):

    def test_round_up(self):
        self.assertEqual(
            round_up(3.14159, '0.01'),
            decimal.Decimal('3.15')
        )
        self.assertEqual(
            round_up(2.001, '1'),
            decimal.Decimal('3')  # Ceiling round to nearest whole number
        )
        self.assertEqual(
            round_up(2.301, '0.1'),
            decimal.Decimal('2.4')  # Ceiling round to nearest whole number
        )

    def test_bitwise_and(self):
        self.assertEqual(bitwise_and(0b1010, 0b1100), 0b1000)
        self.assertEqual(bitwise_and(0b1111, 0b0000), 0b0000)

    def test_bitwise_or(self):
        self.assertEqual(bitwise_or(0b1010, 0b1100), 0b1110)
        self.assertEqual(bitwise_or(0b0001, 0b0010), 0b0011)

if __name__ == '__main__':
    unittest.main()