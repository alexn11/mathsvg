# mathsvg
A  Python library to draw mathematical objects. Create figures and diagrams and save them as SVG files.

The complete documentation is available at: https://mathsvg.readthedocs.io.
The sources are hosted on GitHub: https://github.com/alexn11/mathsvg.

Programs such as Inkscape are great for creating vector graphics. But Inkscape is made more for designer rather than for mathematicians. The process of doing mathematical diagrams and illustrations using Inkscape can sometimes be quite frustrating. Making a python script to produce the content of an SVG file can be a faster solution.

The role of mathsvg is to help with the process of producing your own SVG diagrams using Python scripts. For that purpose a class SvgImage is defined which contains many usefull routines that simplify the creation of mathematical figures with precise descriptions.

Once the mathsvg package and all its dependencies are installed it can be used as a normal Python package.

Here is an example for the creation of a very simple image:

    import mathsvg
    image = mathsvg . SvgImage (rescaling = 100, shift = [ 1, 1 ], view_box = (200, 200))
    image . draw_circle ([0, 0], 1.1)
    image . save ("simple-example.svg")


The above program does the following.

After importing the package mathsvg, a SvgImage object is created. The parameters of the constructors are a rescaling factor, a shift vector and the view box. The rescaling factor and the shift vector are used to convert mathematical object coordinates into pixel coordinates in the SVG. The shift vector corresponds to a translation which is first applied to the coordinates. After this translation both coordinates are multiplied by the rescaling factor. Those are optional parameters and the respective default are 1 and [0, 0]. As for the view box, this means that only the points with x and y coordinates between -1 and 1 will be on the canvas (the y axis is automatically flipped over, ignore the content of this parenthesis if you don't know why this should be).

A circle with center (0, 0) and radius 1.1 is drawn using the default drawing options (black solid stroke). Some points of the circle won't appear in the image since they are outside the canvas.

Finally the file is saved with the name "simple-example.svg". 


