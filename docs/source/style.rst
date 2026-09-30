Heri publication style
======================

The package includes the publication style used across Heriberto Espino
Montelongo's figure-generation repositories.

Global usage
------------

.. code-block:: python

   import matplotlib.pyplot as plt
   import contrastcolors as cc

   cc.set_style("heri")

   fig, ax = plt.subplots()
   ax.plot(x, y)
   ax.set_xlabel(r"$x$")
   ax.set_ylabel(r"$f(x)$")

   cc.save_figure(fig, "figure.pdf")

The preset keeps the top and right spines hidden, uses serif mathematical
typography, transparent figure/axes backgrounds, embedded TrueType-compatible
PDF fonts, and publication-scale font sizes.

Hybrid PDF rasterization
------------------------

With the default rasterize=True, data-heavy Matplotlib artists are rasterized
automatically:

- plot
- scatter
- contourf
- pcolormesh
- imshow
- fill_between
- 3D plot_surface
- 3D plot_trisurf

Axes, spines, tick labels, titles, legends, and annotations remain vector.
This gives compact PDFs without turning the whole figure into an image.

A plotting call can opt out:

.. code-block:: python

   ax.plot(x, y, rasterized=False)

or rasterization can be disabled globally while keeping the rest of the style:

.. code-block:: python

   cc.set_style("heri", rasterize=False)

LaTeX
-----

use_tex="auto" is the default. External LaTeX is enabled only if the required
LaTeX stack is available; otherwise the preset falls back to STIX /
Latin-Modern-like Matplotlib typography.

.. code-block:: python

   cc.set_style("heri", use_tex=True)   # force LaTeX
   cc.set_style("heri", use_tex=False)  # never use external LaTeX

Temporary style
---------------

.. code-block:: python

   with cc.style_context("heri"):
       fig, ax = plt.subplots()
       ax.scatter(x, y)

After the block, the previous Matplotlib rcParams and rasterization state are
restored.

Saving
------

save_figure appends .pdf when no suffix is supplied and defaults to a
transparent, tightly cropped publication figure.

.. code-block:: python

   cc.save_figure(fig, "figures/result")
   cc.save_figure(fig, "figures/result.pdf", dpi=600)
