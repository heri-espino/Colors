Palette & Plot Studio
=====================

The Studio is a static, interactive browser application for designing
contrast-controlled scientific figures. It runs without a server, database,
Python interpreter, or account and works with the Sphinx site on GitHub Pages.

.. raw:: html

   <p class="cc-actions">
     <a class="cc-button primary" href="_static/studio.html" target="_blank" rel="noopener">
       Open Studio in a full browser tab
     </a>
     <a class="cc-button" href="gallery.html">Explore examples</a>
   </p>

   <iframe
     id="cc-studio-frame"
     src="_static/studio.html"
     title="Interactive contrastcolors Palette and Plot Studio"
     style="width:100%;height:3200px;border:0;border-radius:12px;"
     loading="lazy"
   ></iframe>

   <script>
     window.addEventListener("message", function (event) {
       var frame = document.getElementById("cc-studio-frame");
       if (!frame || event.source !== frame.contentWindow ||
           event.origin !== window.location.origin) return;
       if (!event.data || event.data.type !== "contrastcolors-studio-height") return;
       var value = Number(event.data.height);
       if (Number.isFinite(value) && value > 400 && value < 15000) {
         frame.style.height = Math.ceil(value + 28) + "px";
       }
     });
   </script>

What you can customize
----------------------

- **Palette**: 2 to 10 hues, their order, OKLCH chroma, initial WCAG
  luminance, and constant adjacent contrast ratio.
- **Series identifiers**: marker and line style for each series.
- **Plot gallery**: lines, time series, histograms, box plots, violins,
  ridge plots, scatter, categorical heatmaps, and grouped bar charts.
- **Print preview**: color, ideal luminance-preserving grayscale, and
  a deliberately degraded print-stress simulation.
- **Alpha**: opacity, background, and apparent-color compensation.
- **Publication style**: Heri or Matplotlib default, custom font,
  dense-artist rasterization, and output DPI.

The interactive preview is SVG generated in the browser. It is a fast visual
approximation, not the Matplotlib renderer. The **Copy code** action generates
a complete, reproducible Python example for the selected plot family.

Saving and importing designs
----------------------------

Give the palette a valid Python identifier, such as ``paper_palette``.

- **Save locally** remembers the design in the current browser's local
  storage. Use Load or Delete to manage existing local designs.
- **Download JSON** exports the current palette, identifiers, alpha,
  style, and selected plot type. **Import JSON** brings it back on another
  browser or computer.
- **Download Python preset** creates a module that registers the named
  palette with the installed Python library.

Local saves are browser-specific, and may be cleared by browser privacy
settings. Export JSON for a portable backup.

Using an exported Python preset
-------------------------------

For example, download ``paper_palette.py`` and put it next to your plot
script, then:

.. code-block:: python

   import contrastcolors as cc
   import paper_palette  # registers the preset in this process

   colors = cc.color_palette("paper_palette")
   scheme = cc.plot_scheme("paper_palette")

   for y, style in zip(series, scheme):
       ax.plot(x, y, **style)

You can also register the palette directly:

.. code-block:: python

   import contrastcolors as cc

   cc.register_palette(
       "paper_palette",
       hues=[55, 20, 145, 210, 290],
       ratio=1.22,
       start_luminance=0.72,
       markers=["o", "s", "^", "D", "X"],
       linestyles=["-", "--", ":", "-.", (0, (5, 2))],
   )

   colors = cc.color_palette("paper_palette")

Registration is process-local; import the exported module every time you
launch a new Python process. It does not modify the installed package files.

GitHub Pages
------------

The standalone Studio is available within the Sphinx build at
``_static/studio.html``. The interactive site requires
**Settings > Pages > Build and deployment > Source: GitHub Actions**, followed
by the repository's manual ``pages`` deployment workflow. A default Jekyll
workflow does not build the Sphinx documentation.
