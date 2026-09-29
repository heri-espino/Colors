Quickstart
==========

Ordinary plotting
-----------------

For the common case, provide one hue per desired color:

.. code-block:: python

   import contrastcolors as cc

   colors = cc.color_palette(
       hues=[55, 20, 145, 210, 290],
       ratio=1.4,
   )

The first hue receives the lightest luminance level, the second hue receives
the next level, and so on. Adjacent colors therefore keep the requested WCAG
contrast ratio even though every hue may be different.

Use the result anywhere Matplotlib accepts a color:

.. code-block:: python

   import matplotlib.pyplot as plt

   for y, color in zip(series, colors):
       plt.plot(x, y, color=color)

To retain metadata and diagnostics, use :func:`contrastcolors.contrast_palette`:

.. code-block:: python

   palette = cc.contrast_palette(
       hues=[55, 20, 145, 210, 290],
       ratio=1.4,
   )

   print(palette.hex)
   print(palette.adjacent_contrast)
   print(palette.minimum_alpha(background="white"))

Exploring combinations
----------------------

Use a :class:`contrastcolors.ContrastGrid` when you want several candidate
hues at every luminance level:

.. code-block:: python

   grid = cc.contrast_grid(
       levels=5,
       hues=[55, 20, 145, 210, 290],
       ratio=1.4,
       start_luminance=0.95,
   )

   palette = grid.select([0, 1, 2, 3, 4])

The hue index may be chosen independently for each luminance level without
changing the prescribed adjacent contrast ratio.
