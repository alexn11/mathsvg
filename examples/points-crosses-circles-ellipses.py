# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License

import math
import cmath

import mathsvg

the_tau = 2 * math . pi

rescaling = 100

image = mathsvg . SvgImage ("points-crosses-circles-ellipses.svg", rescaling = rescaling, shift = [ 4, 4 ])

image . set_view_box ((800, 800))

image . draw_point ([0, 0])
image . draw_point ([1, 0])

image . draw_cross ([0, 1])
image . draw_cross ([0, -1])
image . draw_cross ([-1, 0])

image . draw_circle ([0, 0], 2.5)

image . draw_circle_arc ([0, 0], 2.88, 0.2, 1.1)

focuses = [ [-1.33, 0.61], [1.33, -0.61] ]

image . draw_plus (focuses [0])
image . draw_plus (focuses [1])

image . set_dash_mode ("dash")
image . draw_ellipse_arc (focuses, 0.412, the_tau * 0.1, the_tau * 0.8)

image . set_dash_mode ("dot")
image . draw_ellipse (focuses, 0.68)

image . save ()
