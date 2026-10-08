# Reproducible LaTeX publication example

The demonstration generates a complete 10 pt two-column article. Its
plots use measured physical widths from main.tex.

Outputs:

- lines.pgf: manuscript-owned LaTeX font glyphs in the final PDF.
- lines.pdf: direct PDF at exactly the same physical size, with an external legend
  and print-safe luminance spacing for the three lines.
- groups.pdf and groups.pgf: scatter groups separated by marker, color and
  luminance, with larger points, **white point outlines** and an external
  legend. The manuscript uses the PGF file for exact TeX font matching.
- dense.pdf: rasterized point cloud with vector labels.
- accessibility.pdf / accessibility.pgf: **true-vector** full-page
  two-column by three-row accessibility views, with TeX-native fonts in PGF.
- groups_accessibility.pdf / groups_accessibility.pgf: **true-vector**
  horizontal three-column by two-row scatter views with translucent points
  and 0.22 pt white outlines.
- accessibility.png / groups_accessibility.png: PNG previews for the website
  only; the LaTeX manuscript uses PGF, not screenshot images.
- lines_proof.pdf: independent TeX verification of the PDF's real width.
- report.json: TeX font, exact dimensions and per-figure warnings.
- main.pdf: final article containing all comparisons.

## Run on macOS

~~~bash
git pull
./examples/latex_publication/run_macos.sh --open
~~~

If necessary:

~~~bash
chmod +x examples/latex_publication/run_macos.sh
~~~

Requires MacTeX or compatible TeX Live (pdflatex, pgf, lmodern,
microtype, graphicx, kpsewhich), and Conda or Python 3.10+.
If TeX has its fonts, no separate macOS font installation is required.

Intermediate outputs are ignored by Git. The final PDF and accessibility
PNG are also copied to docs/source/_static so Sphinx can display them.

After reviewing the PDF:

~~~bash
./examples/latex_publication/run_macos.sh --push
~~~

This explicitly commits and pushes only those two published assets.
The default build does not push or commit anything.

**Important:** the CVD images are approximate simulations; they do not
certify universal accessibility. PGF obtains the document's font glyphs
only when typeset by the original LaTeX document.

## Consistent axis typography and dashboard layouts

The example deliberately tests two formats in the **same two-column** LaTeX
document. A portrait 2 × 3 line-series accessibility panel is placed in a
dedicated float page using `figure* [p]`, with explanatory text. A landscape
3 × 2 scatter accessibility panel spans both text columns using
`figure* [t]`, leaving room for normal article paragraphs.

All original figures use a shared axis-label helper: **normal weight and
exactly the manuscript's nominal body point size**, with ticks scaled to
80% of the text size, following Figure 1. The scatter uses 0.22 pt white marker
outlines, 0.68 opacity and an orange/blue/bluish-green categorical palette
instead of black point borders. Figure 3 uses the TeX-native PGF export
so the font glyphs come from the manuscript, not from Matplotlib.

The preview panels use regular-weight headings centered above each image.
The pie-chart illustration was removed from this publication demonstration.

## Fully vector dashboards

The new `cc.show_vector_accessibility_panel` redraws Line2D and scatter
PathCollection data six times with color transformations *before drawing*.
There is no rasterized snapshot inside these PDFs or PGFs. Each chart panel
sets axis labels to the 10 pt body size of the actual manuscript, tick labels
to 8 pt, and panel headers to 10 pt; the PDF/PGF is included in LaTeX at its
original physical `\\textwidth` without scaling.

The simulated grayscale and CVD colors are approximate. Highly translucent
overlapping points can look different from a pixel-by-pixel simulation;
the goal is a scalable, editorially readable diagnostic. Heatmaps and more
complex artist types still use the original raster-preview helper.
