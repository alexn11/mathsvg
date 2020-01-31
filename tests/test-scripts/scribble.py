# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2020-01-31
# Copyright (C) 2020, Alexandre De Zotti
# License: MIT License


import math
import cmath
import random

import mathsvg

image = mathsvg . SvgImage (pixel_density = 1, view_window = ((0, 0), (400, 150)))

random . seed (1000000000000066600000000000001)
image . draw_random_wavy_line ([20, 75], [380, 75], 2, 55)

image . save ("scribble.svg")
