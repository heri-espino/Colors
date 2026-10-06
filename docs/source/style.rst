Styles
======

``contrastcolors`` currently exposes two style states through
``set_style``: the publication preset ``heri`` and Matplotlib
``default``.

Heri
----

``heri`` follows the visual system used in the WTI APO publication figures.

.. raw:: html

   <div class="cc-style-summary">
     <div><strong>Background</strong>white + light gray grid</div>
     <div><strong>Typography</strong>compact 8--9 pt paper scale</div>
     <div><strong>Lines</strong>1.6 pt, top/right spines hidden</div>
     <div><strong>Export</strong>600 dpi hybrid PDF defaults</div>
   </div>

.. plot::
   :include-source:

   import numpy as np
   import matplotlib.pyplot as plt
   import contrastcolors as cc

   cc.set_style("heri", font="DejaVu Sans")

   x = np.linspace(0, 9, 260)
   fig, ax = plt.subplots(figsize=(8.0, 4.1))

   for i, color in enumerate(cc.HERI_PALETTE[:4]):
       ax.plot(
           x,
           np.sin(x * 0.72 + i * 0.55) + i * 0.34,
           color=color,
           label=f"Series {i + 1}",
       )

   ax.set(
       title="Heri publication style",
       xlabel="Time",
       ylabel="Response",
   )
   ax.legend(ncol=2)
   fig.tight_layout()

Use it with:

.. code-block:: python

   cc.set_style("heri", font="Arial")

Choose another font without changing the rest of the style:

.. code-block:: python

   cc.set_style("heri", font="Helvetica")
   cc.set_style("heri", font="STIX")
   cc.set_style("heri", font="DejaVu Sans")
   cc.set_style("heri", font="utopia")

The categorical cycle is ``cc.HERI_PALETTE`` and the continuous heatmap
colormap is ``cc.HERI_CMAP``.

Default
-------

``default`` restores Matplotlib rcParams and disables the automatic dense
rasterization switch installed by the Heri preset.

.. plot::
   :include-source:

   import numpy as np
   import matplotlib.pyplot as plt
   import contrastcolors as cc

   cc.set_style("default")

   x = np.linspace(0, 9, 260)
   fig, ax = plt.subplots(figsize=(8.0, 4.1))

   for i in range(4):
       ax.plot(
           x,
           np.sin(x * 0.72 + i * 0.55) + i * 0.34,
           label=f"Series {i + 1}",
       )

   ax.set(
       title="Matplotlib default",
       xlabel="Time",
       ylabel="Response",
   )
   ax.legend(ncol=2)
   fig.tight_layout()

Restore it with:

.. code-block:: python

   cc.set_style("default")

Heri with a custom palette
--------------------------

The plotting style does not force you to use the built-in Heri categorical
colors. Generate a palette and pass its colors to the artists.

.. plot::
   :include-source:

   import numpy as np
   import matplotlib.pyplot as plt
   import contrastcolors as cc

   cc.set_style("heri", font="DejaVu Sans")

   colors = cc.color_palette(
       hues=[55, 20, 145, 210, 290],
       ratio=1.20,
       start_luminance=0.72,
   )

   x = np.linspace(0, 8, 250)
   fig, ax = plt.subplots(figsize=(8.0, 4.1))

   for i, color in enumerate(colors):
       ax.plot(
           x,
           np.cos(0.72 * x + i * 0.45) + 0.28 * i,
           color=color,
           label=f"Series {i + 1}",
       )

   ax.set(
       title="Heri layout + generated contrast palette",
       xlabel="x",
       ylabel="Value",
   )
   ax.legend(ncol=3)
   fig.tight_layout()

Publication details
-------------------

Hybrid PDF rasterization
~~~~~~~~~~~~~~~~~~~~~~~~

With ``rasterize=True``, common dense artists such as scatter, hexbin,
``imshow``, ``pcolormesh``, filled contours and 3D surfaces are rasterized.
Ordinary plot lines, error bars, axes, text, ticks and legends stay vector.

.. code-block:: python

   cc.set_style("heri", font="Arial", rasterize=True)
   cc.save_figure(fig, "result.pdf", dpi=600)

Panel labels
~~~~~~~~~~~~

.. code-block:: python

   cc.panel_label(ax, "A")

Temporary styling
~~~~~~~~~~~~~~~~~

.. code-block:: python

   with cc.style_context("heri", font="Arial"):
       fig, ax = plt.subplots()
       ax.plot(x, y)

The previous Matplotlib state is restored after the block.

See :doc:`customization` for hue order, additional colors, markers,
linestyles, alpha and export options.
