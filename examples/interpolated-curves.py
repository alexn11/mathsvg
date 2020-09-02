# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, 2020, Alexandre De Zotti
# License: MIT License

import mathsvg


image = mathsvg.SvgImage(pixel_density = 100, view_window = ((0, 0), (10, 10)))

open_curve_point_list = [ [2.5,5], [4.5,7], [2.5,4], [0.5,3] ]
closed_curve_point_list = [ [7.4, 2], [5.6, 4], [7.3, 6], [ 4.3, 5.2], [ 8.3, 9.1 ] ]

image.set_svg_options(stroke_color = "red")
image.draw_polyline(open_curve_point_list)
image.set_svg_options(stroke_color = "green")
image.draw_polyline(closed_curve_point_list)
image.draw_line_segment(closed_curve_point_list[-1], closed_curve_point_list[0])
image.set_svg_options(stroke_color = "black")

image.draw_smoothly_interpolated_open_curve(open_curve_point_list)
image.draw_smoothly_interpolated_closed_curve(closed_curve_point_list)

image.save("interpolated-curves.svg")
