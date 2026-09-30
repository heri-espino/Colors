API reference
=============

This reference documents the public API first, followed by lower-level module
helpers intended for advanced use.

High-level palette API
----------------------

.. autofunction:: contrastcolors.color_palette

.. autofunction:: contrastcolors.contrast_palette

.. autofunction:: contrastcolors.show_palette

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

Publication style
-----------------

.. autofunction:: contrastcolors.set_style

.. autofunction:: contrastcolors.style_context

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
