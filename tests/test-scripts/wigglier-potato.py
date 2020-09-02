# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2020-01-31
# Copyright (C) 2020, Alexandre De Zotti
# License: MIT License


import sys
import math
import cmath
import random

import mathsvg



general_size = 10
bottom = - 1.5 * general_size
left = - 1.5 * general_size
top = - bottom
right = - left
image_file_name = "wigglier-potato.svg"

image = mathsvg.SvgImage(pixel_density = 42, view_window = ((left, bottom), (right, top)))

random.seed(1000000000000066600000000000001)
image.draw_planar_potato([0.25 * general_size, 0], 0.2 * general_size, general_size, 66)

image.save(image_file_name)



