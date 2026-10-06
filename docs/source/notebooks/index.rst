Notebook cookbook
=================

These notebooks are executable Sphinx pages. During the documentation build,
MyST-NB runs the code against the installed version of contrastcolors and
embeds the real Matplotlib outputs.

.. toctree::
   :maxdepth: 1

   00_overview
   01_lines_time_series
   02_histograms_distributions
   03_box_violin_ridge
   04_scatter_relationships
   05_heatmaps_matrices
   06_categorical
   07_uncertainty
   08_print_grayscale
   09_publication_multipanel
   10_alpha_background
   11_palettes_colormaps

Refresh every notebook at once
------------------------------

You do not need to execute the notebooks one by one.

Locally:

.. code-block:: bash

   python -m pip install -e ".[docs]"
   python tools/execute_notebooks.py

The command executes every IPython notebook in docs/source/notebooks and writes
the generated figures and cell outputs back into the .ipynb files.

GitHub Actions
~~~~~~~~~~~~~~

The manual workflow named ``refresh notebooks and site`` performs the entire
publication workflow in one run:

1. installs contrastcolors and the notebook dependencies;
2. executes all notebooks;
3. saves every output inside the notebooks;
4. commits changed .ipynb files back to the repository;
5. builds Sphinx from the stored outputs; and
6. deploys the refreshed GitHub Pages site.

Ordinary Sphinx builds use the stored outputs and do not execute all notebooks
again. This keeps routine documentation CI lightweight.
