# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License

import math
import cmath

import mathsvg

rescaling = 100

image = mathsvg . SvgImage (rescaling = rescaling, shift = [ -2, 0 ])

image . set_view_box ((800, 800))

image . set_dash_mode ("dash")
image . draw_line_segment ([0, 0], [10, 10])

image . set_dash_mode ("dot")
image . draw_line_segment ([0, 10], [10, 0])

image . set_svg_options (dash_array = [18, 3, 1, 3, 7, 3, 1, 3])
image . set_dash_mode ("dasharray")
image . draw_planar_potato ([5, 5], 2, 4, 8)

image . set_dash_mode ("none")
image . draw_line_segment ([4, 2], [8, 2])

image . save ("dashes.svg")
