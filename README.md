# mathsvg
A  Python library to draw mathematical objects. Create figures and diagrams and save them as SVG files.

The complete documentation is available at: https://mathsvg.readthedocs.io.
The sources are hosted on GitHub: https://github.com/alexn11/mathsvg.

Programs such as Inkscape are great for creating vector graphics. But Inkscape is made more for designer rather than for mathematicians. The process of doing mathematical diagrams and illustrations using Inkscape can sometimes be quite frustrating. Making a python script to produce the content of an SVG file can be a faster solution.

The role of mathsvg is to help with the process of producing your own SVG diagrams using Python scripts. For that purpose a class SvgImage is defined which contains many usefull routines that simplify the creation of mathematical figures with precise descriptions.

Once the mathsvg package and all its dependencies are installed it can be used as a normal Python package.

Here is an example for the creation of a very simple image:

    import mathsvg
    image = mathsvg . SvgImage (pixel_density = 100, view_window = (( -1, -1 ), ( 1, 1 )))
    image . draw_circle ([0, 0], 1.1)
    image . save ("simple-example.svg")


The above program does the following.

After importing the package mathsvg, a SvgImage object is created. The parameters of the constructors are the pixel density (number of pixel per unit of length) and the view window which selects the part of the plane that will be rendered in the image. The coordinates of mathematical objects will be automatically be converted into coordinates on the SVG canvas.

A circle with center (0, 0) and radius 1.1 is drawn using the default drawing options (black solid stroke). Some points of the circle won't appear in the image since they are outside the canvas.

Finally the image is saved in a file with the name "simple-example.svg". 


