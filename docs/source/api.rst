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

.. autodata:: contrastcolors.HERI_PALETTE
   :annotation:

.. autodata:: contrastcolors.HERI_NEUTRAL
   :annotation:

.. autodata:: contrastcolors.HERI_IRIDESCENT_HEX
   :annotation:

.. autodata:: contrastcolors.HERI_CMAP
   :annotation:

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

These are implementation-facing values from contrastcolors.style.

.. autodata:: contrastcolors.style.HERI_BAD_DATA_COLOR
   :annotation:

.. autodata:: contrastcolors.style.HERI_SAVEFIG_KWARGS
   :annotation:
