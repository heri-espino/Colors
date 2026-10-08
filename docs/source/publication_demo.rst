Real LaTeX publication demonstration
======================================

This is a reproducible, two-column LaTeX paper for testing publication-ready
figures on macOS. It uses the manuscript's real column dimensions and its
Latin Modern font, supplied through MacTeX/TeX Live.

The example source is at
https://github.com/heri-espino/Colors/tree/main/examples/latex_publication

Figures included
----------------

- **PGF vs PDF:** the same line graph appears twice, comparing
  manuscript-owned font glyphs with direct Matplotlib vector export.
- **Grouped scatter:** larger markers, distinct colors and luminances for
  each category, with the legend above the data region.
- **Dense scatter:** rasterized points with vector axes and labels.
- **Six views:** original, grayscale, print-stress, deuteranopia,
  protanopia and tritanopia. Panel headings are outside each preview,
  and the images use a two-column layout for legibility in the paper.
- **Grayscale contrast:** when three categorical series are plotted,
  the default scheme spreads their relative luminances more strongly;
  points use bigger, outlined markers and legends stay outside data.
- **LaTeX width proof:** compares an unscaled PDF width with the true column.
- **JSON audit:** measures fonts, physical dimensions and output sizes.

Run on your Mac
---------------

From the repository root:

.. code-block:: bash

   git pull
   ./examples/latex_publication/run_macos.sh --open

If necessary, first make the script executable:

.. code-block:: bash

   chmod +x examples/latex_publication/run_macos.sh

The script installs the editable Python library, runs publication tests,
generates figures, compiles the full article, and copies the final PDF and
accessibility image to the static documentation directory.

Locally generated files are under:

.. code-block:: text

   examples/latex_publication/generated/main.pdf
   examples/latex_publication/generated/lines.pgf
   examples/latex_publication/generated/lines.pdf
   examples/latex_publication/generated/groups.pdf
   examples/latex_publication/generated/dense.pdf
   examples/latex_publication/generated/accessibility.png
   examples/latex_publication/generated/lines_proof.pdf
   examples/latex_publication/generated/report.json

Publish results to the website
------------------------------

After reviewing the local PDF, run:

.. code-block:: bash

   ./examples/latex_publication/run_macos.sh --push

The --push flag explicitly commits and pushes only the final publication
PDF and accessibility PNG, not all intermediate figures.

.. raw:: html

   <p>
     <a href="_static/publication_demo.pdf" target="_blank" rel="noopener">
       Open the generated LaTeX demonstration PDF
     </a>
   </p>
   <p>
     <a href="_static/publication_accessibility.png" target="_blank" rel="noopener">
       Open the accessibility comparison image
     </a>
   </p>
   <figure>
     <img
       src="_static/publication_accessibility.png"
       alt="Six-view figure: original, grayscale, print stress,
       deuteranopia, protanopia and tritanopia"
       style="max-width:100%;height:auto"
       loading="lazy">
     <figcaption>The comparison is generated from the same original line plot
       as the manuscript's PDF and PGF figure.</figcaption>
   </figure>
   <figure>
     <img
       src="_static/publication_scatter_accessibility.png"
       alt="Six simulations of the same grouped scatter plot showing different
       category markers in grayscale and color-vision deficiencies"
       style="max-width:100%;height:auto"
       loading="lazy">
     <figcaption>The categorical scatter comparison preserves
       group-identifying markers independently of color.</figcaption>
   </figure>

These links become live after the Mac script has generated and committed
its outputs. The source and instructions are already in the repository.

Limitations
-----------

PGF typesets text using the actual manuscript font after it is included
in LaTeX. A direct PDF can have equal nominal font size without identical
glyphs. The six-view panel provides diagnostic simulations rather than
universal accessibility certification.

The publication example uses the adaptive ``print_safe_luminances`` defaults
for three series. Relative luminances are more widely spaced than for a
five- or ten-series palette. The original plot places its legend above the
data axes, and each accessibility panel has a separate title strip to prevent
titles colliding with axis labels. Panels are arranged in **two columns by
three rows**, so the final ``figure*`` can be read at journal scale.

The preview includes grayscale rendering to check whether luminance alone
is sufficient; marker shapes and dashed line patterns remain necessary,
especially where color pairs converge under simulated CVD.
