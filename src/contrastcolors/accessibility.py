"""Figure-level print and colour-vision accessibility previews.

CVD simulation uses Colorspacious' Machado et al. (2009) model.
These previews are approximations, not clinical tests or accessibility
certifications.
"""
from __future__ import annotations

from collections.abc import Sequence
from math import ceil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from colorspacious import cspace_convert
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image

DEFAULT_ACCESSIBILITY_MODES = (
    "original", "grayscale", "print",
    "deuteranopia", "protanopia", "tritanopia",
)
_CVD_TYPES = {
    "deuteranopia": "deuteranomaly",
    "protanopia": "protanomaly",
    "tritanopia": "tritanomaly",
}


def _as_rgba(image: np.ndarray) -> np.ndarray:
    image = np.asarray(image)
    if image.ndim != 3 or image.shape[-1] not in (3, 4):
        raise ValueError("Expected RGB or RGBA image of shape (height, width, 3/4).")
    if image.dtype == np.uint8:
        rgba = image.copy()
    else:
        data = np.asarray(image, dtype=np.float64)
        if not np.all(np.isfinite(data)) or np.any(data < 0) or np.any(data > 1):
            raise ValueError("Floating-point images must contain values in [0, 1].")
        rgba = np.rint(data * 255).astype(np.uint8)
    if rgba.shape[-1] == 3:
        alpha = np.full((*rgba.shape[:2], 1), 255, dtype=np.uint8)
        rgba = np.concatenate([rgba, alpha], axis=-1)
    return rgba


def _linearize(rgb: np.ndarray) -> np.ndarray:
    return np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)


def _encode(rgb: np.ndarray) -> np.ndarray:
    rgb = np.clip(rgb, 0.0, 1.0)
    return np.where(rgb <= 0.0031308, 12.92 * rgb, 1.055 * rgb ** (1 / 2.4) - 0.055)


