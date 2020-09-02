# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, 2020, Alexandre De Zotti
# License: MIT License


import math

import mathsvg

def a_function_with_two_parameters(x, a, b):
  return a * x + b

image = mathsvg.SvgImage(pixel_density = 100, view_window = ((0, -5), (10, 5)))

function = lambda x : math.sin(5 * x)

image.set_svg_options(stroke_color = "blue")
image.draw_function_graph(function, 0, 10, 33, curve_type = "polyline")
image.set_svg_options(stroke_color = "black")
image.draw_function_graph(function, 0, 10, 214, curve_type = "autosmooth")

image.set_svg_options(stroke_color = "red")
image.draw_function_graph(lambda x : math.exp(0.2 * x) - 3, 0, 10, 214, curve_type = "autosmooth")

image.set_svg_options(stroke_color = "green")
image.draw_function_graph(a_function_with_two_parameters, 0, 10, 4, 1., -.5, curve_type = "polyline")
image.draw_function_graph(a_function_with_two_parameters, 0, 10, 4, 2., -2.5, curve_type = "polyline")
image.draw_function_graph(a_function_with_two_parameters, 0, 10, 4, 0., 1.5, curve_type = "polyline")
image.draw_function_graph(a_function_with_two_parameters, 0, 10, 4, -1., 3.5, curve_type = "polyline")
image.draw_function_graph(a_function_with_two_parameters, 0, 10, 4, -2., 5.5, curve_type = "polyline")

image.reset_svg_options()
image.draw_arrow([ 0.5, -2.2 ], [ 9.5, -2.2 ])
image.draw_arrow([ 1.2, -4.5 ], [ 1.2, 4.5 ])

image.save("graphs.svg")
