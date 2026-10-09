API reference
=============

This reference documents the public API first, followed by lower-level module
helpers intended for advanced use.

High-level palette API
----------------------

.. autofunction:: contrastcolors.color_palette

.. autofunction:: contrastcolors.contrast_palette

.. autofunction:: contrastcolors.show_palette

.. autofunction:: contrastcolors.plot_scheme

.. autofunction:: contrastcolors.scatter_scheme

DEFAULT_MARKERS
    Default marker sequence used by plot_scheme.

DEFAULT_LINESTYLES
    Default line-style sequence used by plot_scheme.

Accessibility and print previews
--------------------------------

DEFAULT_ACCESSIBILITY_MODES
    Original, grayscale, print-stress, deuteranopia, protanopia, tritanopia.

.. autofunction:: contrastcolors.figure_to_rgba

.. autofunction:: contrastcolors.to_grayscale_image

.. autofunction:: contrastcolors.to_print_stress_image

.. autofunction:: contrastcolors.simulate_cvd_image

.. autofunction:: contrastcolors.simulate_figure

.. autofunction:: contrastcolors.figure_variants

.. autofunction:: contrastcolors.show_vector_accessibility_panel

For standard line and scatter plots, this function redraws vector artists
per viewing mode instead of rasterizing the original graphic. Export its
Matplotlib figure as PDF or PGF; PGF can be included in the manuscript for
the exact document font. Unsupported artist types raise explicitly.

.. autofunction:: contrastcolors.show_accessibility_panel

.. autofunction:: contrastcolors.save_accessibility_panel

Named palette presets
---------------------

Presets register palettes for the current Python process. Put the registration
in a project module, then import it in each script that needs those names.

.. autofunction:: contrastcolors.register_palette

.. autofunction:: contrastcolors.get_palette

.. autofunction:: contrastcolors.available_palettes

.. autoclass:: contrastcolors.PalettePreset
   :members:

Example:

.. code-block:: python

   import contrastcolors as cc

   cc.register_palette(
       "paper_palette",
       hues=[55, 20, 145, 210, 290],
       ratio=1.25,
       start_luminance=0.72,
       markers=["o", "s", "^", "D", "X"],
       linestyles=["-", "--", ":", "-.", (0, (5, 2))],
   )
   colors = cc.color_palette("paper_palette")
   scheme = cc.plot_scheme("paper_palette")

Core palette objects
--------------------

.. autoclass:: contrastcolors.ColorCell
   :members:

.. autoclass:: contrastcolors.RenderedColor
   :members:

.. autoclass:: contrastcolors.Palette
   :members:
   :special-members: __len__, __getitem__

.. autoclass:: contrastcolors.ContrastGrid
   :members:
   :special-members: __getitem__

Palette construction
--------------------

.. autofunction:: contrastcolors.color_for_luminance

.. autofunction:: contrastcolors.contrast_grid

Contrast mathematics
--------------------

.. autofunction:: contrastcolors.luminance_ladder

.. autofunction:: contrastcolors.luminance_contrast

.. autofunction:: contrastcolors.relative_luminance

.. autofunction:: contrastcolors.contrast_ratio

Alpha and compositing
---------------------

.. autoclass:: contrastcolors.AlphaCompensation
   :members:

.. autofunction:: contrastcolors.composite

.. autofunction:: contrastcolors.compensate_alpha

.. autofunction:: contrastcolors.minimum_alpha

Color utilities
---------------

.. autofunction:: contrastcolors.to_rgb

.. autofunction:: contrastcolors.to_hex

.. autofunction:: contrastcolors.srgb_to_oklab

.. autofunction:: contrastcolors.delta_e_ok

Categorical pie charts
----------------------

.. autofunction:: contrastcolors.pie_plot

Pie wedges use white separators by default (with a user-overridable
edgecolor/linewidth), plus the same adaptive color and luminance policy
as other categorical plots.

Adaptive print-safe colors
--------------------------

.. autofunction:: contrastcolors.print_safe_luminances

The default contrastcolors.plot_scheme() and scatter_scheme() distribute
luminances across a broad grayscale range when the number of series is
small (and both the contrast ratio and starting luminance are omitted).
Named presets and explicit contrast ratios are kept unchanged.

LaTeX layout and publication fitting
------------------------------------

.. autoclass:: contrastcolors.LatexFontInfo
   :members:

.. autofunction:: contrastcolors.find_latex_font

.. autoclass:: contrastcolors.LatexLayout
   :members:

.. autoexception:: contrastcolors.LatexProbeError

.. autoclass:: contrastcolors.PublicationStyle
   :members:

.. autoclass:: contrastcolors.FigureAudit
   :members:

.. autoclass:: contrastcolors.FitResult
   :members:

.. autofunction:: contrastcolors.inspect_latex

.. autofunction:: contrastcolors.latex_style

.. autofunction:: contrastcolors.audit_figure

.. autofunction:: contrastcolors.fit_figure_to_latex

.. autofunction:: contrastcolors.verify_latex_placement

TEX_PT_PER_INCH
    Conversion constant: 72.27 TeX points per inch.

Publication style
-----------------

.. autofunction:: contrastcolors.set_style

.. autofunction:: contrastcolors.style_context

.. autofunction:: contrastcolors.apply_elegant_axes

.. autofunction:: contrastcolors.nice_tick_bounds

.. autofunction:: contrastcolors.save_figure

.. autofunction:: contrastcolors.panel_label

.. autofunction:: contrastcolors.available_styles

Heri style constants
--------------------

HERI_PALETTE
    Five categorical colors used as the default Heri line cycle.

    .. code-block:: text

       #97001c
       #0083f9
       #00b49c
       #ffc600
       #f198ff

HERI_NEUTRAL
    Neutral colors used for axes, reference lines, and grid styling.

    .. code-block:: python

       {
           "black": "#111111",
           "dark": "#3A3A3A",
           "mid": "#777777",
           "light": "#B0B0B0",
           "grid": "#D8D8D8",
       }

HERI_IRIDESCENT_HEX
    Twenty-three control colors used to construct the continuous Heri
    iridescent colormap.

HERI_CMAP
    A 256-level Matplotlib LinearSegmentedColormap constructed from
    HERI_IRIDESCENT_HEX. Missing/bad values use #999999.

Advanced color-space helpers
----------------------------

These functions live in the contrastcolors.color_spaces module. They are useful
for implementing custom palette algorithms or diagnostics, but are not all
re-exported at the package root.

.. autofunction:: contrastcolors.color_spaces.srgb_to_linear

.. autofunction:: contrastcolors.color_spaces.linear_to_srgb

.. autofunction:: contrastcolors.color_spaces.oklch_to_linear_srgb

.. autofunction:: contrastcolors.color_spaces.in_srgb_gamut

Advanced style constants
------------------------

contrastcolors.style.HERI_BAD_DATA_COLOR
    Hex color #999999 used for bad/missing values in HERI_CMAP.

contrastcolors.style.HERI_SAVEFIG_KWARGS
    Default save settings used by save_figure:

    .. code-block:: python

       {
           "dpi": 600,
           "bbox_inches": "tight",
           "pad_inches": 0.035,
           "facecolor": "white",
           "edgecolor": "white",
           "transparent": False,
       }
