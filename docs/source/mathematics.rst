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
