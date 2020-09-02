# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, 2020, Alexandre De Zotti
# License: MIT License


import math
import cmath

import mathsvg


general_size = 10
bottom = - 1.5 * general_size
left = - 1.5 * general_size
top = - bottom
right = - left

image = mathsvg.SvgImage(pixel_density = 42, view_window = ((left, bottom), (right, top)))

image.draw_planar_potato([0.25 * general_size, 0], 0.5 * general_size, general_size, 5)

image.save("potato.svg")



