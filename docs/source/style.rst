Heri publication style
======================

The Heri preset follows the publication figures in
Bayesian-Uncertainty-in-WTI-APOs rather than the earlier transparent
Proximity Graphs style.

Basic usage
-----------

.. code-block:: python

   import matplotlib.pyplot as plt
   import contrastcolors as cc

   cc.set_style("heri", font="Arial")

   fig, ax = plt.subplots()
   ax.plot(x, y)
   ax.set_xlabel(r"$x$")
   ax.set_ylabel(r"$f(x)$")

   cc.save_figure(fig, "figure.pdf")

The preset uses:

- compact 8--9 pt publication typography;
- white axes and figure background;
- a light gray grid below the data;
- hidden top and right spines;
- 1.6 pt default lines and 4.5 pt markers;
- 600 dpi saved raster layers;
- embedded PDF/PS font type 42;
- the Paul Tol high-contrast categorical palette;
- the WTI iridescent continuous map as HERI_CMAP.

Selecting the font
------------------

The visual style and font family are independent.

.. code-block:: python

   cc.set_style("heri", font="Arial")
   cc.set_style("heri", font="Helvetica")
   cc.set_style("heri", font="STIX")
   cc.set_style("heri", font="DejaVu Sans")

Any non-empty Matplotlib font-family name is accepted. Matplotlib handles its
normal fallback behavior when that font is not installed.

The default is:

.. code-block:: python

   cc.set_style("heri", font="utopia")

With use_tex="auto", the Utopia font uses the Wiley-like external LaTeX stack
only when the required packages are available. Arbitrary fonts such as Arial
stay in native Matplotlib text mode so the requested family can actually be
respected.

.. code-block:: python

   cc.set_style("heri", font="utopia", use_tex=True)
   cc.set_style("heri", font="Arial", use_tex=False)

Hybrid PDF rasterization
------------------------

The WTI-style preset keeps normal plot lines vector. Only data-heavy artists
are rasterized automatically:

- scatter
- hexbin
- contourf
- pcolormesh
- imshow
- fill_between
- 3D plot_surface
- 3D plot_trisurf

Axes, ordinary lines, errorbars, text, ticks, titles, legends and annotations
remain vector.

Rasterization can be disabled globally:

.. code-block:: python

   cc.set_style("heri", font="Arial", rasterize=False)

Temporary style
---------------

.. code-block:: python

   with cc.style_context("heri", font="Arial"):
       fig, ax = plt.subplots()
       ax.scatter(x, y)

Saving
------

save_figure appends .pdf when no suffix is supplied and uses the WTI publication
defaults: tight crop, 0.035 inch padding, white background and 600 dpi raster
layers.

.. code-block:: python

   cc.save_figure(fig, "figures/result")
   cc.save_figure(fig, "figures/result.pdf", dpi=900)

Panel labels and colormap
-------------------------

.. code-block:: python

   cc.panel_label(ax, "A")
   image = ax.imshow(values, cmap=cc.HERI_CMAP)

The categorical cycle is available as cc.HERI_PALETTE.
