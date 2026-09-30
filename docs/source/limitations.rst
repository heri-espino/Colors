Guarantees and limitations
==========================

What is guaranteed
------------------

Constant adjacent contrast
~~~~~~~~~~~~~~~~~~~~~~~~~~

For a valid generated luminance ladder, adjacent target colors are constructed
to have the requested WCAG contrast ratio, up to numerical precision and sRGB
gamut solving.

Hue independence inside a grid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every cell in one ContrastGrid row targets the same WCAG relative luminance.
Selecting a different hue from that row therefore preserves the row's intended
contrast relationship with adjacent rows.

Explicit alpha feasibility
~~~~~~~~~~~~~~~~~~~~~~~~~~

When alpha compensation is exactly feasible, AlphaCompensation.feasible is
True. When it is not feasible inside sRGB, the library reports False and uses
the requested fallback strategy rather than claiming exact recovery.

What is not guaranteed
----------------------

WCAG contrast is not categorical separability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A constant luminance contrast ratio does not imply that all hues are equally
easy to distinguish as categorical labels. Hue separation, chroma, display
conditions, color-vision deficiency, marker shape, line style, and spatial
context all matter.

For scientific categories, redundant encodings such as marker shape and line
style remain useful.

Generated palettes are not automatically colorblind-safe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The current package does not yet simulate color-vision deficiencies or optimize
palettes specifically for them. The Heri plotting style uses a publication
palette with redundant visual encodings in its source paper, but arbitrary
generated hue lists should be evaluated for the intended audience.

Alpha depends on the background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A source color compensated for a white background is not generally compensated
for a gray, black, or transparent-changing background. Alpha compensation must
be computed for the background on which the artist will actually be rendered.

Exact alpha preservation may be impossible
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The analytical inverse

.. math::

   S=\frac{T-(1-\alpha)B}{\alpha}

can lie outside the sRGB cube. In that case no sRGB source color can reproduce
the target exactly at that alpha and background.

The default perceptual fallback minimizes OKLab error, but the result remains an
approximation.

Font availability is environment-dependent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

set_style accepts arbitrary Matplotlib family names such as Arial. If a font is
not installed, normal Matplotlib font fallback applies. The package does not
ship font files.

External LaTeX is only used for the Utopia mode when the required TeX packages
are available. Custom fonts use native Matplotlib text in automatic mode.

Rasterization is artist-based
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Heri style automatically rasterizes common dense artists such as scatter,
hexbin, imshow, pcolormesh, contourf, fill_between, and 3D surfaces. It cannot
know whether every custom Matplotlib artist is dense. Users can still set
rasterized=True or False explicitly on individual artists.

Current contrast model
----------------------

The implemented contrast model is WCAG relative-luminance contrast. APCA is
planned but is not currently implemented. Do not interpret the ratio parameter
as an APCA score.

Numerical precision
-------------------

Color construction uses iterative numerical solutions for OKLCH lightness and
gamut-limited chroma. Achieved luminance and contrast should be checked through
ColorCell.actual_luminance and Palette.adjacent_contrast when exact numerical
values matter.
