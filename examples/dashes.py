# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License

import mathsvg

image = mathsvg . SvgImage (pixel_density = 100, view_window = ((2, 0), (10, 8)))

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
