"""High-level Seaborn-like public helpers."""

from __future__ import annotations

from collections.abc import Sequence

from .palette import Palette, color_for_luminance
from .color_spaces import relative_luminance
from .contrast import luminance_ladder


def contrast_palette(
    hues: Sequence[float],
    *,
    ratio: float = 1.5,
    start_luminance: float = 0.95,
    chroma: float = 0.13,
) -> Palette:
    """Build one contrast-controlled color per supplied hue.

    Hue hues[k] is assigned to luminance level Y_k. Therefore a list
    of five hues directly produces a five-color palette whose adjacent WCAG
    contrast ratios are ratio.

    Parameters
    ----------
    hues:
        Hue angles in OKLCH degrees. The number of hues determines the number
        of colors.
    ratio:
        Desired WCAG contrast ratio between adjacent colors.
    start_luminance:
        Relative luminance of the first (lightest) color.
    chroma:
        Requested OKLCH chroma. Chroma is reduced automatically when necessary
        to remain inside sRGB.
    """
    if len(hues) == 0:
        raise ValueError("At least one hue is required.")
    ys = luminance_ladder(
        len(hues),
        ratio,
        start_luminance=start_luminance,
    )
    return Palette(
        color_for_luminance(y, hue, chroma=chroma)
        for y, hue in zip(ys, hues, strict=True)
    )


def color_palette(
    hues: Sequence[float],
    *,
    ratio: float = 1.5,
    start_luminance: float = 0.95,
    chroma: float = 0.13,
    alpha: float = 1.0,
    background: str | Sequence[float] = "white",
    preserve_apparent: bool = True,
    alpha_strategy: str = "perceptual",
    as_hex: bool = False,
):
    """Return plotting-ready colors from a contrast-controlled palette.

    This is the convenience function intended for ordinary Matplotlib usage,
    analogous to a palette constructor in a plotting library.

    By default it returns Matplotlib-ready RGBA tuples. Set as_hex=True for
    opaque hexadecimal target colors; in that mode alpha-related arguments are
    not applied.
    """
    p = contrast_palette(
        hues,
        ratio=ratio,
        start_luminance=start_luminance,
        chroma=chroma,
    )
    if as_hex:
        return p.hex
    return p.mpl_colors(
        alpha=alpha,
        background=background,
        preserve_apparent=preserve_apparent,
        alpha_strategy=alpha_strategy,
    )


def show_palette(
    hues: Sequence[float],
    *,
    ratio: float = 1.5,
    start_luminance: float = 0.95,
    chroma: float = 0.13,
    alpha: float = 1.0,
    background: str | Sequence[float] = "white",
    preserve_apparent: bool = True,
    alpha_strategy: str = "perceptual",
    ax=None,
):
    """Draw a compact Matplotlib swatch preview and return its axes."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    p = contrast_palette(
        hues,
        ratio=ratio,
        start_luminance=start_luminance,
        chroma=chroma,
    )
    rendered = p.render(
        alpha=alpha,
        background=background,
        preserve_apparent=preserve_apparent,
        alpha_strategy=alpha_strategy,
    )
    if ax is None:
        _, ax = plt.subplots(figsize=(max(4.0, len(p) * 1.25), 1.7))

    for i, item in enumerate(rendered):
        r, g, b, a = item.rgba
        ax.add_patch(Rectangle((i, 0), 1, 1, facecolor=(r, g, b, a), edgecolor="none"))
        displayed_y = relative_luminance(item.compensation.displayed_rgb)
        text_color = "black" if displayed_y > 0.55 else "white"
        ax.text(
            i + 0.5,
            0.5,
            item.target.hex,
            ha="center",
            va="center",
            color=text_color,
            fontsize=9,
            family="monospace",
        )

    ax.set_xlim(0, len(p))
    ax.set_ylim(0, 1)
    ax.set_aspect("auto")
    ax.axis("off")
    return ax
