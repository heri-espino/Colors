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
- **Grouped scatter:** distinct markers and colors for each category.
- **Dense scatter:** rasterized points with vector axes and labels.
- **Six views:** original, grayscale, print-stress, deuteranopia,
  protanopia and tritanopia.
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

These links become live after the Mac script has generated and committed
its outputs. The source and instructions are already in the repository.

Limitations
-----------

PGF typesets text using the actual manuscript font after it is included
in LaTeX. A direct PDF can have equal nominal font size without identical
glyphs. The six-view panel provides diagnostic simulations rather than
universal accessibility certification.
