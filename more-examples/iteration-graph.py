# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2021-06-09
# Copyright (C) 2021 Alexandre De Zotti
# License: MIT License

import math
import mathsvg

# ---------------------------------------------------------------------

frame_stroke_w = 3
diags_stroke_w = 2
graph_stroke_w = 4
iterations_stroke_w = 3
axes_arrow_rel_size = 1.5
iteration_arrow_rel_size = 0.7

r = 4.
x0 = 0.10491
n = 6
spacing = 0.1

# ---------------------------------------------------------------------

def eval_logistic_map(r, x):
  return r * x * (1 - x)


def draw_frame(g):
  g.set_dash_mode("none")
  g.set_svg_options(stroke_width=frame_stroke_w, units='svg')
  g.set_arrow_options(width = axes_arrow_rel_size * arrow_size, units='svg')
  g.draw_arrow((0, 0), (1 + 0.5 * spacing, 0))
  g.draw_arrow((0, 0), (0, 1 + 0.5 * spacing))
  g.set_dash_mode("dash")
  g.set_svg_options(stroke_width=diags_stroke_w, units='svg')
  g.draw_line_segment((0, 0), (1, 1))
  

def draw_graph(g, eval_map_function):
  g.set_dash_mode("none")
  g.set_svg_options(stroke_width=graph_stroke_w, units='svg')
  g.draw_function_graph(eval_map_function, 0, 1, 50)
  
def draw_iterations(g, eval_map_function, x0, n):

  def draw_mid_point_arrows(x, x_next, both=True):
    if(x_next > x):
      arrow_direction_angles = (0.5*math.pi, 0)
    else:
      arrow_direction_angles = (-0.5*math.pi, math.pi)
    g.draw_arrow_tip((x, mid_value), arrow_direction_angles[0])
    if(both):
      g.draw_arrow_tip((mid_value, x_next), arrow_direction_angles[1])

  xs = [ x0 ]
  for i in range(n):
    xs.append(eval_map_function(xs[-1]))

  g.set_dash_dash_structure(12, 4, units='svg')
  g.set_dash_mode("dash")
  g.set_svg_options(stroke_width=iterations_stroke_w, units='svg')
  g.set_arrow_options(width = iteration_arrow_rel_size * arrow_size, curvature = 0, units='svg')
  g.set_point_size(0.01)

  g.draw_line_segment((x0, 0), (x0, x0))
  for i, x in enumerate(xs[:-2]):
    x_next = xs[i+1]
    g.draw_polyline([(x, x), (x, x_next), (x_next, x_next)])
    mid_value = 0.5 * (x + x_next)
    draw_mid_point_arrows(x, x_next)
  g.draw_polyline([ (xs[-2], xs[-2]), (xs[-2], xs[-1]) ])
  g.draw_point((xs[-2], xs[-1]))
  draw_mid_point_arrows(xs[-2], xs[-1], both=False)
  g.reset_dash_and_dot_structures()

# ---------------------------------------------------------------------

eval_map = lambda x : eval_logistic_map(r, x)


graph = mathsvg.SvgImage(pixel_density=600, view_window=((0-spacing, 0-spacing),(1+spacing, 1+spacing)))
arrow_size = graph.arrow_width_svgpx

draw_frame(graph)
draw_graph(graph, eval_map)
draw_iterations(graph, eval_map, x0, n)

graph.save('iteration-graph.svg')

