# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, 2020, Alexandre De Zotti
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
image_file_name = sys.argv[0][ : -3] + ".svg"


image = mathsvg.SvgImage(pixel_density = 42, view_window = ((left, bottom), (right, top)))

image.draw_planar_potato([0.25 * general_size, 0], 0.2 * general_size, general_size, 18)

image.save(image_file_name)



