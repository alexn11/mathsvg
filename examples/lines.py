# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, 2020, Alexandre De Zotti
# License: MIT License

import mathsvg

image = mathsvg.SvgImage(pixel_density = 100, view_window = ((-4, -4), (4, 4)))

image.draw_line_segment([-3.5, 3.5], [-3, 3.2])

image.draw_line_segment([-3.2, 3.5], [-2.7, 3.2])
image.draw_line_segment([-3.2, 3.5], [-2.5, 3.2])
image.draw_line_segment([-3.2, 3.5], [-2.3, 3.2])
image.draw_line_segment([-3.2, 3.5], [-2.1, 3.2])
image.draw_line_segment([-3.2, 3.5], [-1.9, 3.2])
image.draw_line_segment([-3.2, 3.5], [-1.7, 3.2])
image.draw_line_segment([-3.2, 3.5], [-1.5, 3.2])
image.draw_line_segment([-3.2, 3.5], [-1.3, 3.2])

image.draw_random_wavy_line([-1.5, 3], [1, -3], 0.2, 0.33)
image.set_dash_mode("dash")
image.draw_random_wavy_line([-1.5, 3], [1, -3], 0.2, 2.4)

image.set_dash_mode("dot")
image.draw_line_segment([-3., -2.9], [3., 3.1])
image.set_dash_mode("none")
image.draw_random_wavy_line([-3., -2.8], [3., 3.2], 0.1, 0.1)
image.set_dash_mode("dot")
image.draw_line_segment([-3., -2.7], [3., 3.3])

image.save("lines.svg")
