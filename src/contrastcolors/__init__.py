"""Contrast-controlled color palettes for scientific Python."""

from .alpha import AlphaCompensation, compensate_alpha, composite, minimum_alpha
from .api import (
    DEFAULT_LINESTYLES,
    DEFAULT_MARKERS,
    color_palette,
    contrast_palette,
    plot_scheme,
    show_palette,
)
from .color_spaces import contrast_ratio, delta_e_ok, relative_luminance, srgb_to_oklab, to_hex, to_rgb
from .contrast import luminance_contrast, luminance_ladder
from .style import (
    HERI_CMAP,
    HERI_IRIDESCENT_HEX,
    HERI_NEUTRAL,
    HERI_PALETTE,
    available_styles,
    panel_label,
    save_figure,
    set_style,
    style_context,
)
from .palette import (
    ColorCell,
    ContrastGrid,
    Palette,
    RenderedColor,
    color_for_luminance,
    contrast_grid,
)

__all__ = [
    "AlphaCompensation",
    "HERI_CMAP",
    "HERI_IRIDESCENT_HEX",
    "HERI_NEUTRAL",
    "HERI_PALETTE",
    "ColorCell",
    "DEFAULT_LINESTYLES",
    "DEFAULT_MARKERS",
    "ContrastGrid",
    "Palette",
    "RenderedColor",
    "color_for_luminance",
    "color_palette",
    "compensate_alpha",
    "composite",
    "contrast_grid",
    "contrast_ratio",
    "delta_e_ok",
    "luminance_contrast",
    "luminance_ladder",
    "minimum_alpha",
    "contrast_palette",
    "relative_luminance",
    "srgb_to_oklab",
    "show_palette",
    "available_styles",
    "panel_label",
    "plot_scheme",
    "save_figure",
    "set_style",
    "style_context",
    "to_hex",
    "to_rgb",
]

__version__ = "0.1.0"
