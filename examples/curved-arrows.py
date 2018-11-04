# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License


import math
import cmath

import mathsvg

the_tau = 2 * math . pi
rescaling = 100




image = mathsvg . SvgImage ("curved-arrows.svg", rescaling = rescaling, shift = [ 4, 4 ])

image . set_view_box ((800, 800))



image . draw_curved_arrow ([ -2, 2 ], [ 2, 2 ])

image . draw_curved_arrow ([ -2, 1 ], [ 2, 1 ], curvedness = .1)

image . draw_curved_arrow ([ -2, 0 ], [ 2, 0 ], curvedness = 0.5)

image . draw_curved_arrow ([ -2, -1 ], [ 2, -1 ], curvedness = -.2)

image . draw_curved_arrow ([ -2, -2 ], [ 2, -2 ], curvedness = 0.)




image . set_dash_mode ("dash")
image . draw_curved_arrow ([ 2.5, -2.5 ], [ -2.5, 2.5 ])

image . save ()




