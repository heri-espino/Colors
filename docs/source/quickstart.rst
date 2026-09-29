Quickstart
==========

Create a 5 x 5 candidate grid:

.. code-block:: python

   import contrastcolors as cc

   grid = cc.contrast_grid(
       levels=5,
       hues=[55, 20, 145, 210, 290],
       ratio=1.4,
       start_luminance=0.95,
   )

   palette = grid.select([0, 1, 2, 3, 4])
   print(palette.hex)
   print(palette.adjacent_contrast)

The hue index may be chosen independently for each luminance level without
changing the prescribed contrast ratio.
