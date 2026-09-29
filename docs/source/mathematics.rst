Mathematics
===========

Constant contrast ladder
------------------------

For descending relative luminances :math:`Y_k` and an adjacent WCAG contrast
ratio :math:`r`, impose

.. math::

   \frac{Y_k+0.05}{Y_{k+1}+0.05}=r.

Therefore

.. math::

   Y_k=\frac{Y_0+0.05}{r^k}-0.05.

Hue-luminance matrix
--------------------

For hue choices :math:`h_1,\ldots,h_j`, the library constructs

.. math::

   C_{k\ell}=C(Y_k,h_\ell).

Every cell in row :math:`k` has relative luminance :math:`Y_k`. Thus selecting
one arbitrary hue from every row preserves the same adjacent contrast ratio.

Alpha compensation
------------------

For target color :math:`T`, opaque background :math:`B`, source color
:math:`S`, and opacity :math:`\alpha`, simple sRGB alpha composition is

.. math::

   T=\alpha S+(1-\alpha)B.

When feasible in sRGB,

.. math::

   S=\frac{T-(1-\alpha)B}{\alpha}.


Gamut-limited alpha compensation
--------------------------------

The inverse source color may leave the sRGB cube. Exact recovery is then
impossible for that opacity/background pair. The default fallback minimizes

.. math::

   \Delta E_{OK}\left(
      \alpha S + (1-\alpha)B,\,T
   \right)

over representable source colors :math:`S\in[0,1]^3`, using Euclidean
distance in OKLab. The analytical inverse is still used whenever it is
feasible, so optimization introduces no approximation in the exact case.
