# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, 2020, Alexandre De Zotti
# License: MIT License


import math
import cmath

import mathsvg

image = mathsvg.SvgImage(pixel_density = 1, view_window = ((0, 0), (400, 150)))

image.draw_random_wavy_line([20, 75], [380, 75], 2, 55)

image.save("scribble.svg")
