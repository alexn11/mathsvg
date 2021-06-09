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


Here is a simple example::

   import mathsvg
   image = mathsvg.SvgImage(pixel_density = 100, view_window = (( -1, -1 ), ( 1, 1 )))
   image.draw_circle([0, 0], 1.1)
   image.save("simple-example.svg")

The above example produces the following image:

.. image:: simple-example.svg
   :width: 200px
   :height: 200px
   :align: center
   :alt: A cropped circle centered on a square canvas


You can install mathsvg with ``pip``::

   pip install mathsvg



Example of how to use your SVG file
-----------------------------------

The SVG file can then be edited using programs such as `Inkscape <https://inkscape.org/>`_. *For example* you can convert them into ``pdf_tex`` files using the command::

  inkscape -D math-svg-saved-image.svg  -o exported-name.pdf --export-latex

Then include the file in the LaTeX document with:

.. code-block:: latex

  \begin{figure}
    \centering
    \def\svgwidth{\columnwidth}
    \input{exported-name.pdf_tex}
  \end{figure}


Don't forget to include the package ``graphicx``.

See the documentations of the relevant programs for more details.


Examples
--------

.. toctree::
   :glob:

   more-examples/*


Click on the image to see the sources.

.. include:: more-image-targets.rst


The SvgImage class
------------------

.. automodule:: mathsvg.mathsvg
   :members:


Feature examples
----------------



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
