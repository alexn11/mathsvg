# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2020-01-31
# Copyright (C) 2020, Alexandre De Zotti
# License: MIT License


import cmath
import math
import random
import sys

import mathsvg


general_size = 10
bottom = - 1.5 * general_size
left = - 1.5 * general_size
top = - bottom
right = - left

image = mathsvg.SvgImage(pixel_density = 42, view_window = ((left, bottom), (right, top)))

random.seed(10000000000000666000000000000001)
image.draw_planar_potato([0.25 * general_size, 0], 0.3 * general_size, general_size, 10)

image.save("save-1.svg")

image.draw_point([0.25 * general_size, 0])
image.save("save-2.svg")



