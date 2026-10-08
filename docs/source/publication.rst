LaTeX publication fit
=====================

Prepare a Matplotlib figure at its **real insertion size** instead of
guessing fonts from pixels or rescaling it repeatedly.

The workflow has four steps: measure the LaTeX template, create the figure
at the final physical width, audit it, and optionally compile an insertion
proof. Use only trusted LaTeX sources; the probe compiles the preamble with
shell escape disabled.

Measure the actual manuscript
-----------------------------

Install a LaTeX engine (TeX Live, MiKTeX or MacTeX), then run:

.. code-block:: python

   import contrastcolors as cc

   layout = cc.inspect_latex("paper/main.tex", engine="pdflatex")
   print(layout.columnwidth_pt)
   print(layout.textwidth_pt)
   print(layout.fontsize_pt)
   print(layout.font_family)

The probe uses a temporary source containing the manuscript preamble and
a very short document body. It measures the sizes *after* class/package
initialization, without editing the original manuscript.

If TeX is unavailable but your journal specifies the dimensions:

.. code-block:: python

   layout = cc.LatexLayout.from_dimensions(
       columnwidth_pt=245.0,
       textwidth_pt=510.0,
       fontsize_pt=10.0,
   )

Those are illustrative values, **not universal journal dimensions**.

Create at column or text width
------------------------------

.. code-block:: python

   import numpy as np
   import contrastcolors as cc

   with cc.latex_style("paper/main.tex", width="column") as pub:
       fig, ax = pub.subplots(height_ratio=0.65)
       x = np.linspace(0, 10, 160)
       ax.plot(x, np.sin(x))
       ax.set_xlabel("Time")
       ax.set_ylabel("Response")
       report = pub.audit(fig)
       print(report.passed, report.warnings)
       pub.savefig(fig, "paper/figures/signal.pdf")

The generated PDF has the same width as your column. Axis labels use
the nominal body font size; ticks and legends default to 80% of that size.
For a figure across both columns use width="text" instead.

.. code-block:: latex

   \begin{figure}
     \centering
     \includegraphics{figures/signal.pdf}
     \caption{Example figure.}
   \end{figure}

**Do not resize this PDF again in includegraphics** unless you intend a
different effective font size. The output uses bbox_inches=None; automatically
tight-cropping a PDF would change its physical insertion dimensions.

Adjust an existing Matplotlib figure
------------------------------------

.. code-block:: python

   layout = cc.inspect_latex("paper/main.tex")
   result = cc.fit_figure_to_latex(fig, layout, width="column")
   print(result.passed, result.audit.warnings)
   cc.save_figure(fig, "fitted.pdf", bbox_inches=None, pad_inches=0)

The fitter adjusts width and text hierarchy, runs tight_layout where
applicable, and may increase figure height if clipping persists. It has a
bounded number of iterations: unresolved problems are reported rather than
silently hidden. It cannot infer the scientific importance of an overlap.

Compile a proof PDF
-------------------

.. code-block:: python

   cc.verify_latex_placement(
       "paper/main.tex",
       "paper/figures/signal.pdf",
       proof_pdf="paper/figures/signal_proof.pdf",
   )

This compiles a **separate minimal document** with your template preamble
and an *unscaled* copy of the PDF, comparing the physical PDF width against
the measured column width (default tolerance: 0.75 TeX points). The proof
also shows normal document text for a typography comparison. For a wide
two-column figure use width="text".
It does not validate the final position of a float inside the manuscript.

Matching the actual font glyphs
-------------------------------

Matching 10 pt in both LaTeX and Matplotlib does not necessarily mean both
use the *same* Times/Utopia/Computer Modern outlines. The automatic font
choice is a serif/sans-serif approximation. For true document-owned TeX fonts
and math typesetting, export a PGF file:

.. code-block:: python

   with cc.latex_style("paper/main.tex", width="column") as pub:
       fig, ax = pub.subplots()
       ax.plot([0, 1, 2], [2, 3, 1])
       pub.savefig(fig, "paper/figures/curve.pgf")

.. code-block:: latex

   \begin{figure}
     \centering
     \input{figures/curve.pgf}
     \caption{Figure text typeset by LaTeX.}
   \end{figure}

A working TeX installation is required for PGF and some nonstandard math/font
settings may need additional configuration.

What the audit checks
---------------------

- Width mismatch against the actual TeX column or text width.
- Smallest rendered point size at that insertion scale.
- Smallest line thickness at that insertion scale.
- Matplotlib text that extends beyond the figure canvas.

It does *not* certify colorblind accessibility, scientific clarity,
legend overlap quality, or journal compliance. Use
:doc:`accessibility` for grayscale and CVD diagnostics.

See :doc:`api` for inspect_latex, LatexLayout, latex_style,
PublicationStyle, fit_figure_to_latex, FigureAudit and verify_latex_placement.
