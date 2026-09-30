"""Matplotlib style presets for publication-quality figures.

The Heri preset is distilled from the shared paper_figure_style.py modules used
across Heriberto Espino Montelongo's research repositories: transparent paper
figures, serif/LaTeX typography, minimal spines, and hybrid PDF output where
data-heavy artists are rasterized while axes and text remain vector.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import shutil
import subprocess
from typing import Iterator, Literal

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


StyleName = Literal["heri", "default", "matplotlib"]

HERI_LATEX_PREAMBLE = (
    r"\usepackage[T1]{fontenc}"
    r"\usepackage{lmodern}"
    r"\usepackage{stix}"
)

HERI_PALETTE = (
    "#1565C0",
    "#FF9800",
    "#009688",
    "#F44336",
    "#448AFF",
    "#8BC34A",
    "#AD1457",
    "#FFC107",
)

HERI_SAVEFIG_KWARGS = {
    "facecolor": "none",
    "edgecolor": "none",
    "transparent": True,
    "bbox_inches": "tight",
    "pad_inches": 0.02,
}

_RASTER_PATCHED = False
_RASTERIZE_DATA = False


def available_styles() -> tuple[str, ...]:
    """Return the style names understood by set_style."""
    return ("heri", "default")


def _latex_stack_available() -> bool:
    """Return whether the LaTeX packages required by the Heri preset exist."""
    if shutil.which("latex") is None:
        return False

    kpsewhich = shutil.which("kpsewhich")
    if kpsewhich is None:
        return False

    for package in ("lmodern.sty", "stix.sty"):
        try:
            result = subprocess.run(
                [kpsewhich, package],
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )
        except (OSError, subprocess.SubprocessError):
            return False
        if result.returncode != 0 or not result.stdout.strip():
            return False

    return True


def _set_rasterized(artist):
    if hasattr(artist, "set_rasterized"):
        artist.set_rasterized(True)
    for child in getattr(artist, "collections", []):
        if hasattr(child, "set_rasterized"):
            child.set_rasterized(True)
    return artist


def _install_rasterized_defaults() -> None:
    """Install conditional rasterization wrappers once per Python process."""
    global _RASTER_PATCHED
    if _RASTER_PATCHED or getattr(Axes, "_contrastcolors_rasterized_defaults", False):
        _RASTER_PATCHED = True
        return

    _RASTER_PATCHED = True
    Axes._contrastcolors_rasterized_defaults = True

    original_plot = Axes.plot
    original_scatter = Axes.scatter
    original_contourf = Axes.contourf
    original_pcolormesh = Axes.pcolormesh
    original_imshow = Axes.imshow
    original_fill_between = Axes.fill_between

    def plot(self, *args, **kwargs):
        if _RASTERIZE_DATA:
            kwargs.setdefault("rasterized", True)
        return original_plot(self, *args, **kwargs)

    def scatter(self, *args, **kwargs):
        if _RASTERIZE_DATA:
            kwargs.setdefault("rasterized", True)
        return original_scatter(self, *args, **kwargs)

    def contourf(self, *args, **kwargs):
        artist = original_contourf(self, *args, **kwargs)
        return _set_rasterized(artist) if _RASTERIZE_DATA else artist

    def pcolormesh(self, *args, **kwargs):
        if _RASTERIZE_DATA:
            kwargs.setdefault("rasterized", True)
        return original_pcolormesh(self, *args, **kwargs)

    def imshow(self, *args, **kwargs):
        if _RASTERIZE_DATA:
            kwargs.setdefault("rasterized", True)
        return original_imshow(self, *args, **kwargs)

    def fill_between(self, *args, **kwargs):
        artist = original_fill_between(self, *args, **kwargs)
        return _set_rasterized(artist) if _RASTERIZE_DATA else artist

    Axes.plot = plot
    Axes.scatter = scatter
    Axes.contourf = contourf
    Axes.pcolormesh = pcolormesh
    Axes.imshow = imshow
    Axes.fill_between = fill_between

    try:
        from mpl_toolkits.mplot3d.axes3d import Axes3D
    except Exception:
        return

    if getattr(Axes3D, "_contrastcolors_rasterized_defaults", False):
        return

    Axes3D._contrastcolors_rasterized_defaults = True
    original_plot_surface = Axes3D.plot_surface
    original_plot_trisurf = Axes3D.plot_trisurf

    def plot_surface(self, *args, **kwargs):
        if _RASTERIZE_DATA:
            kwargs.setdefault("rasterized", True)
        return original_plot_surface(self, *args, **kwargs)

    def plot_trisurf(self, *args, **kwargs):
        if _RASTERIZE_DATA:
            kwargs.setdefault("rasterized", True)
        return original_plot_trisurf(self, *args, **kwargs)

    Axes3D.plot_surface = plot_surface
    Axes3D.plot_trisurf = plot_trisurf


def _heri_rcparams(*, use_tex: bool) -> dict:
    params = {
        "font.family": "serif",
        "font.size": 16,
        "axes.titlesize": 21,
        "axes.labelsize": 16,
        "legend.fontsize": 13,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.75,
        "axes.facecolor": "none",
        "figure.facecolor": "none",
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.facecolor": "none",
        "savefig.edgecolor": "none",
        "savefig.transparent": True,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "lines.linewidth": 1.5,
        "axes.prop_cycle": mpl.cycler(color=HERI_PALETTE),
        "text.usetex": use_tex,
    }

    if use_tex:
        params["text.latex.preamble"] = HERI_LATEX_PREAMBLE
    else:
        params.update(
            {
                "font.serif": [
                    "Latin Modern Roman",
                    "STIX Two Text",
                    "STIXGeneral",
                    "DejaVu Serif",
                ],
                "mathtext.fontset": "stix",
            }
        )

    return params


def set_style(
    style: StyleName | str = "heri",
    *,
    use_tex: bool | Literal["auto"] = "auto",
    rasterize: bool = True,
) -> None:
    """Apply a named global Matplotlib style.

    style="heri" applies the publication preset. "default" and "matplotlib"
    restore Matplotlib defaults.

    use_tex="auto" enables external LaTeX only when the required stack exists.
    When rasterize=True, data-heavy artists created after this call are
    rasterized by default while axes, text, ticks, titles, and legends stay
    vector. Individual plotting calls can override rasterized=False.
    """
    global _RASTERIZE_DATA

    name = str(style).strip().lower()
    if name in {"default", "matplotlib"}:
        _RASTERIZE_DATA = False
        mpl.rcdefaults()
        return

    if name != "heri":
        choices = ", ".join(repr(x) for x in available_styles())
        raise ValueError(f"Unknown style {style!r}. Available styles: {choices}.")

    _install_rasterized_defaults()
    _RASTERIZE_DATA = bool(rasterize)

    if use_tex == "auto":
        resolved_use_tex = _latex_stack_available()
    elif isinstance(use_tex, bool):
        resolved_use_tex = use_tex
    else:
        raise ValueError("use_tex must be True, False, or 'auto'.")

    mpl.rcParams.update(_heri_rcparams(use_tex=resolved_use_tex))


@contextmanager
def style_context(
    style: StyleName | str = "heri",
    *,
    use_tex: bool | Literal["auto"] = "auto",
    rasterize: bool = True,
) -> Iterator[None]:
    """Temporarily apply a style and restore previous rcParams afterwards."""
    global _RASTERIZE_DATA

    previous = mpl.rcParams.copy()
    previous_rasterize = _RASTERIZE_DATA
    try:
        set_style(style, use_tex=use_tex, rasterize=rasterize)
        yield
    finally:
        _RASTERIZE_DATA = previous_rasterize
        mpl.rcParams.update(previous)


def save_figure(
    fig,
    path: str | Path,
    *,
    dpi: int | None = None,
    close: bool = False,
    **kwargs,
) -> Path:
    """Save a publication figure, defaulting to a hybrid transparent PDF.

    If path has no suffix, .pdf is appended. Under the Heri style, rasterized
    artists are embedded as raster layers at the requested DPI while axes,
    text, labels, ticks, and other vector artists remain vector.
    """
    target = Path(path)
    if not target.suffix:
        target = target.with_suffix(".pdf")
    target.parent.mkdir(parents=True, exist_ok=True)

    save_kwargs = dict(HERI_SAVEFIG_KWARGS)
    save_kwargs.update(kwargs)
    if dpi is not None:
        save_kwargs["dpi"] = dpi

    fig.savefig(target, **save_kwargs)
    if close:
        plt.close(fig)
    return target
