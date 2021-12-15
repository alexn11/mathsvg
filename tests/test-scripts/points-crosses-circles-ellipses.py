# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, 2020, Alexandre De Zotti
# License: MIT License

import math
import cmath

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.pardir))
import mathsvg

two_pi = 2 * math.pi

image = mathsvg.SvgImage(pixel_density = 100, view_window = ((-4, -4), (4, 4)))

image.draw_point([0, 0])
image.draw_point([1, 0])

image.draw_cross([0, 1])
image.draw_cross([0, -1])
image.draw_cross([-1, 0])

image.draw_circle([0, 0], 2.5)

image.draw_circle_arc([0, 0], 2.88, 0.2, 1.1)

focuses = [ [-1.33, 0.61], [1.33, -0.61] ]

image.draw_plus(focuses [0])
image.draw_plus(focuses [1])

image.set_dash_mode("dash")
image.draw_ellipse_arc(focuses, 0.412, two_pi * 0.1, two_pi * 0.8)

image.set_dash_mode("dot")
image.draw_ellipse(focuses, 0.68)

image.save("points-crosses-circles-ellipses.svg", do_overwrite=True)
