# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License

import math
import cmath

import mathsvg

the_tau = 2 * math . pi
rescaling = 100




image = mathsvg . SvgImage ("arrows.svg", rescaling = rescaling, shift = [ 4, 4 ])

image . set_view_box ((800, 800))



image . draw_arrow ([ -2, -2 ], [ 2, 2 ])

image . set_arrow_options (curvature = 0.55)
image . draw_arrow ([ -2, -2 ], [ 2, 1.7 ])

image . reset_arrow_options ()
image . set_arrow_options (width = 4 * image . arrow_width)
image . draw_arrow ([ -2, -2 ], [ 2, 1.2 ])


image . reset_arrow_options ()
image . set_arrow_options (width = 2 * image . arrow_width)
image . set_arrow_options (curvature = 0)
image . draw_arrow ([ -2, -2 ], [ 2, 0.6 ])


image . reset_arrow_options ()
image . set_svg_options (stroke_color = "red")
image . draw_arrow ([ -2, -2 ], [ 2, 0.3 ])

image . set_svg_options (stroke_color = "black")
image . set_dash_mode ("dash")
image . draw_arrow ([ -2, -2 ], [ 2, 0.0 ])

image . set_dash_mode ("dot")
image . draw_arrow ([ -2, -2 ], [ 2, -0.3 ])


image . set_arrow_options (width = 8 * image . arrow_width)
image . draw_arrow_tip ([ 1., -2], math . pi - 0.1)

image . set_dash_mode ("none")
image . reset_arrow_options ()
image . set_arrow_options (curvature = -0.22, width = 2.4 * image . arrow_width)
image . draw_arrow ([ 2, -2 ], [ -2, 2 ])

image . save ()




