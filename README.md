# Colors

`contrastcolors` is a small Python library for building color palettes whose
**adjacent WCAG contrast ratios are controlled by construction**, while hue can
change independently. It is designed for scientific plotting and depends on
Matplotlib in the same spirit that higher-level plotting libraries build on it.

The core object is an `i × j` hue–luminance grid:

\[
C_{k\ell}=C(Y_k,h_\ell),
\]

where every color in row `k` has the same relative luminance `Y_k`, every
column corresponds to a chosen hue `h_ell`, and adjacent rows satisfy

\[
\frac{Y_k+0.05}{Y_{k+1}+0.05}=r.
\]

Therefore **any selection of one hue per row preserves the same adjacent
contrast ratio**.

## Install locally

```bash
python -m pip install -e .
```

For development:

```bash
python -m pip install -e ".[dev,docs]"
pytest
```

## Quick start

```python
import contrastcolors as cc

# 5 luminance levels × 5 hue choices = 25 candidate colors.
grid = cc.contrast_grid(
    levels=5,
    hues=[55, 20, 145, 210, 290],
    ratio=1.4,
    start_luminance=0.95,
)

# Choose one hue from each row. Hue may change at every level.
palette = grid.select([0, 1, 2, 3, 4])

print(palette.hex)
print(palette.adjacent_contrast)
```

### Matplotlib

```python
colors = palette.mpl_colors(
    alpha=0.75,
    background="white",
    preserve_apparent=True,
)
```

With `preserve_apparent=True`, the library solves

\[
T=\alpha S+(1-\alpha)B
\]

for the source color `S`, so the composited color approaches the original
target `T` on background `B`. When the exact inverse falls outside sRGB, the
source is clipped and the result explicitly reports that exact reconstruction
was not feasible.

## Design goals

- constant adjacent WCAG contrast ratios;
- hue chosen independently at each luminance level;
- OKLCH-based hue/chroma construction with automatic sRGB gamut reduction;
- alpha compensation against a known background;
- Matplotlib-ready RGBA output and `ListedColormap` export;
- a Sphinx documentation site, with an interactive palette picker planned as a
  separate web layer inspired by tools such as Harmonizer.

## Status

Early MVP. The mathematical core, Matplotlib adapter, tests, and Sphinx docs are
being built first. APCA, perceptual gamut optimization for infeasible alpha
compensation, color-vision simulation, and the interactive web picker belong to
later milestones.
