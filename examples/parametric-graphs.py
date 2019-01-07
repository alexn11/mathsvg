
import mathsvg


import math

image = mathsvg . SvgImage ("parametric-graphs.svg", rescaling = 100, shift = [ 1.1, 1.5 ])
image . set_view_box ((360, 300))

x = lambda t : math . sin (10 * math . pi * t) + 0.1
y = lambda t : math . cos (6 * math . pi *  t)
image . set_svg_options (stroke_color = "black")
image . draw_parametric_graph (x, y, 0, 1, 40, curve_type = "autosmooth", is_closed = False)
image . set_svg_options (stroke_color = "blue")
image . draw_parametric_graph (x, y, 0, 1, 40, curve_type = "polyline", is_closed = False)


x = lambda t : math . sin (6 * math . pi * t) + 1.1
y = lambda t : math . cos (10 * math . pi * t)
image . set_svg_options (stroke_color = "red")
image . set_dash_mode ("none")
image . draw_parametric_graph (x, y, 0, 1, 400, curve_type = "polyline", is_closed = True)
image . set_svg_options (stroke_color = "black")
image . set_dash_mode ("dot")
image . draw_parametric_graph (x, y, 0, 1, 40, curve_type = "autosmooth", is_closed = True)




image . save ()

