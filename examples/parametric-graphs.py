import math
import mathsvg


def a_function_with_one_parameter (t, r):
  return (r * math . cos (2. * math . pi * t), r * math . sin (2. * math . pi * t))



image = mathsvg . SvgImage (pixel_density = 100, view_window = ((-1.1, -1.5), (2.5, 2.1)))

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


image . set_dash_mode ("none")
image . reset_svg_options ()
radius = .5
image . draw_parametric_graph (a_function_with_one_parameter, 0., 1., 22, radius, curve_type = "autosmooth", is_closed = True)
radius = .25
image . draw_parametric_graph (a_function_with_one_parameter, 0., 1., 22, radius, curve_type = "autosmooth", is_closed = True)


image . save ("parametric-graphs.svg")

