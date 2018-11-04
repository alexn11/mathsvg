# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License


import math
import cmath

import mathsvg


general_size = 10
bottom = - 1.5 * general_size
left = - 1.5 * general_size
top = - bottom
right = - left
rescaling = 42



image = mathsvg . SvgImage ("potato-3v.svg", rescaling = rescaling, shift = [- left, - bottom])
image . set_view_box ((rescaling * (right - left), rescaling * (top - bottom)))


image . draw_planar_potato ([0.25 * general_size, 0], 0.5 * general_size, general_size, 3)


image . save ()



