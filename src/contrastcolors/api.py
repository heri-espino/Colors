"""High-level Seaborn-like public helpers."""

from __future__ import annotations

from collections.abc import Sequence

from .palette import Palette, color_for_luminance
from .color_spaces import relative_luminance
from .contrast import luminance_ladder
from .presets import get_palette


def contrast_palette(
    hues: Sequence[float] | str,
    *,
    ratio: float | None = None,
    start_luminance: float | None = None,
    chroma: float | None = None,
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
    if isinstance(hues, str):
        preset = get_palette(hues)
        hues = preset.hues
        ratio = preset.ratio if ratio is None else ratio
        start_luminance = preset.start_luminance if start_luminance is None else start_luminance
        chroma = preset.chroma if chroma is None else chroma
    ratio = 1.5 if ratio is None else ratio
    start_luminance = 0.95 if start_luminance is None else start_luminance
    chroma = 0.13 if chroma is None else chroma
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
    hues: Sequence[float] | str,
    *,
    ratio: float | None = None,
    start_luminance: float | None = None,
    chroma: float | None = None,
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
    hues: Sequence[float] | str,
    *,
    ratio: float | None = None,
    start_luminance: float | None = None,
    chroma: float | None = None,
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


DEFAULT_MARKERS = ("o", "s", "^", "D", "X", "P", "v", "<", ">", "*")
DEFAULT_LINESTYLES = ("-", "--", ":", "-.", (0, (5, 2)), (0, (3, 1, 1, 1)))


def plot_scheme(
    hues: Sequence[float] | str,
    *,
    ratio: float | None = None,
    start_luminance: float | None = None,
    chroma: float | None = None,
    alpha: float = 1.0,
    background: str | Sequence[float] = "white",
    preserve_apparent: bool = True,
    alpha_strategy: str = "perceptual",
    markers: Sequence[str] | None = None,
    linestyles: Sequence[object] | None = None,
) -> list[dict]:
    """Return Matplotlib style dictionaries for redundant series encoding.

    Each returned dictionary contains color, marker, and linestyle. Colors are
    generated by the contrast-controlled palette system, while marker and line
    styles cycle independently. This makes one plotting scheme usable in color
    and easier to identify in grayscale or monochrome output.

    Parameters
    ----------
    hues:
        Hue angle for each desired series.
    markers:
        Optional marker sequence. Defaults to a set of distinct Matplotlib
        markers and cycles if shorter than the hue list.
    linestyles:
        Optional line-style sequence. Defaults to a mix of solid, dashed,
        dotted, dash-dot, and custom dash patterns and cycles if shorter than
        the hue list.
    """
    preset = get_palette(hues) if isinstance(hues, str) else None
    colors = color_palette(
        hues,
        ratio=ratio,
        start_luminance=start_luminance,
        chroma=chroma,
        alpha=alpha,
        background=background,
        preserve_apparent=preserve_apparent,
        alpha_strategy=alpha_strategy,
    )
    if markers is None and preset is not None:
        markers = preset.markers
    if linestyles is None and preset is not None:
        linestyles = preset.linestyles
    marker_values = tuple(DEFAULT_MARKERS if markers is None else markers)
    line_values = tuple(DEFAULT_LINESTYLES if linestyles is None else linestyles)
    if not marker_values:
        raise ValueError("markers must contain at least one marker.")
    if not line_values:
        raise ValueError("linestyles must contain at least one style.")

    return [
        {
            "color": color,
            "marker": marker_values[i % len(marker_values)],
            "linestyle": line_values[i % len(line_values)],
        }
        for i, color in enumerate(colors)
    ]


def scatter_scheme(hues: Sequence[float] | str, **kwargs) -> list[dict]:
    """Return distinct colors and group markers to pass into Axes.scatter.

    Line styles are omitted since Matplotlib scatter does not accept them.
    Registered palettes and plot_scheme parameters are fully supported.
    """
    return [
        {"color": item["color"], "marker": item["marker"]}
        for item in plot_scheme(hues, **kwargs)
    ]
