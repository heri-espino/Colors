Real LaTeX publication demonstration
======================================

This is a reproducible, two-column **technical presentation** of the
library, with mathematical explanations of palette construction,
hue/luminance control, accessibility, alpha compositing, exact LaTeX
fonts, physical dimensions and vector/hybrid export. It uses the
manuscript's measured column dimensions and Latin Modern font from
MacTeX or TeX Live.

The example source is at
https://github.com/heri-espino/Colors/tree/main/examples/latex_publication

Figures included
----------------

- **Palette construction:** a vector ContrastGrid illustrating three
  relative-luminance levels crossed with four OKLCH hue angles.
- **Palette Studio:** the manuscript links to the
  `interactive Studio <https://heri-espino.github.io/Colors/studio.html>`_
  and describes its equidistant, golden-angle, analogous, single-hue,
  balanced-family and manual strategies, plus alpha/contrast choices.
- **PGF vs PDF:** the same line graph appears twice, comparing
  manuscript-owned font glyphs with direct Matplotlib vector export.
  The categorical scatter is also included as PGF for matching fonts.
- **Grouped scatter:** translucent markers with very thin **white boundaries**,
  three Okabe–Ito colorblind-friendly hues (orange/blue/bluish green), and
  the same nominal LaTeX axis font size. The categories retain different
  shapes even when their colors become similar.
- Redundant hue, relative luminance, marker shapes and an external legend
  help keep the three groups legible; PGF ensures document-owned typography.
- **Dense scatter:** rasterized points with vector axes and labels.
- **Full-page vector series dashboard:** six views in a portrait 2 × 3 grid,
  displayed on a dedicated LaTeX float page with an explanatory paragraph.
- **Horizontal vector scatter dashboard:** six views in a landscape 3 × 2 grid,
  spanning both text columns with surrounding article prose.
- **Compact labels:** regular-weight titles are visually centered over the
  actual rendered image and placed close to it without covering plot text.
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
generates figures, compiles the full article, and copies the manuscript,
three vector figure PDFs and three website PNG previews to the static
documentation directory.

Locally generated files are under:

.. code-block:: text

   examples/latex_publication/generated/main.pdf
   examples/latex_publication/generated/lines.pgf
   examples/latex_publication/generated/lines.pdf
   examples/latex_publication/generated/groups.pdf
   examples/latex_publication/generated/groups.pgf
   examples/latex_publication/generated/dense.pdf
   examples/latex_publication/generated/palette_grid.pdf
   examples/latex_publication/generated/palette_grid.pgf
   examples/latex_publication/generated/palette_grid.png
   examples/latex_publication/generated/accessibility.pdf
   examples/latex_publication/generated/accessibility.pgf
   examples/latex_publication/generated/accessibility.png
   examples/latex_publication/generated/groups_accessibility.pdf
   examples/latex_publication/generated/groups_accessibility.pgf
   examples/latex_publication/generated/lines_proof.pdf
   examples/latex_publication/generated/report.json

Publish results to the website
------------------------------

After reviewing the local PDF, run:

.. code-block:: bash

   ./examples/latex_publication/run_macos.sh --push

The --push flag explicitly commits and pushes the final article PDF,
the two vector dashboard PDFs, the palette-grid PDF and the corresponding
website PNG thumbnails, not the intermediate source PGF files.

.. raw:: html

   <p>
     <a href="_static/publication_demo.pdf" target="_blank" rel="noopener">
       Open the generated LaTeX demonstration PDF
     </a>
   </p>
   <p>
     <a href="_static/publication_palette_grid.pdf" target="_blank" rel="noopener">
       Download the vector OKLCH hue / WCAG luminance grid (PDF)
     </a>
   </p>
   <p>
     <a href="_static/publication_accessibility.pdf" target="_blank" rel="noopener">
       Download full-size vector series dashboard (PDF)
     </a>
   </p>
   <p>
     <a href="_static/publication_scatter_accessibility.pdf" target="_blank" rel="noopener">
       Download full-size vector scatter dashboard (PDF)
     </a>
   </p>
   <p>
     <a href="_static/publication_accessibility.png" target="_blank" rel="noopener">
       Open the accessibility comparison image
     </a>
   </p>
   <figure>
     <img
       src="_static/publication_palette_grid.png"
       alt="Hue-luminance grid with equal-luminance rows and varying hue columns"
       style="max-width:100%;height:auto"
       loading="lazy">
     <figcaption>Three controlled relative luminance rows and four OKLCH
       hue columns: the rule for selecting colours is visible.</figcaption>
   </figure>
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
universal accessibility certification. For the supported standard line and
scatter artists the published dashboards are true vector drawings, and
the compiled manuscript inserts their PGF sources for document-owned text
typesetting. The PNG files here are only web previews.

The publication example explicitly fixes the three Okabe--Ito colours
``#E69F00``, ``#0072B2`` and ``#009E73``; these are not generated by
``print_safe_luminances`` and are not asserted to form an exact WCAG
contrast ladder. Independently, ``plot_scheme()`` and ``scatter_scheme()``
can use adaptive ``print_safe_luminances`` defaults when no luminance
constraint is specified. The source legends sit above the data axes.
Dashboard labels are centered on their own rendered images, with a small
title gap instead of a separate, oversized heading row.

The six-view **series panel** uses two internal columns and three rows and
occupies a dedicated float page; the **scatter panel** uses three internal
columns and two rows, taking the full width of a two-column journal page.
The accompanying article text explains why the aspect ratios differ.

The preview includes grayscale rendering to check whether luminance alone
is sufficient; marker shapes and dashed line patterns remain necessary,
especially where color pairs converge under simulated CVD.

All original charts follow the Figure 1 typography convention: axis labels
are normal weight and match the document body in nominal point size.
Figure 3 also uses PGF when included in the article, guaranteeing that its
text is typeset with the same LaTeX font setup as Figure 1.
The pie-chart example is not part of this publication demo.

Feature catalogue and sources
-----------------------------

Read the full :doc:`features` inventory for every public Python export and
for the separate Studio, notebook, build and deployment capabilities.
The `live Palette Studio <https://heri-espino.github.io/Colors/studio.html>`_
lets readers create a palette without coding, compare luminance and hue
arrangements, inspect simulated colour-vision deficiencies and export a
Python preset.

The technical manuscript explains that the WCAG ratio constrains adjacent
**opaque** sRGB luminances, whereas the fixed three-colour Okabe--Ito
demonstration is an accessibility-oriented starting point, not an exact
WCAG ladder. It also distinguishes independent PDF vector export, native
document-owned PGF text, and intentional selective rasterization of dense
data. A PDF may contain both vector and pixel-based material.
