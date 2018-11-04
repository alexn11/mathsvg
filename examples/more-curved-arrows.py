# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License

import math
import cmath

import mathsvg

the_tau = 2 * math . pi
rescaling = 100




image = mathsvg . SvgImage ("more-curved-arrows.svg", rescaling = rescaling, shift = [ 4, 4 ])

image . set_view_box ((800, 800))

image . draw_point ([ 0.2, -0.2 ])

image . set_dash_mode ("dots")
image . draw_curved_arrow ([ 0.2, -.2 ], [ 1.7, 1.8 ], curvedness = -1.)


image . set_dash_mode ("none")

image . draw_curved_arrow ([ -2.7, 2 ], [ -0.3, 2 ], asymmetry = - 0.8)

image . draw_curved_arrow ([ -2.7, 1 ], [ -0.3, 1 ], asymmetry = - 0.2)

image . draw_curved_arrow ([ -2.7, 0 ], [ -0.3, 0 ], asymmetry = 0.2)

image . draw_curved_arrow ([ -2.7, -1 ], [ -0.3, -1 ], asymmetry = 0.5)

image . draw_curved_arrow ([ -2.7, -2 ], [ -0.3, -2 ], curvedness = -0.2, asymmetry = 1.2)



image . save ()




