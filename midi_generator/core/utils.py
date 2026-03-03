from __future__ import annotations


def clamp(n: int, low: int, high: int) -> int:
    return max(low, min(high, n))

