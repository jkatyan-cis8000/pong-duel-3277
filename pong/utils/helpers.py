"""Utils layer for Pong game."""

from pong.types import Position

def clamp(value: int, min_val: int, max_val: int) -> int:
    """Clamp a value to be within min and max."""
    return max(min_val, min(value, max_val))


def abs_val(x: int) -> int:
    """Absolute value for integers."""
    return -x if x < 0 else x
