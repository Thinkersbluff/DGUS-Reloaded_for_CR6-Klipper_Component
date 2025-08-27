"""Generic utility functions - imported by t5uid1.py"""

import decimal
import time
from typing import Optional, Union

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

# New helpers moved from t5uid1 (get_duration, get_remaining, map_value_range, get_now)

def get_now(reactor: Optional[object] = None) -> float:
    """
    Return a monotonic timestamp in seconds.
    If a reactor with monotonic() is provided, use that; otherwise fallback to time.time().
    """
    try:
        if reactor is not None and hasattr(reactor, "monotonic"):
            return reactor.monotonic()
    except Exception:
        pass
    return time.time()

def get_duration(start: float, end: Optional[float] = None, reactor: Optional[object] = None) -> float:
    """
    Return a non-negative duration (seconds) between start and end.
    If end is None, use get_now().
    """
    if end is None:
        end = get_now(reactor)
    try:
        dur = float(end) - float(start)
    except Exception:
        return 0.0
    return dur if dur >= 0.0 else 0.0

def get_remaining(total: float, elapsed: float) -> float:
    """Return non-negative remaining time given total and elapsed seconds."""
    try:
        rem = float(total) - float(elapsed)
    except Exception:
        return 0.0
    return rem if rem > 0.0 else 0.0

def map_value_range(value: Union[int, float],
                    in_min: Union[int, float],
                    in_max: Union[int, float],
                    out_min: Union[int, float],
                    out_max: Union[int, float],
                    clamp: bool = True) -> float:
    """
    Map `value` from input range to output range.
    If clamp is True, clamp value to [in_min, in_max] before mapping.
    """
    try:
        v = float(value)
        imin = float(in_min)
        imax = float(in_max)
        omin = float(out_min)
        omax = float(out_max)
        if imax == imin:
            # avoid division by zero; return midpoint of output
            return (omin + omax) / 2.0
        if clamp:
            if v < imin:
                v = imin
            elif v > imax:
                v = imax
        ratio = (v - imin) / (imax - imin)
        return omin + ratio * (omax - omin)
    except Exception:
        return float(out_min)
