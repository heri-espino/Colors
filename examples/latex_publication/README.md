# Reproducible LaTeX publication example

The demonstration generates a complete 10 pt two-column article. Its
plots use measured physical widths from main.tex.

Outputs:

- lines.pgf: manuscript-owned LaTeX font glyphs in the final PDF.
- lines.pdf: direct PDF at exactly the same physical size, with an external legend
  and print-safe luminance spacing for the three lines.
- groups.pdf: scatter groups separated by marker, color and luminance,
  with larger points and a legend above the axes.
- dense.pdf: rasterized point cloud with vector labels.
- accessibility.png: two-column six-view comparison of the line plot,
  with panel headings separated from each image.
- groups_accessibility.png: the scatter plot under the same six conditions.
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

## Paper dashboard layouts and pie separators

The example deliberately tests two formats in the **same two-column** LaTeX
document. A portrait 2 × 3 line-series accessibility panel is placed in a
dedicated float page using `figure* [p]`, with explanatory text. A landscape
3 × 2 scatter accessibility panel spans both text columns using
`figure* [t]`, leaving room for normal article paragraphs.

Both panels use regular-weight headings centered above their respective
rendered images, close enough not to waste vertical space. A separate
`pie.pdf` figure demonstrates `cc.pie_plot()`: its wedge boundaries are
white, not black, by default.
