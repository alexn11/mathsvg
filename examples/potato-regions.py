# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License




import math
import cmath

import mathsvg




image = mathsvg . SvgImage (rescaling = 100, shift = [2, 2])
image . set_view_box ((400, 400))

center = [0, 0]
inner_radius = 0.5
outer_radius = 1.5

image . set_dash_mode ("dots")
image . draw_circle (center, inner_radius)
image . draw_circle (center, outer_radius)
image . set_dash_mode ("none")
image . draw_planar_potato (center, inner_radius, outer_radius, 5)


image . save ("potato-regions.svg")



