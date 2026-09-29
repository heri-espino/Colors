"""Contrast-ratio mathematics."""

from __future__ import annotations

import math

import numpy as np


def luminance_ladder(
    levels: int,
    ratio: float,
    *,
    start_luminance: float = 1.0,
) -> np.ndarray:
    r"""Generate luminances with a constant adjacent WCAG contrast ratio.

    For descending relative luminances ``Y_k`` and a fixed ratio ``r``,

    .. math::

       \frac{Y_k + 0.05}{Y_{k+1} + 0.05} = r,

    hence

    .. math::

       Y_k = \frac{Y_0 + 0.05}{r^k} - 0.05.

    Raises
    ------
    ValueError
        If the requested number of levels cannot fit in ``Y in [0, 1]``.
    """
    if levels < 1:
        raise ValueError("levels must be >= 1.")
    if ratio < 1:
        raise ValueError("ratio must be >= 1.")
    if not 0 <= start_luminance <= 1:
        raise ValueError("start_luminance must lie in [0, 1].")

    k = np.arange(levels, dtype=float)
    values = (start_luminance + 0.05) / np.power(ratio, k) - 0.05
    if np.any(values < -1e-12):
        max_levels = 1 + int(
            math.floor(math.log((start_luminance + 0.05) / 0.05) / math.log(ratio))
        ) if ratio > 1 else math.inf
        raise ValueError(
            f"{levels} levels at ratio={ratio:g} do not fit in the luminance range; "
            f"at most {max_levels} levels fit from start_luminance={start_luminance:g}."
        )
    return np.clip(values, 0, 1)


def luminance_contrast(y_a: float, y_b: float) -> float:
    """Contrast ratio computed directly from two relative luminances."""
    if not (0 <= y_a <= 1 and 0 <= y_b <= 1):
        raise ValueError("luminances must lie in [0, 1].")
    hi, lo = max(y_a, y_b), min(y_a, y_b)
    return (hi + 0.05) / (lo + 0.05)
