# Colors

`contrastcolors` builds scientific plotting palettes whose **adjacent WCAG
contrast ratios are controlled by construction** while hue can change
independently. It is designed as a small layer on top of Matplotlib, in the
same general role that palette helpers play in higher-level plotting libraries.

For relative luminance levels (Y_k) and a requested adjacent contrast ratio
(r),

[
rac{Y_k+0.05}{Y_{k+1}+0.05}=r,
qquad
Y_k=rac{Y_0+0.05}{r^k}-0.05.
]

The library then solves for an sRGB-representable OKLCH color at each requested
luminance and hue.

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

For the ordinary case, supply one hue per desired color:

```python
import contrastcolors as cc

colors = cc.color_palette(
    hues=[55, 20, 145, 210, 290],
    ratio=1.4,
)

# Matplotlib-ready RGBA tuples
for y, color in zip(series, colors):
    plt.plot(x, y, color=color)
```

Use `contrast_palette` when you want diagnostics and metadata:

```python
palette = cc.contrast_palette(
    hues=[55, 20, 145, 210, 290],
    ratio=1.4,
)

print(palette.hex)
print(palette.adjacent_contrast)
print(palette.minimum_alpha(background="white"))
```

## Publication style

The package includes the publication style used by the WTI APO paper:

```python
import matplotlib.pyplot as plt
import contrastcolors as cc

cc.set_style("heri", font="Arial")

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$f(x)$")

cc.save_figure(fig, "figure.pdf")
```

The Heri preset matches that repository's publication figures: compact
white-grid axes, 8--9 pt typography, top/right spines removed, 600-dpi hybrid
PDF export, Paul Tol categorical colors, and the iridescent continuous map
available as `cc.HERI_CMAP`.

The visual style and the font are independent:

```python
cc.set_style("heri")                   # Utopia when available, STIX fallback
cc.set_style("heri", font="Arial")
cc.set_style("heri", font="Helvetica")
cc.set_style("heri", font="STIX")
cc.set_style("heri", font="DejaVu Sans")
```

For arbitrary fonts, `use_tex="auto"` renders text directly through
Matplotlib so the requested family is respected. The Utopia preset can use the
Wiley-like LaTeX stack when it is installed:

```python
cc.set_style("heri", font="utopia", use_tex=True)
```

By default, ordinary lines and typography remain vector, while dense artists
such as scatter plots, heatmaps, filled contours, hexbins and 3D surfaces are
rasterized inside the PDF. This can be disabled:

```python
cc.set_style("heri", font="Arial", rasterize=False)
```

For local use without changing global settings permanently:

```python
with cc.style_context("heri", font="Arial"):
    ...
```

## Exploring hue combinations

The lower-level object is an (i 	imes j) hue-luminance grid:

[
C_{kell}=C(Y_k,h_ell).
]

Every color in row (k) has the same relative luminance (Y_k), while each
column corresponds to a candidate hue. Therefore any selection of one hue per
row preserves the prescribed adjacent contrast ratio.

```python
grid = cc.contrast_grid(
    levels=5,
    hues=[55, 20, 145, 210, 290],
    ratio=1.4,
)

palette = grid.select([0, 1, 2, 3, 4])
grid.plot()
```

The Sphinx documentation includes an interactive picker inspired by the
workflow of tools such as Evil Martians Harmonizer. The picker lets you change
levels, contrast ratio, hues, chroma, alpha and background, click one candidate
per row, and copy the resulting `contrastcolors` Python call.

## Alpha compensation

With `preserve_apparent=True`, the library solves

[
T=alpha S+(1-alpha)B
]

for the source color (S), where (T) is the desired apparent color and (B)
is the background:

[
S=rac{T-(1-alpha)B}{alpha}.
]

If the inverse lies outside the sRGB gamut, exact reconstruction is physically
impossible at that alpha/background combination. The result reports
`feasible=False` rather than claiming the original color was preserved.

## Current features

- constant adjacent WCAG contrast ratios;
- independently selectable hue at every luminance level;
- OKLCH hue/chroma construction with automatic sRGB gamut reduction;
- alpha compensation against a known background;
- perceptual OKLab optimization when exact alpha compensation is outside sRGB;
- minimum-alpha feasibility calculation;
- Matplotlib-ready RGBA output and `ListedColormap` export;
- `color_palette`, `contrast_palette`, `show_palette`, and
  `ContrastGrid` APIs;
- `set_style("heri")`, `style_context`, and hybrid-PDF `save_figure` helpers;
- interactive Sphinx palette picker;
- tests and Sphinx builds in GitHub Actions.

## Planned

- optional APCA contrast model;
- color-vision-deficiency simulation/diagnostics;
- richer Matplotlib integration and named reusable palettes;
- package publishing after the API stabilizes.
