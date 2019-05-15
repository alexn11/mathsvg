# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2019-05-18
# Copyright (C) 2019, Alexandre De Zotti
# License: MIT License


import sys
import math
import cmath

import mathsvg


general_size = 10
bottom = - 1.5 * general_size
left = - 1.5 * general_size
top = - bottom
right = - left
rescaling = 42



image = mathsvg . SvgImage (file_name = "save-1.svg", rescaling = rescaling, shift = [- left, - bottom])
image . set_view_box ((rescaling * (right - left), rescaling * (top - bottom)))

image . draw_planar_potato ([0.25 * general_size, 0], 0.3 * general_size, general_size, 10)

image . save ()

image . draw_point ([0.25 * general_size, 0])
image . save ("save-2.svg")



