.. mathsvg documentation master file, created by
   sphinx-quickstart on Tue Nov  6 20:05:46 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

mathsvg's documentation
=======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


The module defines the class ``SvgImage`` whose instances are used for creating SVG images.

The source code is hosted on `GitHub <https://github.com/alexn11/mathsvg>`_.



Example of how to use your SVG file
-----------------------------------

The SVG file can then be edited using programs such as `Inkscape <https://inkscape.org/>`_. For example you can convert them into ``pdf_tex`` files using the command::

  inkscape -D -z --file=your-svg-file.svg --export-pdf=exported-name.pdf --export-latex

Then include the file in the LaTeX document with:

.. code-block:: latex

  \begin{figure}
    \centering
    \def\svgwidth{\columnwidth}
    \input{exported-name.pdf_tex}
  \end{figure}


Don't forget to include the package ``graphicx``.

See the documentations of the relevant programs for more details.


The SvgImage class
------------------

.. automodule:: mathsvg.mathsvg
   :members:


Examples
--------



.. toctree::
   :glob:

   examples/*


Click on the image to see the sources.

.. include:: image-targets.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
