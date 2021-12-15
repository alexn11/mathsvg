# Author:  alexn11(alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright(C) 2018, 2020, 2021 Alexandre De Zotti
# License: MIT License

import os
import sys

import math
import cmath

sys.path.insert(0, os.path.abspath(os.path.pardir))
import mathsvg

image = mathsvg.SvgImage(pixel_density = 100, view_window = ( (-4, -4), (4, 4) )) 

image.draw_arrow([ -2, -2 ], [ 2, 2 ])

image.set_arrow_options(curvature = 0.55)
image.draw_arrow([ -2, -2 ], [ 2, 1.7 ])

image.reset_arrow_options()
image.set_arrow_options(width = 4 * image.arrow_width_svgpx, units='svg')
image.draw_arrow([ -2, -2 ], [ 2, 1.2 ])


image.reset_arrow_options()
image.set_arrow_options(width = 2 * image.arrow_width_svgpx, units='svg')
image.set_arrow_options(curvature = 0)
image.draw_arrow([ -2, -2 ], [ 2, 0.6 ])


image.reset_arrow_options()
image.set_svg_options(stroke_color = "red")
image.draw_arrow([ -2, -2 ], [ 2, 0.3 ])

image.set_svg_options(stroke_color = "black")
image.set_dash_mode("dash")
image.draw_arrow([ -2, -2 ], [ 2, 0.0 ])

image.set_dash_mode("dot")
image.draw_arrow([ -2, -2 ], [ 2, -0.3 ])


image.set_arrow_options(width = 8 * image.arrow_width_svgpx, units='svg')
image.draw_arrow_tip([ 1., -2], math.pi - 0.1)

image.set_dash_mode("none")
image.reset_arrow_options()
image.set_arrow_options(curvature = -0.22, width = 2.4 * image.arrow_width_svgpx, units='svg')
image.draw_arrow([ 2, -2 ], [ -2, 2 ])

image.save("arrows.svg")




