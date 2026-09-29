"""Alpha compositing and apparent-color compensation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .color_spaces import RGBLike, to_hex, to_rgb


@dataclass(frozen=True)
class AlphaCompensation:
    """Result of compensating a transparent foreground for a background."""

    target_rgb: np.ndarray
    source_rgb: np.ndarray
    displayed_rgb: np.ndarray
    background_rgb: np.ndarray
    alpha: float
    feasible: bool

    @property
    def target_hex(self) -> str:
        return to_hex(self.target_rgb)

    @property
    def source_hex(self) -> str:
        return to_hex(self.source_rgb)

    @property
    def displayed_hex(self) -> str:
        return to_hex(self.displayed_rgb)

    @property
    def max_channel_error(self) -> float:
        return float(np.max(np.abs(self.displayed_rgb - self.target_rgb)))


def composite(foreground: RGBLike, background: RGBLike, alpha: float) -> np.ndarray:
    """Composite an sRGB foreground over an opaque sRGB background.

    The operation is performed on encoded sRGB channels, matching the simple
    alpha behavior expected by common plotting/rendering pipelines.
    """
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must lie in [0, 1].")
    fg = to_rgb(foreground)
    bg = to_rgb(background)
    return alpha * fg + (1 - alpha) * bg


def compensate_alpha(
    target: RGBLike,
    *,
    alpha: float,
    background: RGBLike = "#FFFFFF",
) -> AlphaCompensation:
    r"""Find a transparent source color that reproduces an apparent target.

    Solves, channel by channel,

    .. math::

       T = \alpha S + (1-\alpha) B

    for ``S``.  If the exact inverse is outside the sRGB gamut, ``S`` is
    clipped to the nearest feasible channel values.  ``feasible`` reports
    whether exact reconstruction was possible.
    """
    if not 0 < alpha <= 1:
        raise ValueError("alpha must satisfy 0 < alpha <= 1.")
    target_rgb = to_rgb(target)
    background_rgb = to_rgb(background)

    raw = (target_rgb - (1 - alpha) * background_rgb) / alpha
    feasible = bool(np.all((raw >= 0) & (raw <= 1)))
    source_rgb = np.clip(raw, 0, 1)
    displayed_rgb = composite(source_rgb, background_rgb, alpha)
    return AlphaCompensation(
        target_rgb=target_rgb,
        source_rgb=source_rgb,
        displayed_rgb=displayed_rgb,
        background_rgb=background_rgb,
        alpha=float(alpha),
        feasible=feasible,
    )
