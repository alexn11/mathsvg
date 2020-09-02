# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2019-05-18
# Copyright (C) 2019, 2020 Alexandre De Zotti
# License: MIT License


import math
import cmath
import mathsvg

two_pi = 2. * math.pi

# ------ parameters ----------------------------------------------------------------------------------------------------

image_size = 800
nb_levels = 9

start_size = 1.
rescaling_factor = 0.48 # normally should be less than 1/2, but a priori not forbidden
corner_turn = - 1. / 12.

do_draw_intermediate_levels = False
do_draw_centers = False

#triangle_rotation = 1 / 49.

# --- below are treated as global variables, the angle (corner_turn) could theoretically be a parameter as well ---------

bottom = -0.75
left = -1.
view_window = ((left, bottom), (left + 2, bottom + 2))

drawings_fill_color = "lightgreen"
drawings_stroke_color = "orangered"

"""
drawings_fill_color = "gold"
drawings_stroke_color = "goldenrod"
"""

centers_relative_distance_to_center = 1 - rescaling_factor

turn_direction = cmath.exp(two_pi * corner_turn * 1.j)
#rotation_direction = cmath.exp(two_pi * triangle_rotation * 1.j)

up_vector = [ 0., 1. ]
right_vector = [ turn_direction.real, turn_direction.imag ]
left_vector = [ - right_vector[0], right_vector[1] ] 

"""

up_vector = rotate_vector(rotation_direction, up_vector)
right_vector = rotate_vector(rotation_direction, right_vector)
left_vector = rotate_vector(rotation_direction, left_vector)
"""

centers_relative_positions = [
    [ up_vector[0] * centers_relative_distance_to_center, up_vector[1] * centers_relative_distance_to_center ],
    [ left_vector[0] * centers_relative_distance_to_center, left_vector[1] * centers_relative_distance_to_center ],
    [ right_vector[0] * centers_relative_distance_to_center, right_vector[1] * centers_relative_distance_to_center ], ]
# --- -------------------------------------------------------------------------------------------------------------------

"""
def rotate_vector(rotation_direction, vector):
  return [ vector[0] * rotation_direction.real - vector[1] * rotation_direction.imag,
           vector[0] * rotation_direction.imag + vector[1] * rotation_direction.real ]
"""

def compute_next_size(current_size, rescaling_factor):
  return current_size * rescaling_factor

def compute_next_centers_relative(current_size, next_size): #, rotation_direction):
  centers = [ [ current_size * x for x in c ] for c in centers_relative_positions ]
  return centers
  # return [ rotate_vector(rotation_direction, c) for c in centers ]

def compute_next_centers(current_center, next_centers_relative):
  return [ [ c[0] + current_center[0], c[1] + current_center[1] ] for c in next_centers_relative ]

def compute_triangle_vertexes(center, size):
  return [
    [ up_vector[i] * size + center[i] for i in range(2) ],
    [ left_vector[i] * size + center[i] for i in range(2) ],
    [ right_vector[i] * size + center[i] for i in range(2) ], ]

def draw_triangle(image, center, size):
  vertexes = compute_triangle_vertexes(center, size)
  image.draw_polyline(vertexes + [ vertexes[0], ])
  return



def draw_triforce(image, start_size, rescaling_factor, nb_levels):

  size = start_size
  centers = [ [ 0, 0 ], ]

  for level in range(nb_levels - 1):
    next_size = compute_next_size(size, rescaling_factor)
    next_centers_relative_positions = compute_next_centers_relative(size, next_size) #, rotation_direction)
    next_centers = []
    for center in centers:
      if(do_draw_centers): # debugging
        image.set_svg_options(stroke_color = "red")
        image.draw_cross(center)
        image.set_svg_options(stroke_color = drawings_stroke_color)
      #
      if(do_draw_intermediate_levels):
        draw_triangle(image, center, size)
      next_centers += compute_next_centers(center, next_centers_relative_positions)
    size = next_size
    centers = next_centers

  # last level doesn't need to compute next centers etc.
  for center in centers:
    if(do_draw_centers): # debugging
      image.set_svg_options(stroke_color = "red")
      image.draw_cross(center)
      image.set_svg_options(stroke_color = "black")
    #
    draw_triangle(image, center, size)

  return

image = mathsvg.SvgImage(pixel_density = image_size / 2, view_window = view_window)

image.set_svg_options(fill_color = drawings_fill_color, stroke_color = drawings_stroke_color)
draw_triforce(image, start_size, rescaling_factor, nb_levels)

image.save("selfsim-triforce.svg")



