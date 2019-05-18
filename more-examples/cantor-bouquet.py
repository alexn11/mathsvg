# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2019-05-18
# Copyright (C) 2019, Alexandre De Zotti
# License: MIT License


import sys
import math

import cmath

import mathsvg



smallest_interval = 0.0003
density = 0.5
max_length = 1.


allowed_object_types = [ "disconnected-straight-brush", "compact-cantor-bouquet", "one-sided-hairy-circle" ]



def print_help_and_leave ():
  print ("\nUsage:\n")
  print ("> " + sys . argv [0] + " object-type " + " --smallest-interval float --density float --max-length float")
  print ("\nObject type must one of these: " + str (allowed_object_types) + "\n")
  sys . exit ()



object_type = allowed_object_types [0]
if (len (sys . argv) > 1):
  object_type = sys . argv [1]


if (object_type not in allowed_object_types):
  if (sys . argv [1] == "--help"):
    print_help_and_leave ()
  message = "Object type should be one from: "
  for object_type in allowed_object_types:
    message += object_type +  ", "
  print (message)
  raise Exception ("Wrong command line argument")




if (len (sys . argv) > 2):
  argc = len (sys . argv)
  arg_index = 2
  while (arg_index < argc):
    if (sys . argv [arg_index] == "--smallest-interval"):
      smallest_interval = float (sys . argv [arg_index + 1])
      arg_index += 2
    elif (sys . argv [arg_index] == "--density"):
      density = float (sys . argv [arg_index + 1])
      arg_index += 2
    elif (sys . argv [arg_index] == "--max-length"):
      max_length = float (sys . argv [arg_index + 1])
      arg_index += 2
    elif (sys . argv [arg_index] == "--help"):
      print_help_and_leave ()
      arg_index += 1





def generate_intermediate_lengths (left_element, right_element, smallest_interval, density):
  lengths = []

  left_x = left_element [0]
  left_length = left_element [1]
  right_x = right_element [0]
  right_length = right_element [1]
  width = right_x - left_x
  next_width = density * width

  while (abs (next_width) > smallest_interval):
    next_x = left_x + next_width
    next_length = (next_width * left_length + (width - next_width) * right_length) / width
    lengths . append (( next_x, next_length, True ))
    right_x = next_x
    right_length = next_length
    width = next_width
    next_width = density * width


  if (width > 0):
   lengths . reverse ()
  #print (lengths)

  return lengths


def compute_lengths (max_length, smallest_interval, density, max_level = 188):

  # last coordinate indicate if an intermediate length can fit in between (given the smallest_interval restriction)

  level = 0
  left_element = (0., max_length, True)
  right_element = (1., max_length, True)
  lengths_list = [ left_element, right_element ]


  while (level < max_level):

    next_level = level + 1
    left_index = 0
    right_index = 1
    interval_count = 0


    while (left_index < len (lengths_list) - 1):

        right_index = left_index + 1
        left_element = lengths_list [left_index]
        right_element = lengths_list [right_index]

        if ((not left_element [2]) and (not right_element [2])):
          left_index = right_index
        else:
          interval_count += 1
          middle_coordinate = 0.5 * (right_element [0] + left_element [0])
          middle_element = (middle_coordinate, 0, True)
          new_lengths_list = generate_intermediate_lengths (left_element, middle_element, smallest_interval, density)
          new_lengths_list += (generate_intermediate_lengths (right_element, middle_element, smallest_interval, density))
          if (len (new_lengths_list) == 0):
             lengths_list [left_index] = (lengths_list [left_index] [0], lengths_list [left_index] [1], False)
             lengths_list [right_index] = (lengths_list [right_index] [0], lengths_list [right_index] [1], False)
             left_index = right_index
          else:
            lengths_list = lengths_list [ : left_index + 1 ] + new_lengths_list + lengths_list [ right_index : ]
            left_index = right_index + len (new_lengths_list)


    if (interval_count == 0):
      break



  return lengths_list






image_name = object_type + ".svg"
image_main_scale = 800
padding = 0.1




lengths = compute_lengths (max_length, smallest_interval, density)

#print (lengths)

if (object_type == "disconnected-straight-brush"):
  view_window = ((-padding, -padding), (1 + padding, 1 + padding))
  image = mathsvg . SvgImage (pixel_density = image_main_scale, view_window = view_window)
  for element in lengths:
    image . draw_line_segment ( [ element [0], 0 ], [ element [0], element [1] ] )
elif (object_type == "compact-cantor-bouquet"):
  view_window = ((-1 - padding, -1 - padding), (1 + padding, 1 + padding))
  image = mathsvg . SvgImage (pixel_density = image_main_scale, view_window = view_window)
  for element in lengths:
    endpoint = element [1] * cmath . exp (2. * math . pi * element [0] * 1.j)
    image . draw_line_segment ( [ 0, 0 ], [ endpoint. real, endpoint . imag ] )
elif (object_type == "one-sided-hairy-circle"):
  view_window = ((-1 - padding, -1 - padding), (1 + padding, 1 + padding))
  image = mathsvg . SvgImage (pixel_density = image_main_scale, view_window = view_window)
  image . draw_circle ( (0, 0), 0.5)
  for element in lengths:
    direction = cmath . exp (2. * math . pi * element [0] * 1.j)
    start_point  = 0.5 * direction
    endpoint = start_point + 0.5 * element [1] * direction
    image . draw_line_segment ( [ start_point . real, start_point . imag ], [ endpoint. real, endpoint . imag ] )


image . save (image_name)
















