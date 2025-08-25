"""Generic utility functions - imported by t5uid1.py"""

import decimal

def round_up(value, num_dec_places):
    """Use to round variables up to the specified number of decimal places"""
    num = decimal.Decimal(value)
    rounded_up = num.quantize(decimal.Decimal(str(num_dec_places)), rounding=decimal.ROUND_CEILING)
    return rounded_up

def bitwise_and(lhs, rhs):
    """Perform bitwise AND"""
    return lhs & rhs

def bitwise_or(lhs, rhs):
    """Perform bitwise OR"""
    return lhs | rhs

def format_fixed(value, places):
    '''Format a float to a fixed number of decimal places.'''
    return "{:.{}f}".format(float(value), places)