Customization
=============

The style, the colors, and the series identifiers are separate pieces. You can
change one without rebuilding the others.

Choose the plotting style
-------------------------

The available presets are ``heri``, ``elegante``, and ``default``.
The new ``elegante`` preset uses tick-aligned plot boundaries and
keeps decorative markers inside the axes without changing spline data.

.. code-block:: python

   cc.set_style("elegante", font="Arial")
   ax.plot(x, y, marker="o")
   cc.apply_elegant_axes(ax, target_xticks=6, marker_inset_pt=4)

For a visual comparison of all three styles, see :doc:`style`.

Change the number of colors
---------------------------

The number of hues is the number of generated colors.

.. code-block:: python

   colors = cc.color_palette(
       hues=[35, 95, 155, 215, 275, 330],
       ratio=1.18,
       start_luminance=0.72,
   )

Adding one more hue adds one more color. The important constraint is that the
requested number of luminance levels must fit inside the available WCAG
luminance range for the chosen contrast ratio.

The hue angle controls the color family:

.. code-block:: text

   0° / 360°   red
   30°         orange
   60°         yellow
   120°        green
   180°        cyan / teal
   240°        blue
   300°        violet / magenta

The exact appearance also depends on luminance, chroma and the sRGB gamut.

See different palette sizes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   import contrastcolors as cc

   fig, axes = plt.subplots(3, 1, figsize=(8.2, 2.8))

   configs = [
       ([35, 155, 260], 1.25, 0.72, "3 colors"),
       ([55, 20, 145, 210, 290], 1.18, 0.72, "5 colors"),
       ([20, 70, 120, 170, 220, 275, 330], 1.10, 0.72, "7 colors"),
   ]

   for ax, (hues, ratio, start, title) in zip(axes, configs):
       colors = cc.color_palette(
           hues=hues,
           ratio=ratio,
           start_luminance=start,
       )
       for i, color in enumerate(colors):
           ax.barh(0, 1, left=i, color=color, height=1)
       ax.set_xlim(0, len(colors))
       ax.set_ylim(-0.5, 0.5)
       ax.set_title(title, loc="left", fontsize=10)
       ax.axis("off")

   fig.tight_layout()

Change hue order
----------------

Hue order and luminance order are independent. Reordering ``hues`` changes
which hue receives each luminance level.

.. code-block:: python

   palette_a = cc.contrast_palette(
       hues=[55, 20, 145, 210, 290],
       ratio=1.4,
   )

   palette_b = cc.contrast_palette(
       hues=[210, 145, 55, 290, 20],
       ratio=1.4,
   )

Both use the same contrast ladder. The Studio is the easiest place to try the
order visually.

Markers and line styles
-----------------------

Use ``plot_scheme`` when color should not be the only identifier.

.. code-block:: python

   scheme = cc.plot_scheme(
       hues=[55, 20, 145, 210, 290],
       ratio=1.3,
       markers=["o", "s", "^", "D", "X"],
       linestyles=["-", "--", ":", "-.", (0, (5, 2))],
   )

   for y, kwargs in zip(series, scheme):
       ax.plot(x, y, **kwargs)

This is particularly useful for grayscale printing and for figures with many
overlapping lines.

Choose the font
---------------

The Heri visual style and font family are independent.

.. code-block:: python

   cc.set_style("heri", font="Arial")
   cc.set_style("heri", font="Helvetica")
   cc.set_style("heri", font="STIX")
   cc.set_style("heri", font="DejaVu Sans")
   cc.set_style("heri", font="utopia")

``Arial`` and other custom families use native Matplotlib text when
``use_tex="auto"``. Matplotlib applies its normal fallback behavior if a font
is not installed.

Change transparency and background
----------------------------------

.. code-block:: python

   colors = cc.color_palette(
       hues=[20, 145, 210],
       ratio=1.3,
       alpha=0.65,
       background="#FFFFFF",
       preserve_apparent=True,
   )

Alpha compensation is background-specific. A source color prepared for white
is not generally compensated for a dark background.

Use the Heri categorical colors directly
-----------------------------------------

The built-in categorical cycle is available as:

.. code-block:: python

   cc.HERI_PALETTE

You can use individual entries directly:

.. code-block:: python

   ax.plot(x, y, color=cc.HERI_PALETTE[1])
   ax.scatter(x2, y2, color=cc.HERI_PALETTE[2])

Or generate an entirely new palette with ``color_palette``. The Heri style does
not require the Heri categorical colors.

Change the continuous colormap
------------------------------

Use the supplied publication colormap:

.. code-block:: python

   ax.imshow(values, cmap=cc.HERI_CMAP)

Or use any normal Matplotlib colormap:

.. code-block:: python

   ax.imshow(values, cmap="viridis")

Rasterization and export
------------------------

Dense artists are rasterized by default in the Heri style while ordinary lines
and typography remain vector.

.. code-block:: python

   cc.set_style("heri", font="Arial", rasterize=True)
   cc.save_figure(fig, "figure.pdf", dpi=600)

Turn automatic dense-artist rasterization off with:

.. code-block:: python

   cc.set_style("heri", font="Arial", rasterize=False)

Interactive customization
-------------------------

Use the :doc:`studio` to adjust the same parameters visually and copy the
corresponding Python.
