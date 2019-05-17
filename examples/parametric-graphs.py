
import mathsvg


import math

image = mathsvg . SvgImage (rescaling = 100, shift = [ 1.1, 1.5 ], view_box = (360, 360))

graph_function = lambda t : (math . sin (10 * math . pi * t) + 0.1, math . cos (6 * math . pi *  t))
image . set_svg_options (stroke_color = "black")
image . draw_parametric_graph (graph_function, 0, 1, 40, curve_type = "autosmooth", is_closed = False)
image . set_svg_options (stroke_color = "blue")
image . draw_parametric_graph (graph_function, 0, 1, 40, curve_type = "polyline", is_closed = False)


graph_function = lambda t : (math . sin (6 * math . pi * t) + 1.1, math . cos (10 * math . pi * t))
image . set_svg_options (stroke_color = "red")
image . set_dash_mode ("none")
image . draw_parametric_graph (graph_function, 0, 1, 400, curve_type = "polyline", is_closed = True)
image . set_svg_options (stroke_color = "black")
image . set_dash_mode ("dot")
image . draw_parametric_graph (graph_function, 0, 1, 40, curve_type = "autosmooth", is_closed = True)


image . save ("parametric-graphs.svg")

