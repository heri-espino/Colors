"""Contrast-controlled color palettes for scientific Python."""

from .alpha import AlphaCompensation, compensate_alpha, composite, minimum_alpha
from .api import color_palette, palette, show_palette
from .color_spaces import contrast_ratio, relative_luminance, to_hex, to_rgb
from .contrast import luminance_contrast, luminance_ladder
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
    "ColorCell",
    "ContrastGrid",
    "Palette",
    "RenderedColor",
    "color_for_luminance",
    "color_palette",
    "compensate_alpha",
    "composite",
    "contrast_grid",
    "contrast_ratio",
    "luminance_contrast",
    "luminance_ladder",
    "minimum_alpha",
    "palette",
    "relative_luminance",
    "show_palette",
    "to_hex",
    "to_rgb",
]

__version__ = "0.1.0"
