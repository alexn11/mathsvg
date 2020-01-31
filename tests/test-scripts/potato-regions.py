# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2020-01-31
# Copyright (C) 2020, Alexandre De Zotti
# License: MIT License




import math
import cmath
import random

import mathsvg


image = mathsvg . SvgImage (pixel_density = 100, view_window = ((-2, -2), (2, 2)))

center = [0, 0]
inner_radius = 0.5
outer_radius = 1.5

image . set_dash_mode ("dots")
image . draw_circle (center, inner_radius)
image . draw_circle (center, outer_radius)
image . set_dash_mode ("none")
random . seed (1000000000000066600000000000001)
image . draw_planar_potato (center, inner_radius, outer_radius, 5)


image . save ("potato-regions.svg")



