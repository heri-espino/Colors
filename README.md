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

## Windows: run the entire project with Conda

Install [Miniforge](https://github.com/conda-forge/miniforge) or Miniconda,
clone the repository, and open an initialized Conda PowerShell:

~~~powershell
git clone https://github.com/heri-espino/Colors.git
cd Colors
Set-ExecutionPolicy -Scope Process Bypass
.\tools\setup_and_run.ps1
~~~

The script creates or updates a Python 3.12 Conda environment, installs all
dependencies and the editable package, checks dependencies, runs pytest,
executes **every demo notebook**, saves generated plots inside the .ipynb
files, verifies the outputs, and builds the Sphinx website (strict warnings).

Optional flags:

~~~powershell
# Run tests and rebuild Sphinx without re-executing notebooks
.\tools\setup_and_run.ps1 -SkipNotebooks

# Run tests and serve the documentation at http://localhost:8765/
.\tools\setup_and_run.ps1 -SkipNotebooks -Serve

# Explicitly commit saved notebook results
.\tools\setup_and_run.ps1 -CommitOutputs

# Explicitly commit and push results to GitHub
.\tools\setup_and_run.ps1 -CommitOutputs -Push
~~~

Without those flags, **no changes are pushed or committed automatically**.
The generated documentation is in
`docs/_build/html/index.html`, and the notebook outputs are saved in
`docs/source/notebooks/*.ipynb`.

Launch JupyterLab with `conda run -n contrastcolors jupyter lab`.

To publish the Sphinx site, go to GitHub **Settings > Pages**, select
**GitHub Actions** as the source, and run the manual `pages` workflow.
A default Jekyll Pages deployment does not build Sphinx.

## Install locally

```bash
python -m pip install -e .
```

For development:

```bash
python -m pip install -e ".[dev,docs]"
pytest
```

## LaTeX publication figures: automatic document size

Match the real physical widths and nominal body font size of a trusted
LaTeX document. No PNG screenshots or pixel-based trial and error are needed.

~~~python
import contrastcolors as cc

with cc.latex_style("paper/main.tex", width="column") as pub:
    fig, ax = pub.subplots(height_ratio=0.65)
    ax.plot([0, 1, 2], [1, 3, 2])
    ax.set(xlabel="Time", ylabel="Response")
    print(pub.audit(fig).warnings)
    pub.savefig(fig, "paper/figures/result.pdf")

cc.verify_latex_placement(
    "paper/main.tex", "paper/figures/result.pdf",
    proof_pdf="paper/figures/result_proof.pdf",
)
~~~

Include the saved PDF **without resizing** in LaTeX (plain includegraphics).
Set width="text" to span both columns. To resize an existing figure, call
cc.fit_figure_to_latex(fig, cc.inspect_latex("paper/main.tex")).

A suitable TeX engine must be on PATH for inspection or proof compilation.
If unavailable, pass LatexLayout.from_dimensions(columnwidth_pt=...,
textwidth_pt=..., fontsize_pt=...) instead.

Font sizes and widths are matched in physical units; identical font *glyphs*
require a configured TeX font or PGF export. The bounded fit and audit
cannot automatically resolve every legend or annotation overlap. The TeX
probe uses a temporary document and does not modify your paper's source,
but it still executes trusted LaTeX preamble macros with shell escape disabled.

To reuse the exact TeX fonts without downloading them again, inspect the
available font information and export a PGF for the manuscript itself to typeset:

~~~python
font = cc.find_latex_font("paper/main.tex")
print(font.tex_font_name, font.metrics_path, font.outline_path)
with cc.latex_style("paper/main.tex") as pub:
    fig, ax = pub.subplots()
    ax.plot([0, 1], [1, 2])
    pub.savefig(fig, "paper/figures/figure.pgf")
~~~

Include the PGF in the manuscript with the LaTeX command
`\\input{figures/figure.pgf}`. A TFM is font metrics, not an outline
font: no need to manually install it into Matplotlib.

See [publication guide](docs/source/publication.rst).

## Figure accessibility

The Heri Matplotlib style now defaults to different line markers and
linestyles, and repeated scatter groups get distinct markers. Use the
six-view panel to inspect an entire figure in grayscale, print stress,
deuteranopia, protanopia and tritanopia, alongside the original:

    cc.show_accessibility_panel(fig)
    cc.save_accessibility_panel(fig, "accessible.png")

See the accessibility documentation. Simulations are approximations.

## Interactive Palette & Plot Studio

The browser-based Studio works without a backend and offers live previews for
line plots, time series, histograms, box/violin/ridge plots, scatter,
categorical heatmaps and grouped bars.

It includes grayscale/print-stress views, hue order and identifier editing,
browser-local save/load, portable JSON import/export, and downloadable named
Python palette presets.

Open the Studio in the Sphinx site or directly at
[docs/source/_static/studio.html](docs/source/_static/studio.html).

**Named palette example:**

~~~python
import contrastcolors as cc

cc.register_palette(
    "paper_palette",
    hues=[55, 20, 145, 210, 290],
    ratio=1.22,
    start_luminance=0.72,
    markers=["o", "s", "^", "D", "X"],
    linestyles=["-", "--", ":", "-.", (0, (5, 2))],
)

colors = cc.color_palette("paper_palette")
scheme = cc.plot_scheme("paper_palette")
~~~

A Python preset registration lasts for the current process. Keep the
registration in a project module and import it to reuse it.

## Documentation

The Sphinx site now documents the complete library:

- library tour and function/object inventory;
- quickstart and installation;
- palette and ContrastGrid workflows;
- alpha compositing and apparent-color compensation;
- Heri publication style, selectable fonts, hybrid PDF export, and colormaps;
- WCAG, sRGB, OKLab/OKLCH, and gamut behavior;
- guarantees and limitations;
- end-to-end Matplotlib examples;
- interactive palette picker;
- complete public API and advanced low-level helpers.

Build it locally with:

~~~bash
python -m pip install -e ".[docs]"
sphinx-build -W -b html docs/source docs/_build/html
~~~

Open docs/_build/html/index.html in a browser.

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

~~~python
import matplotlib.pyplot as plt
import contrastcolors as cc

cc.set_style("heri", font="Arial")

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$f(x)$")

cc.save_figure(fig, "figure.pdf")
~~~

The Heri preset matches that repository's publication figures: compact
white-grid axes, 8--9 pt typography, top/right spines removed, 600-dpi hybrid
PDF export, Paul Tol categorical colors, and the iridescent continuous map
available as cc.HERI_CMAP.

The visual style and the font are independent:

~~~python
cc.set_style("heri")                   # Utopia when available, STIX fallback
cc.set_style("heri", font="Arial")
cc.set_style("heri", font="Helvetica")
cc.set_style("heri", font="STIX")
cc.set_style("heri", font="DejaVu Sans")
~~~

For arbitrary fonts, use_tex="auto" renders text directly through Matplotlib so
the requested family is respected. The Utopia preset can use the Wiley-like
LaTeX stack when it is installed:

~~~python
cc.set_style("heri", font="utopia", use_tex=True)
~~~

By default, ordinary lines and typography remain vector, while dense artists
such as scatter plots, heatmaps, filled contours, hexbins and 3D surfaces are
rasterized inside the PDF. This can be disabled:

~~~python
cc.set_style("heri", font="Arial", rasterize=False)
~~~

For local use without changing global settings permanently:

~~~python
with cc.style_context("heri", font="Arial"):
    ...
~~~

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
- `color_palette`, `contrast_palette`, `plot_scheme`, `show_palette`, and
  `ContrastGrid` APIs;
- `set_style("heri")`, `style_context`, and hybrid-PDF `save_figure` helpers;
- interactive Sphinx palette picker;
- interactive Palette & Plot Studio for hue order, markers, linestyles, grayscale/print preview, alpha, style, and code export;
- tests and Sphinx builds in GitHub Actions.

## Planned

- optional APCA contrast model;
- color-vision-deficiency simulation/diagnostics;
- richer Matplotlib integration and named reusable palettes;
- package publishing after the API stabilizes.