def _pack(rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    return np.concatenate(
        [np.rint(np.clip(rgb, 0, 1) * 255).astype(np.uint8), alpha], axis=-1
    )


def figure_to_rgba(fig: plt.Figure, *, max_width: int | None = 900) -> np.ndarray:
    """Render a figure with its labels/legends into RGBA uint8 pixels.

    A width limit keeps notebook outputs manageable. The source figure is not
    recolored or closed.
    """
    if max_width is not None and max_width < 1:
        raise ValueError("max_width must be positive or None")
    original_canvas = fig.canvas
    if hasattr(original_canvas, "buffer_rgba"):
        original_canvas.draw()
        rgba = np.asarray(original_canvas.buffer_rgba()).copy()
    else:
        canvas = FigureCanvasAgg(fig)
        try:
            canvas.draw()
            rgba = np.asarray(canvas.buffer_rgba()).copy()
        finally:
            fig.set_canvas(original_canvas)
    if max_width and rgba.shape[1] > max_width:
        height = max(1, round(rgba.shape[0] * max_width / rgba.shape[1]))
        rgba = np.asarray(Image.fromarray(rgba).resize(
            (max_width, height), resample=Image.Resampling.BILINEAR
        ))
    return rgba


def to_grayscale_image(image: np.ndarray) -> np.ndarray:
    """Grayscale preserving linear-sRGB relative luminance."""
    rgba = _as_rgba(image)
    linear = _linearize(rgba[..., :3].astype(np.float64) / 255)
    y = np.sum(linear * [0.2126, 0.7152, 0.0722], axis=-1, keepdims=True)
    return _pack(_encode(np.repeat(y, 3, axis=-1)), rgba[..., 3:4])


def to_print_stress_image(image: np.ndarray, *, levels: int = 9) -> np.ndarray:
    """Simulate reduced grayscale contrast and tone levels, not an ICC profile."""
    if levels < 2:
        raise ValueError("levels must be at least 2")
    rgba = to_grayscale_image(image)
    gray = rgba[..., :1].astype(np.float64) / 255
    compressed = np.clip(0.5 + 0.68 * (gray - 0.5), 0, 1)
    rounded = np.rint(compressed * (levels - 1)) / (levels - 1)
    return _pack(np.repeat(rounded, 3, axis=-1), rgba[..., 3:4])


def simulate_cvd_image(image: np.ndarray, mode: str, *, severity: float = 100) -> np.ndarray:
    """Approximate complete or partial colour-vision deficiency with Machado matrices."""
    if mode not in _CVD_TYPES:
        raise ValueError(f"Unknown CVD mode {mode!r}")
    if not np.isfinite(severity) or not 0 <= severity <= 100:
        raise ValueError("severity must be in [0, 100]")
    rgba = _as_rgba(image)
    rgb = rgba[..., :3].astype(np.float64) / 255
    space = {
        "name": "sRGB1+CVD",
        "cvd_type": _CVD_TYPES[mode],
        "severity": float(severity),
    }
    result = cspace_convert(rgb, space, "sRGB1")
    return _pack(np.clip(result, 0, 1), rgba[..., 3:4])


def _mode(image: np.ndarray, mode: str, severity: float) -> np.ndarray:
    if mode == "original":
        return image.copy()
    if mode == "grayscale":
        return to_grayscale_image(image)
    if mode == "print":
        return to_print_stress_image(image)
    if mode in _CVD_TYPES:
        return simulate_cvd_image(image, mode, severity=severity)
    raise ValueError(f"Unknown preview mode {mode!r}")


def simulate_figure(fig: plt.Figure, mode: str, *, severity: float = 100,
                    max_width: int | None = 900) -> np.ndarray:
    """Render a figure under one requested accessibility mode."""
    return _mode(figure_to_rgba(fig, max_width=max_width), mode, severity)


def figure_variants(
    fig: plt.Figure,
    modes: Sequence[str] = DEFAULT_ACCESSIBILITY_MODES,
    *,
    severity: float = 100,
    max_width: int | None = 900,
) -> dict[str, np.ndarray]:
    """Render the source once and return RGBA variants by name."""
    if not modes:
        raise ValueError("At least one mode is required")
    source = figure_to_rgba(fig, max_width=max_width)
    return {mode: _mode(source, mode, severity) for mode in modes}


def show_accessibility_panel(
    fig: plt.Figure,
    modes: Sequence[str] = DEFAULT_ACCESSIBILITY_MODES,
    *,
    ncols: int = 3,
    figsize: tuple[float, float] | None = None,
    titles: bool = True,
    severity: float = 100,
    max_width: int | None = 900,
) -> tuple[plt.Figure, np.ndarray]:
    """Make a panel with original, grayscale, print and three CVD views.

    Titles are placed in a dedicated row above each image, rather than as
    ordinary Matplotlib subplot titles over a rasterized plot. The original
    figure remains intact. Returns only the image axes in a flat array.
    """
    if not modes or ncols < 1:
        raise ValueError("Supply modes and ncols >= 1")
    views = figure_variants(fig, modes, severity=severity, max_width=max_width)
    cols = min(ncols, len(modes))
    rows = ceil(len(modes) / cols)
    # A separate header axis for every preview prevents title overlap with
    # source figures' legends, axis labels, annotations, and adjacent rows.
    panel = plt.figure(figsize=figsize or (4.3 * cols, 3.55 * rows))
    grid = panel.add_gridspec(
        rows * 2, cols,
        height_ratios=[0.12, 1.0] * rows,
        left=0.018, right=0.982, bottom=0.025, top=0.982,
        hspace=0.09, wspace=0.055,
    )
    image_axes = []
    for index, mode in enumerate(modes):
        row, col = divmod(index, cols)
        header = panel.add_subplot(grid[2 * row, col])
        header.axis("off")
        if titles:
            label = {
                "print": "Print stress",
                "grayscale": "Grayscale",
            }.get(mode, mode.capitalize())
            header.text(
                0.5, 0.5, label, ha="center", va="center",
                fontsize=12.0, fontweight="semibold",
                transform=header.transAxes,
            )
        ax = panel.add_subplot(grid[2 * row + 1, col])
        ax.imshow(views[mode], interpolation="antialiased")
        ax.set_axis_off()
        image_axes.append(ax)
    # No tight_layout(): it can draw labels from one image into the header
    # of another, particularly when the original plot has a top legend.
    return panel, np.asarray(image_axes, dtype=object)


def save_accessibility_panel(fig: plt.Figure, filename: str | Path, *,
                             dpi: int = 180, **kwargs) -> Path:
    """Save a preview panel, closing only that panel, never the original figure."""
    target = Path(filename)
    target.parent.mkdir(parents=True, exist_ok=True)
    panel, _ = show_accessibility_panel(fig, **kwargs)
    try:
        panel.savefig(target, dpi=dpi, bbox_inches="tight")
    finally:
        plt.close(panel)
    return target
