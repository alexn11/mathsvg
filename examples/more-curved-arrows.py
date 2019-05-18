# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License

import mathsvg


image = mathsvg . SvgImage (pixel_density = 100, view_window = ((-4, -4), (4, 4)))

image . draw_point ([ 0.2, -0.2 ])

image . set_dash_mode ("dots")
image . draw_curved_arrow ([ 0.2, -.2 ], [ 1.7, 1.8 ], curvedness = -1.)


image . set_dash_mode ("none")

image . draw_curved_arrow ([ -2.7, 2 ], [ -0.3, 2 ], asymmetry = - 0.8)

image . draw_curved_arrow ([ -2.7, 1 ], [ -0.3, 1 ], asymmetry = - 0.2)

image . draw_curved_arrow ([ -2.7, 0 ], [ -0.3, 0 ], asymmetry = 0.2)

image . draw_curved_arrow ([ -2.7, -1 ], [ -0.3, -1 ], asymmetry = 0.5)

image . draw_curved_arrow ([ -2.7, -2 ], [ -0.3, -2 ], curvedness = -0.2, asymmetry = 1.2)


image . save ("more-curved-arrows.svg")




