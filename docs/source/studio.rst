Palette & Plot Studio
=====================

The Studio is the interactive front end for contrastcolors. It runs entirely
in the browser and requires no backend, so the same build can be served
directly by GitHub Pages.

Use it to:

- choose the number of series;
- set adjacent WCAG contrast ratio, starting luminance, and OKLCH chroma;
- reorder hue assignments across luminance levels;
- choose one marker and line style per series;
- preview the same figure in color and ideal grayscale;
- run a deliberately degraded print-stress preview;
- inspect alpha compensation against a selected background;
- select the Heri plotting font and export settings;
- copy ready-to-paste Python using plot_scheme;
- download the design as JSON.

.. raw:: html

   <iframe
     src="_static/studio.html"
     title="contrastcolors Palette and Plot Studio"
     style="width:100%;height:2450px;border:0;border-radius:12px;"
   ></iframe>

GitHub Pages
------------

The Studio is static HTML/CSS/JavaScript embedded in the Sphinx site. Building
the documentation copies it into _static automatically.

Build locally with:

.. code-block:: bash

   python -m pip install -e ".[docs]"
   sphinx-build -W -b html docs/source docs/_build/html

Then open docs/_build/html/studio.html through the Sphinx site.

The repository also contains a manual pages GitHub Actions workflow. Once
GitHub Pages is configured to use GitHub Actions, that workflow uploads
docs/_build/html as the site artifact and deploys it.
