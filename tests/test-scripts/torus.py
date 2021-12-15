# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, 2020, Alexandre De Zotti
# License: MIT License


import math
import cmath
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.pardir))
import mathsvg

two_pi = 2 * math.pi
rescaling = 100


def draw_a_torus(image, torus_position, torus_size, thinness = 0.375):
  # NOTE: there's limits to acceptable thinness beyond which the computations will produce an error
  # TODO: check that thinness is within the right bounds
  r = torus_size
  a = r / 2
  b = 5 * a / 8
  d = math.sqrt(a * a - b * b)

  focuses = [ [- d, 0], [d, 0] ]
  focuses = [ [ f[0] + torus_position[0], f[1] + torus_position[1] ] for f in focuses ]
  image.draw_ellipse(focuses, b)

  small_ellipses_factor = thinness
  a *= small_ellipses_factor
  b *= small_ellipses_factor
  d *= small_ellipses_factor
  shift_factor = 1 / 20
  ellipse_shift = shift_factor * r

  focuses = [ [- d, ellipse_shift], [d, ellipse_shift] ]
  focuses = [ [ f[0] + torus_position[0], f[1] + torus_position[1] ] for f in focuses ]
  image.draw_ellipse_arc(focuses, b, math.pi, two_pi)

  focuses = [ [- d, - ellipse_shift], [d, - ellipse_shift] ]
  focuses = [ [ f[0] + torus_position[0], f[1] + torus_position[1] ] for f in focuses ]
  angle_start = math.asin(ellipse_shift / b)

  image.draw_ellipse_arc(focuses, b, angle_start, math.pi - angle_start)




image = mathsvg.SvgImage(pixel_density = rescaling, view_window = ((-4, -4), (4, 4)))

draw_a_torus(image, [0, 0], 6.2)

draw_a_torus(image, [3.1,-2.2], 0.63)
draw_a_torus(image, [2.07,-2.7], 0.63)
draw_a_torus(image, [2.81,-3.01], 0.63)

draw_a_torus(image, [2.5, 2.5], 1.3, thinness = 0.8)
draw_a_torus(image, [-2.5, 2.5], 1.3, thinness = 0.2)

image.set_dash_mode("dash")
draw_a_torus(image, [-2.9,-2.2], 1.78, thinness = 0.35)

image.save("torus.svg", do_overwrite = True)

