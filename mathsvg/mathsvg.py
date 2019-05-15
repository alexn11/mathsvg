# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License


"""
.. module:: mathsvg

.. moduleauthor:: Alexandre De Zotti <alexn11.gh@gmail.com>


"""


import math
import cmath
import random

import svgwrite


# The Fundamental Constant of the mathematical universe:
the_tau = 2 * math . pi



# note: not checking any of the parameters

class SvgImage:
  """
  Main class used for creating SVG images.

  In order to make SVG graphics using mathsvg, you need first to create an instance of SvgImage. Then do your drawings by calling a few members functions of this object. Finally call ``save ()`` to save the result.

  The constructor requires a path or file name for the SVG.

  The optional parameters of the constructor are ``rescaling`` (nonzero floating point number), ``shift`` (list of two floating point numbers),d ``view_box`` (tuple of two integers) and ``image_file_name`` (string).

  The parameters ``rescaling`` and ``shift`` cannot be modified because they need to be consistent for all the drawings.

  The parameters ``view_box`` can be modified with the method ``set_view_box`` and ``image_file_name`` can be passed as a parameter to the method ``save``."""

  def __init__ (self, rescaling = 1., shift = [0, 0], file_name = None, view_box = (500, 500)):

    self . image_file_name = file_name
    self . svgwrite_object = svgwrite . Drawing (filename = "None" if (file_name is None) else file_name, debug = True) #, size = (u'1000%', u'1000%'))

    self . _set_view_box_no_reset (view_box)
    self . reset_svg_options ()
    self . point_size = 6 * self . stroke_width

    # old temporary back compatiblity hack (to remove) ----------------------
    if ((type (rescaling) is list) or (type (rescaling) is tuple)):
      raise Exception ("obsolete rescaling parameter type")
      if (rescaling [0] != rescaling [1]):
        raise Exception ("Now is not compatible with nonconformal rescaling")
      rescaling = rescaling [0]
    # -----------------------------------------------------------------------

    self . rescaling = rescaling
    self . shift = shift

    self . reset_dash_and_dot_structures ()
    self . reset_arrow_options ()

    self . set_dash_mode ("none")



  def set_dash_mode (self, mode):
    """Choose the type of stroke.

    Args:
      * ``mode`` (``str``): the type of stroke, should be either ``"none"`` (solid line), ``"dash"``, ``"dot"`` (or ``"dots"``) or ``"dasharray"`` (customized dash/dot, see SVG specifications for more details on dash arrays)

    Example (see also :ref:`lines.py`, :ref:`dashes.py`, :ref:`more-curved-arrows.py`, :ref:`torus.py`, :ref:`points-crosses-circles-ellipses.py`, :ref:`arrows.py`, :ref:`curved-arrows.py`, :ref:`potato-regions.py`)::

      image = mathsvg . SvgImage (file_name = "example.svg", rescaling = 20, shift = [ 4, 4 ])

      image . set_dash_mode ("dash")
      image . draw_line_segment ([0, 0], [10, 10])

      image . set_dash_mode ("dot")
      image . draw_line_segment ([0, 10], [10, 0])

      image . set_svg_options (dash_array = [18, 3, 1, 3, 7, 3, 1, 3])
      image . set_dash_mode ("dasharray")
      image . draw_planar_potato ([5, 5], 2, 4, 8)

      image . save ()
    """

    if (mode not in ("none", "dash", "dot", "dots", "dasharray")):
      raise Exception ("set_dash_mode mode not in ('none', 'dash', 'dot', 'dasharray')")
    self . dash_mode = mode


  def _set_view_box_no_reset (self, view_box):
    self . svgwrite_object . viewbox (width = view_box [0], height = view_box [1])
    self . view_box = view_box


  def set_view_box (self, view_box):
    """Sets the size of the SVG canvas

    Args:
      * ``view_box`` (``tuple``): tuple of integers corresponding to the size in pixels of the SVG in the x and y directions
    """

    self . svgwrite_object . viewbox (width = view_box [0], height = view_box [1])
    self . view_box = view_box
    # this will not be retroactive:
    self . reset_dash_and_dot_structures ()
    self . reset_arrow_options ()



  def set_dash_dash_structure (self, black_len, white_len):
    """Sets the size of the dashes and space for the dash mode

    Args:
      * ``black_len`` (``int`` or ``float``): length of the dash in pixels
      * ``white_len`` (``int`` or ``float``): length of the space between dashes in pixels
    """

    self . dash_dasharray = (black_len, white_len)
    

  def set_dash_dot_structure (self, dot_sep):
    """Sets the separations between dots for dotted stroke

    Args:
      * ``dot_sep`` (``int`` or ``float``): separation between the dots in pixels
    """

    self . dot_dasharray = (self . stroke_width, dot_sep)

 
  def reset_svg_options (self):
    """Sets the stroke color to ``"black"``, the stroke width to ``1`` pixel and the fill color to ``"none"``."""

    self . set_svg_options (stroke_color = "black", stroke_width = 1, fill_color = "none")


  def _compute_a_smallish_size (self):
    return min (self . view_box) / 50

  def reset_dash_and_dot_structures (self):
    """Sets the dash, dot and dasharray structures to default values depending on the size of the canvas."""

    dash_len = self . _compute_a_smallish_size ()
    dot_sep = max ((dash_len / 2, 2 * self . stroke_width))
    self . set_dash_dash_structure (dash_len, dash_len)
    self . set_dash_dot_structure (dot_sep)
    self . dasharray_dasharray = [ dash_len, 1 ]


  def reset_arrow_options (self):
    """Sets the width, opening angle and curvature of arrows to default values depending eventually on the size of the canvas."""

    self . arrow_width = self . _compute_a_smallish_size ()
    self . arrow_opening_angle = 0.12 * math . pi
    self . arrow_curvature = 0.14

  def set_arrow_options (self, width = None, opening_angle = None, curvature = None):
    """Sets some values governing the shape and geometry of the arrows.

    Args:
      * ``width`` (``float`` or ``None``): width for the stroke of arrows
      * ``opening_angle`` (``float`` or ``None``): opening angle of the arrow tip
      * ``curvature`` (``float`` or ``None``): curving for the back of the tip of the arrow, ``0`` for a straight arrow tip

    Examples (see also :ref:`arrows.py`)::
      
      image = mathsvg . SvgImage (file_name = "example.svg", rescaling = 20, shift = [ 4, 4 ])

      image . set_arrow_options (curvature = 0.55)
      image . draw_arrow ([ -2, -2 ], [ 2, 1.7 ])

      image . set_arrow_options (width = 4 * image . arrow_width)
      image . draw_arrow ([ -2, -2 ], [ 2, 1.2 ])

      image . reset_arrow_options ()
      image . set_arrow_options (curvature = 0)
      image . draw_arrow ([ -2, -2 ], [ 2, 0.6 ])

      image . save ()
    """

    if (width is not None):
      self . arrow_width = width
    if (opening_angle is not None):
      self . opening_angle = opening_angle
    if (curvature is not None):
      self . arrow_curvature = curvature

  
  def set_svg_options (self, stroke_color = None, stroke_width = None, fill_color = None, dash_array = None):
    """Sets the stroke width, color, fill color and dash array options

    Args:
      * ``stroke_color`` (``str`` or ``None``): stroke color (default is ``"black"``)
      * ``stroke_width`` (``float`` or ``None``): stroke width in pixels
      * ``fill_color`` (``str`` or ``None``): fill color (default is ``"none"``)
      * ``dash_array`` (``list`` or ``None``): list of stroke/space lengths (in pixels) describing the customize dash stroke

    Examples:
    To do some drawings in red, then restore back to the default options::

      image . set_svg_options (stroke_color = "red")
      (etc.)
      image . reset_svg_options ()
    """

    if (stroke_color is not None):
      self . stroke_color = stroke_color
    if (stroke_width is not None):
      self . stroke_width = stroke_width
    if (fill_color is not None):
      self . fill_color = fill_color
    if (dash_array is not None):
      self . dasharray_dasharray = dash_array [:]



  def save (self, file_name = None):
    """Save the drawings into a SVG file. 

        If no path/name is given, the file name given as a parameter to the constructor will be used.
        Meanwhile if no name was given to the constructor an exception is raised.

        If a path/name is given will use this as the path/name of the file to save the drawings.

        See an example in :ref:`multiple-save.py`"""

    if (file_name is None):
      if (self . image_file_name is None):
        raise Exception ("Save: no file name given!")
      self . svgwrite_object . save ()
    else:
      self . svgwrite_object . saveas (file_name)



  def _flip_point (self, point):
    return [ point [0], self . view_box [1] - point [1] ]



  def _flip_vector (self, vector):
    return [ vector [0], - vector [1] ]



  def _rescale_vector (self, vector):
    return [ self . rescaling * vector [0], self . rescaling * vector [1] ]
    # previous nonconformal version:
    #return [ self . rescaling [0] * vector [0], self . rescaling [1] * vector [1] ]


  def _rescale_length (self, length):
    # this assumes conformal projection
    return length * self . rescaling


  def _shift_point (self, point):
    return [ point [0] + self . shift [0], point [1] + self . shift [1] ]



  def project_point_to_canvas (self, point):
    """Compute the coordinate of a point on the SVG canvas (first translates by ``shift`` then rescales by ``rescaling``)."""
    return self . _flip_point ( self . _rescale_vector (self . _shift_point (point)))



  def project_complex_point_to_canvas (self, z):
    """Compute the coordinates of a complex number projected onto the SVG canvas (equivalent to ``project_point_to_canvas ([ z . real, z . imag ])``)."""
    return self . project_point_to_canvas ([ z . real, z . imag ])



  def project_vector_to_canvas (self, vector):
    """Compute the coordinates of a vector attached at 0 on the SVG canvas (rescaling without translation)."""
    return self . _flip_vector (self . _rescale_vector (vector))



  def project_complex_vector_to_canvas (self, dz):
    """Compute the coordinates of a complex vector attached at 0 on the SVG canvas (rescaling without translation)."""
    return self . project_vector_to_canvas ([ dz . real, dz . imag ])


  def _convert_point_to_svg_string (self, point):
    # control vectors are points too
    return str (point [0]) + ", " + str (point [1])


  def _make_svg_path_M_command (self, points):
    path_command = " M "
    for point in points:
      path_command += self . _convert_point_to_svg_string (point) + "  "
    return path_command

  def _make_svg_path_L_command (self, points):
    path_command = " L "
    for point in points:
      path_command += self . _convert_point_to_svg_string (point) + "  "
    return path_command
 

  def _make_svg_path_C_command (self, points, control_vectors):

    nb_points = len (points)

    path_command = " C "

    control_vector_index = 0
    for point_index in range (nb_points):
      path_command += " " + self . _convert_point_to_svg_string (control_vectors [control_vector_index])
      control_vector_index += 1
      path_command += " " + self . _convert_point_to_svg_string (control_vectors [control_vector_index])
      control_vector_index += 1
      path_command += " " + self . _convert_point_to_svg_string (points [point_index]) + "  "
  
    return path_command


  def _make_svg_path_M_and_C_command (self, points, control_vectors):

    path_command = self . _make_svg_path_M_command (points [ 0 : 1 ])
    path_command += self . _make_svg_path_C_command (points [ 1 : ], control_vectors)

    return path_command


  
  def _make_svg_path_Z_command (self):
    return " Z "   


  def _make_svg_dasharray_string (self, dash_mode = None):
    if (dash_mode is None):
      dash_mode = self . dash_mode

    dash_array_string = "stroke-dasharray : "
    if (dash_mode == "none"):
      dash_array_string += "none"
    elif (dash_mode == "dash"):
      dash_array_string += str (self . dash_dasharray [0]) + ", " + str (self . dash_dasharray [1])
    elif (dash_mode in [ "dot", "dots" ]):
      dash_array_string += str (self . dot_dasharray [0]) + ", " + str (self . dot_dasharray [1])
    elif (dash_mode == "dasharray"):
      for length in self . dasharray_dasharray:
        dash_array_string += str (length) + ", "
      dash_array_string = dash_array_string [ : -2 ]
    else:
      dash_array_string += "YOUFAILED"
    dash_array_string += ";"
    return dash_array_string
  

  def _make_svg_style_string (self,
                              fill_color = None,
                              stroke_color = None,
                              stroke_width = None,
                              dash_mode = None):
    if (fill_color is None):
      fill_color = self . fill_color
    if (stroke_color is None):
      stroke_color = self . stroke_color
    if (stroke_width is None):
      stroke_width = self . stroke_width
    if (dash_mode is None):
      dash_mode = self . dash_mode
    style = ""
    style += "fill : " + str (fill_color) + "; "
    style += "stroke : " + str (self . stroke_color) + "; "
    style += "stroke-width : " + str (self . stroke_width) + "; "
    style += self . _make_svg_dasharray_string (dash_mode)
    return style


  def draw_arrow_tip (self, tip, arrow_direction_angle):
    """Draw the tip of an arrow.

    Args:
      * ``tip`` (``list``): position of the tip
      * ``arrow_direction_angle`` (``float``): angle where the arrow is pointing in radians

    Examples: see :ref:`arrows.py`
    """

    tip_position = self . project_point_to_canvas (tip)

    size = self . arrow_width
    opening_angle = self . arrow_opening_angle
    curvature = self . arrow_curvature

    tan_opening = math . tan (opening_angle)
    semi_height = size * tan_opening
    inner_coordinate = size * (1 - curvature)
    top_point = [ size, semi_height ]
    bottom_point = [ size, - semi_height ]
    middle_point = [ inner_coordinate, 0 ]
    control_height = 0.5 * inner_coordinate * tan_opening
    control_vector_top = [ inner_coordinate, control_height ]
    control_vector_bottom = [ inner_coordinate, - control_height ]
    tip_point = [ 0, 0 ]
    path_command = self . _make_svg_path_M_command ([ top_point, tip_point, bottom_point ] )
    path_command += self . _make_svg_path_C_command ([ middle_point, top_point ],
                                                    [ bottom_point, control_vector_bottom, control_vector_top, top_point ])
    path_command += self . _make_svg_path_Z_command ()
    path = self . svgwrite_object . path (d = path_command,
                                          style = self . _make_svg_style_string (fill_color = self . stroke_color, dash_mode = "none"))
    # be wary of that featured bug that reverse the order of the transformations
    path . translate (tip_position)
    path . rotate (math . degrees (math . pi - arrow_direction_angle), center = [ 0, 0 ]) # also: angles are negative
    # 
    self . svgwrite_object . add (path)


  def _compute_line_angle (self, start_point, end_point):
    direction = end_point [0] - start_point [0] + 1j * (end_point [1] - start_point [1])
    return cmath . phase (direction)


  def draw_straight_arrow  (self, start_point, end_point):
    """Draws an arrow as a straight line segment between two points and an arrow tip at the last point.

     Equivalent to ``self . draw_arrow (start_point, end_point)``.

    Args:
      * ``start_point`` (``list``): coordinates of where the arrow starts
      * ``end_point`` (``list``): coordinates of where the arrow ends
    """

    self . draw_line_segment (start_point, end_point)
    self . draw_arrow_tip (end_point, self . _compute_line_angle (start_point, end_point))


  def _compute_curved_arrow_endpoint_tangent (self, arrow_body_point_list, control_vectors):
    broken_line_tangent = self . _compute_line_angle (arrow_body_point_list [-2], arrow_body_point_list [-1])
    control_vector_line_tangent = self . _compute_line_angle (control_vectors [-2], arrow_body_point_list [-1])
    return - control_vector_line_tangent

  def _compute_curved_arrow_control_vectors (self, arrow_body_point_list):
    # this is general not assuming exactly three points in the body of the arrow
    return self . _compute_autosmooth_control_vectors (arrow_body_point_list, vectors_relative_size = 0.6)
    


  def draw_curved_arrow  (self, start_point, end_point, curvedness = 0.25, asymmetry = 0.):
    """Draws an arrow as a curved line joining two points with an arrow tip at the last point.

    Args:
      * ``start_point`` (``list``): coordinates of where the arrow starts
      * ``end_point`` (``list``): coordinates of where the arrow ends
      * ``curvedness`` (``float`` or ``None``): height of the bump making the arrow curve (0 for a straight arrow)
      * ``asymmetry`` (``float`` or ``None``): where the bump should be located: 0 is the middle, negative: towards the first point, positive: towards the last point. A value between -0.5 and 0.5 guarantees that the bump is between the two end points.

    Examples (see also: :ref:`curved-arrows.py` and :ref:`more-curved-arrows.py`)::

      image = mathsvg . SvgImage (file_name = "curved-arrows.svg", rescaling = 100, shift = [ 4, 4 ])
      image . set_view_box ((800, 800))

      image . draw_curved_arrow ([ -2, -1 ], [ 2, -1 ], curvedness = -.2)
      image . draw_curved_arrow ([ -2.7, 2 ], [ -0.3, 2 ], asymmetry = - 0.8)
      image . draw_curved_arrow ([ -2.7, 1 ], [ -0.3, 1 ], asymmetry = - 0.2)
      image . draw_curved_arrow ([ -2.7, 0 ], [ -0.3, 0 ], asymmetry = 0.2)
      image . draw_curved_arrow ([ -2.7, -1 ], [ -0.3, -1 ], asymmetry = 0.5)
      image . draw_curved_arrow ([ -2.7, -2 ], [ -0.3, -2 ], curvedness = -0.2, asymmetry = 1.2)

      image . save ()
    """

    direction = [ end_point [i] - start_point [i] for i in range (2) ]
    orthogonal_direction = [ - direction [1], direction [0] ]
    middle_point = [ (0.5 - asymmetry) * start_point [i] + (0.5 + asymmetry) * end_point [i] for i in range (2) ]
    intermediate_point = [ middle_point [i] + curvedness * orthogonal_direction [i] for i in range (2) ]

    arrow_body_point_list = [ self . project_point_to_canvas (p) for p in ( start_point, intermediate_point, end_point ) ] 
    control_vectors = self . _compute_curved_arrow_control_vectors (arrow_body_point_list)
    path_command = self . _make_svg_path_M_and_C_command (arrow_body_point_list, control_vectors)
    self . insert_svg_path_command (path_command)
    arrow_direction_angle = self . _compute_curved_arrow_endpoint_tangent (arrow_body_point_list, control_vectors)
    # note: here we need conformal projection
    self . draw_arrow_tip (end_point, arrow_direction_angle)
    return


 



  def draw_arrow (self, start_point, end_point, curvedness = 0., asymmetry = 0.):
    """Draws either a straight or curved arrow.

    Args:
      * ``start_point`` (``list``): coordinates of where the arrow starts
      * ``end_point`` (``list``): coordinates of where the arrow ends
      * ``curvedness`` (``float`` or ``None``): height of the bump making the arrow curve, if is ``None`` then will draw a straight arrow (``asymmetry`` will be ignored)
      * ``asymmetry`` (``float`` or ``None``): where the bump should be located: ``0`` is the middle, negative: towards the first point, positive: towards the last point. A value between ``-0.5`` and ``0.5`` guarantees that the bump is between the two end points.

    Examples: see :ref:`graphs.py`, :ref:`arrows.py`
    """

    if (curvedness == 0):
      self . draw_straight_arrow (start_point, end_point)
    else:
      self . draw_curved_arrow (start_point, end_point, curvedness, asymmetry)




  def draw_point (self, position):
    """Draws a small circle.

    Args:
      * ``position`` (``list``): position of the center of the circle

    Examples: see :ref:`points-crosses-circles-ellipses.py`
    """

    point = svgwrite . shapes . Circle (self . project_point_to_canvas (position),
                                        r = self . point_size,
                                        style = self . _make_svg_style_string (fill_color = self . stroke_color, dash_mode = "none"))
    self . svgwrite_object . add (point)


  def draw_cross (self, position):
    """Draws a small X cross.

    Args:
      * ``position`` (``list``): position of the center of the cross

    Examples: see :ref:`points-crosses-circles-ellipses.py`
    """

    center = self . project_point_to_canvas (position)
    x_min = center [0] - self . point_size
    x_max = center [0] + self . point_size
    y_min = center [1] - self . point_size
    y_max = center [1] + self . point_size
    style_string = self . _make_svg_style_string (dash_mode = "none")
    line = self . svgwrite_object . line  ([x_min, y_min], [x_max, y_max], style = style_string)
    self . svgwrite_object . add (line)
    line = self . svgwrite_object . line  ([x_max, y_min], [x_min, y_max], style = style_string)
    self . svgwrite_object . add (line)


  def draw_plus (self, position):
    """Draws a small + cross.

    Args:
      * ``position`` (``list``): position of the center of the cross

    Examples: see :ref:`points-crosses-circles-ellipses.py`
    """

    center = self . project_point_to_canvas (position)
    x_min = center [0] - self . point_size
    x_max = center [0] + self . point_size
    y_min = center [1] - self . point_size
    y_max = center [1] + self . point_size
    style_string = self . _make_svg_style_string (dash_mode = "none")
    line = self . svgwrite_object . line  ([x_min, center [1]], [x_max, center [1]], style = style_string)
    self . svgwrite_object . add (line)
    line = self . svgwrite_object . line  ([center [0], y_min], [center [0], y_max], style = style_string)
    self . svgwrite_object . add (line)



  def draw_line_segment (self, start_point, end_point):
    """Draws the line segment between two points.

    Args:
      * ``start_point`` (``list``): coordinates of the first end point of the line segment
      * ``end_point`` (``list``): coordinates of the second end point of the line segment

    Examples: see :ref:`lines.py`, :ref:`dashes.py`, :ref:`interpolated-curves.py`
    """

    #line = self . svgwrite_object . shapes . Line (start_point, end_point)
    line = self . svgwrite_object . line (self . project_point_to_canvas (start_point),
                                          self . project_point_to_canvas (end_point),
                                          style = self . _make_svg_style_string ())
    self . svgwrite_object . add (line)


  def _draw_svg_arc (self, start_point, end_point, start_angle, end_angle, major_axis_angle, radiuses):
    # abstract code factoring routine

    angle_difference = (end_angle - start_angle) % the_tau
    if (angle_difference < 0):
      arc_orientation = "+"
      angle_difference = - angle_difference
    else:
      arc_orientation = "-"
    is_a_large_arc = (angle_difference >= math . pi)

    x_axis_rotation = - math . degrees (major_axis_angle)

    path_command = self . _make_svg_path_M_command ([ start_point, ])

    path = svgwrite . path . Path (d = path_command,
                                   style = self . _make_svg_style_string ())

    path . push_arc (end_point,
                     x_axis_rotation,
                     radiuses,
                     large_arc = is_a_large_arc,
                     angle_dir = arc_orientation,
                     absolute = True)

    self . svgwrite_object . add (path)


  def draw_circle_arc (self, center, radius, start_angle, end_angle):
    """Draws an arc of a circle (in anticlockwise direction).

    Args:
      * ``center`` (``list``): coordinates of the center of the circle
      * ``radius`` (``float``): radius of the circle
      * ``start_angle`` (``float``): angle where the arc starts in radians
      * ``end_angle`` (``float``): angle where the arc ends in radians

    Examples: see :ref:`points-crosses-circles-ellipses.py`
    """

    arc_start_point = self . project_point_to_canvas ([ center [0] + radius * math . cos (start_angle),
                                                        center [1] + radius * math . sin (start_angle) ])
    arc_end_point = self . project_point_to_canvas ([ center [0] + radius * math . cos (end_angle),
                                                      center [1] + radius * math . sin (end_angle) ])
    radiuses_on_canvas = self . _rescale_vector ([ radius, radius ])

    self . _draw_svg_arc (arc_start_point, arc_end_point, start_angle, end_angle, 0, radiuses_on_canvas)

    return


  def _rescale_ellipse_radiuses (self, ellipse_radiuses):
    return [ self . _rescale_length (r) for r in ellipse_radiuses ]

  def draw_ellipse_arc (self, focuses, semi_minor_axis, start_angle, end_angle):
    """Draws an arc of an ellipse (in anticlockwise direction) with axis parallel to the x and y axis. The ellipse is parametrised in the form *"c + (a cos t, b sin t)"* where *t* varies from ``start_angle`` to ``end_angle`` (*a*, *b* and *c* are the parameters of the ellipse computed from the coordinates of the focuses and the semi minor axis). 

    Args:
      * ``focuses`` (``list``): list of two list of coordinates of the focuses of the ellipse
      * ``semi_minor_axis`` (``float``): semi minor axis
      * ``start_angle`` (``float``): angle where the arc starts in radians
      * ``end_angle`` (``float``): angle where the arc ends in radians

    Examples (see also :ref:`points-crosses-circles-ellipses.py` and :ref:`torus.py`)::

      import math
      #the_tau = 2. * math . pi

      import mathsvg

      image = mathsvg . SvgImage (file_name = "example.svg", rescaling = 100, shift = [ 4, 4 ])
      image . set_view_box ((800, 800))

      focuses = [ [-1.33, 0.61], [1.33, -0.61] ]

      image . draw_ellipse_arc (focuses, 0.412, the_tau * 0.1, the_tau * 0.8)
    
      image . save ()
    """

    # computing the ellipse parameters:
    complex_focuses = [ f [0] + 1j * f [1] for f in focuses ]
    major_axis_direction = complex_focuses [1] - complex_focuses [0]
    distance_between_the_focuses = abs (major_axis_direction)
    major_axis_direction /= distance_between_the_focuses
    half_distance_between_the_focuses = 0.5 * distance_between_the_focuses
    semi_major_axis = math . sqrt (semi_minor_axis * semi_minor_axis + half_distance_between_the_focuses * half_distance_between_the_focuses)
    middle_point = 0.5 * (complex_focuses [0] + complex_focuses [1])
    top_point = middle_point + semi_minor_axis * 1j * major_axis_direction
    right_point = middle_point + semi_major_axis * major_axis_direction

    start_point = middle_point + major_axis_direction * (semi_major_axis * math . cos (start_angle) + 1j * semi_minor_axis * math . sin (start_angle))
    end_point = middle_point + major_axis_direction * (semi_major_axis * math . cos (end_angle) + 1j * semi_minor_axis * math . sin (end_angle))

    # computing svg ellipse parameters:
    radiuses_on_canvas = self . _rescale_ellipse_radiuses ([semi_major_axis, semi_minor_axis])
    arc_start_point = self . project_complex_point_to_canvas (start_point)
    arc_end_point = self . project_complex_point_to_canvas (end_point)

    self . _draw_svg_arc (arc_start_point, arc_end_point, start_angle, end_angle, cmath . phase (major_axis_direction), radiuses_on_canvas)



  def draw_ellipse (self, focuses, semi_minor_axis):
    """Draws an ellipse with axis parallel to the x and y axis.

    Args:
      * ``focuses`` (``list``): list of two list of coordinates of the focuses of the ellipse
      * ``semi_minor_axis`` (``float``): semi minor axis

    Examples (see also :ref:`points-crosses-circles-ellipses.py` and :ref:`torus.py`)::

      import math
      #the_tau = 2. * math . pi

      import mathsvg

      image = mathsvg . SvgImage (file_name = "example.svg", rescaling = 100, shift = [ 4, 4 ])
      image . set_view_box ((800, 800))

      focuses = [ [-1.33, 0.61], [1.33, -0.61] ]

      image . draw_ellipse (focuses, 0.68)
      
      image . save ()
    """
    complex_focuses = [ f [0] + 1j * f [1] for f in focuses ]
    major_axis_direction = complex_focuses [1] - complex_focuses [0]
    distance_between_the_focuses = abs (major_axis_direction)
    major_axis_direction /= distance_between_the_focuses
    half_distance_between_the_focuses = 0.5 * distance_between_the_focuses
    semi_major_axis = math . sqrt (semi_minor_axis * semi_minor_axis + half_distance_between_the_focuses * half_distance_between_the_focuses)

    middle_point = 0.5 * (complex_focuses [0] + complex_focuses [1])

    center_on_canvas = self . project_complex_point_to_canvas (middle_point)
    radiuses_on_canvas = self . _rescale_ellipse_radiuses ([semi_major_axis, semi_minor_axis])

    ellipse = svgwrite . shapes . Ellipse (center_on_canvas,
                                           radiuses_on_canvas,
                                           style = self . _make_svg_style_string ())
    ellipse . rotate (- math . degrees (cmath . phase (major_axis_direction)), center = center_on_canvas)

    self . svgwrite_object . add (ellipse)

 

  def draw_circle (self, center, radius):
    """Draws an arc of a circle.

    Args:
      * ``center`` (``list``): coordinates of the center of the circle
      * ``radius`` (``float``): radius of the circle

    Examples: see :ref:`points-crosses-circles-ellipses.py`, :ref:`potato-regions.py`
    """

    center_on_canvas = self . project_point_to_canvas (center)
    radius_on_canvas = self . _rescale_vector ([ radius, radius ])
    ellipse = svgwrite . shapes . Ellipse (center_on_canvas,
                                           radius_on_canvas,
                                           style = self . _make_svg_style_string ())
    self . svgwrite_object . add (ellipse)




  def draw_polyline (self, point_list):
    """Draw a sequence of connected lins segments.

    Args:
      * ``point_list`` (``list``): ordered list of points (coordinates) to connect with line segments

    Example (see also :ref:`interpolated-curves.py`)::

      image = mathsvg . SvgImage ("example.svg", rescaling = 100)
      image . set_view_box ((1000, 1000))
      point_list = [ [2.5,5], [4.5,7], [2.5,4], [0.5,3] ]
      image . draw_polyline (point_list)
    """
    
    points = [ self . project_point_to_canvas (point) for point in point_list ]

    polyline = svgwrite . shapes . Polyline (points = points,
                                             style = self . _make_svg_style_string ())
    self . svgwrite_object . add (polyline)



  def draw_function_graph (self, eval_function, x_start, x_end, nb_x, curve_type = "polyline"):
    """Draws the graph of a function *f*, that is, an interpolation of a set of ``nb_x`` points *(x, y)* with *y = f (x)* and with *x* between ``x_start`` and ``x_end``. The default interpolation is by straight lines. It is also possible to have some type of smooth interpolation. The ``nb_x`` points have regularly spaced *x* coordinates starting from ``x_start`` and ending at ``x_end``.

    Args:
      * ``eval_function``: a function (or a lambda) that takes *x* as an argument and returns *y = f (x)*
      * ``x_start`` (``float``): start of the graph domain
      * ``x_end`` (``float``): end of the graph domain
      * ``nb_x`` (``int``): number of points *x* at which the function is computed
      * ``curve_type`` (``str`` or ``None``): if ``"polyline"`` then the point are interpolated by line segments, if ``"autosmooth"`` the interpolation is smoother

    Examples (see also :ref:`graphs.py`)::

      image = mathsvg . SvgImage ("example.svg", rescaling = 100, shift = [ 0, 5 ])
      image . set_view_box ((1000, 1000))

      function = lambda x : math . sin (5 * x)

      image . set_svg_options (stroke_color = "blue")
      image . draw_function_graph (function, 0, 10, 33, curve_type = "polyline")
      image . set_svg_options (stroke_color = "black")
      image . draw_function_graph (function, 0, 10, 214, curve_type = "autosmooth")
    """

    x_step = (x_end - x_start) / (nb_x - 1)
    point_list = [ [ x, eval_function (x) ] for x in [ x_start + xi * x_step for xi in range (nb_x) ] ]
    if (curve_type == "polyline"):
      self . draw_polyline (point_list)
    elif (curve_type == "autosmooth"):
      self . draw_smoothly_interpolated_open_curve (point_list)
    else:
      raise Exception ("curve_type not in ('polyline', 'autosmooth')")
    return      

 


  def draw_parametric_graph (self, eval_x, eval_y, t_start, t_end, nb_t, curve_type = "polyline", is_closed = False):
    """Draws a parametric graph given by the functions *x(t)* and *y(t)*, that is, an interpolation of a set of ``nb_t`` points *(x, y)* with *x = x(t)* and *y = y(t)* and with *t* between ``t_start`` and ``t_end``. The default interpolation is by straight lines. It is also possible to have some type of smooth interpolation. The ``nb_t`` parameters are regularly spaced starting from ``t_start`` and ending at ``t_end``.

If ``is_closed`` is set to ``True`` the two endpoints of the curve will be joined according to the choice of interpolation.

    Args:
      * ``eval_x``: a function (or a lambda) that takes the parameter *t* as an argument and returns the coordinate *x* for the pameter *t*
      * ``eval_y``: a function (or a lambda) that takes the parameter *t* as an argument and returns the coordinate *y* for the pameter *t*
      * ``t_start`` (``float``): start of the parameter domain
      * ``t_end`` (``float``): end of the parameter domain
      * ``nb_t`` (``int``): number of parameters *t* at which the functions *x* and *y* are computed
      * ``curve_type`` (``str`` or ``None``): if ``"polyline"`` then the point are interpolated by line segments, if ``"autosmooth"`` the interpolation is smoother
      * ``is_closed`` (``str`` or ``None``): whether the parametric curve should be closed (``True``) or not (``False``)

    Examples (see also :ref:`parametric-graphs.py`)::

      import math

      image = mathsvg . SvgImage ("example.svg", rescaling = 100, shift = [ 1.1, 1.5 ])
      image . set_view_box ((400, 300))

      x = lambda t : math . sin (10 * math . pi * t) + 0.1
      y = lambda t : math . cos (6 * math . pi *  t)
      image . set_svg_options (stroke_color = "blue")
      image . draw_parametric_graph (x, y, 0, 1, 40, curve_type = "polyline", is_closed = False)

      x = lambda t : math . sin (10 * math . pi * t) + 1.1
      y = lambda t : math . cos (6 * math . pi * t)
      image . set_svg_options (stroke_color = "black")
      image . set_dash_mode ("dash")
      image . draw_parametric_graph (x, y, 0, 1, 40, curve_type = "autosmooth", is_closed = True)
    """

    t_step = (t_end - t_start) / (nb_t - 1)
    point_list = [ [ eval_x (t), eval_y (t) ] for t in [ t_start + ti * t_step for ti in range (nb_t) ] ]
    if (curve_type == "polyline"):
      self . draw_polyline (point_list)
      if (is_closed):
        self . draw_line_segment (point_list [-1], point_list [0])
    elif (curve_type == "autosmooth"):
      if (is_closed):
        self . draw_smoothly_interpolated_closed_curve (point_list)
      else:
        self . draw_smoothly_interpolated_open_curve (point_list)
    else:
      raise Exception ("curve_type not in ('polyline', 'autosmooth')")
    return      

 


  def _compute_autosmooth_control_vectors (self, point_coordinates, is_path_closed = False, vectors_relative_size = 0.3):

    # Pretend-emulates Inkscape autosmooth (for open paths):
    #  the control vectors are parallel to the direction determined by the points before (left point) and after (right point) the current point
    #  their length is proportional to the respective distances on the left and on the right
    #  (first left vector and last right vector are zero)
    #
    # NOTE: on Inkscape, this works differently with closed paths, but im fine with the current working
    #
    # Implementation when is_path_closed == True :
    #       add extra points at the start and at the end,
    #       then compute the "control vectors" as if this was an open path,
    #       then remove the extremities again
    #
    #
    # As a purely graphical routine: applies to points on the canvas (ie after projection)
    #
    # vectors_relative_size will be ignored forever
 
    # when the path is closed, the extremities are artifically replicated at both ends in order to pretend that we are autosmoothing an open path
    if (is_path_closed):
      points = [ p [:] for p in point_coordinates ]
      points . insert (0, point_coordinates [-1] [:])
      points . append (point_coordinates [0] [:])
    else:
      points = point_coordinates

    nb_points = len (points)

    complex_points = [ pt [0] + 1j * pt [1] for pt in points ]

    left_right_vectors = []

    prev_point = complex_points [0]
    current_point = complex_points [1]
    right_dist = abs (current_point - prev_point)

    for point_index in range (1, nb_points - 1):

      next_point = complex_points [point_index + 1]

      direction = next_point - prev_point
      direction_len_inverse = 1 / abs (direction)
      normalized_direction = direction_len_inverse * direction

      left_dist = right_dist
      right_dist = abs (next_point - current_point)

      left_vector = - vectors_relative_size * left_dist * normalized_direction
      right_vector = vectors_relative_size * right_dist * normalized_direction

      left_right_vectors += [ left_vector, right_vector ]

      prev_point = current_point
      current_point = next_point

    # Conversion of coordinates: vector -> attached vector = point + vector
    control_vectors = [ complex_points [0] ]
    for point_index in range (1, nb_points - 1):
      vector_index  = 2 * (point_index - 1)
      control_vectors . append (left_right_vectors [vector_index] + complex_points [point_index])
      control_vectors . append (left_right_vectors [vector_index + 1] + complex_points [point_index])
    control_vectors . append (complex_points [-1])

    if (is_path_closed):
     last_left_vector = control_vectors [1]
     control_vectors = control_vectors [ 2 : -1 ]
     control_vectors . append (last_left_vector)

    return [ [ cv . real, cv . imag ] for cv in control_vectors ]

  
  def draw_smoothly_interpolated_open_curve (self, points):
    """Draws a smooth open curve that interpolates the points given as parameter.

    The coordinates of the endpoints of the curve are the first and last set of coordinates from the list given as argument.

    Args:
      * ``points`` (``list``): list of point coordinates to interpolate

    Example (see also :ref:`interpolated-curves.py`)::

      image = mathsvg . SvgImage (file_name = "example.svg", rescaling = 100)
      image . set_view_box ((1000, 1000))
      point_list = [ [7.4, 2], [5.6, 4], [7.3, 6], [ 4.3, 5.2], [ 8.3, 9.1 ] ]
      image . draw_smoothly_interpolated_open_curve (point_list)
      image . save ()
    """

    control_points = [ self . project_point_to_canvas (point) for point in points ]
    control_vectors = self . _compute_autosmooth_control_vectors (control_points, is_path_closed = False)
    path_command = self . _make_svg_path_M_and_C_command (control_points, control_vectors)
    self . insert_svg_path_command (path_command)
    return

  def draw_smoothly_interpolated_closed_curve (self, points):
    """Draws a smooth closed curve that interpolates the points given as parameter.

    Args:
      * ``points`` (``list``): list of point coordinates to interpolate

    Example (see also :ref:`interpolated-curves.py`)::

      image = mathsvg . SvgImage (file_name = "example.svg", rescaling = 100)
      image . set_view_box ((1000, 1000))
      point_list = [ [7.4, 2], [5.6, 4], [7.3, 6], [ 4.3, 5.2], [ 8.3, 9.1 ] ]
      image . draw_smoothly_interpolated_closed_curve (point_list)
      image . save ()
    """

    control_points = [ self . project_point_to_canvas (point) for point in points ]
    control_vectors = self . _compute_autosmooth_control_vectors (control_points, is_path_closed = True)
    path_command = self . _make_svg_path_M_and_C_command (control_points + [ control_points [0], ], control_vectors)
    path_command += self . _make_svg_path_Z_command ()
    self . insert_svg_path_command (path_command)
    return


  def _generate_potato_complex_vertexes (self, center, inner_radius, outer_radius, nb_vertexes):
   # generate complex numbers in the abstract plane, ie before projection on the canvas

   angles = [ random . uniform (0, the_tau) for v in range (nb_vertexes) ]
   angles . sort ()
   
   lengths = [ random . uniform (inner_radius, outer_radius) for v in range (nb_vertexes) ]

   return [ center + lengths [i] * cmath . exp (1j * angles [i]) for i in range (nb_vertexes) ] 
 


  def draw_planar_potato (self, center, inner_radius, outer_radius, nb_vertexes):
    """Draws some randomly generated smooth shape in the form of a smooth closed curve.

    A set of radomly generated set of ``nb_vertexes`` points is generated. Both angles and distances with respect to center are generated according to a uniform law. The distance from the center is chosen uniformly between the values of ``inner_radius`` and ``outer_radius``.

    Args:
      * ``center`` (``list``): coordinates of the center of the potato
      * ``inner_radius`` (``float``): roughly the closest the curve comes from the center
      * ``outer_radius`` (``float``): roughly the farthest the curve comes from the center
      * ``nb_vertexes`` (``int``): number of points to generate (more points means that it is more likely that the curve will have selfintersections)

    Example (see also: :ref:`potato.py`, :ref:`potato-3v.py`, :ref:`dashes.py`, :ref:`wiggly-potato.py`, :ref:`wigglier-potato.py`, :ref:`potato-regions.py`)::

      image = mathsvg . SvgImage (file_name = "example.svg", rescaling = 100, shift = [2, 2])
      image . set_view_box ((400, 400))
      image . draw_planar_potato ([0, 0], 0.5, 1.5, 3)
      image . save ()
    """


    z_center = center [0] + 1j * center [1]

    complex_vertexes = self . _generate_potato_complex_vertexes (z_center, inner_radius, outer_radius, nb_vertexes)

    vertexes = [ self . project_complex_point_to_canvas (v) for v in complex_vertexes ]

    control_vectors = self . _compute_autosmooth_control_vectors (vertexes, is_path_closed = True)

    vertexes . append (vertexes [0])
    path_command = self . _make_svg_path_M_and_C_command (vertexes, control_vectors)

    path_command += self . _make_svg_path_Z_command ()

    self . insert_svg_path_command (path_command)

    return



  def draw_random_wavy_line (self, start_point, end_point, wave_len, amplitude):
    """Draws a smooth line with randomly generated bumps perpendicularly to its direction.

    Regularly separated points are computed along the straight line segment between the two end points.  The distance between two consecutive points is equal to ``wave_len``.
    Then for each of these points, a point is picked randomly on the corresponding perpendicular line according to a uniform law, symmetrically with respect to the directing line and with maximum distance equal to the value of ``amplitude``. Finally a smooth interpolating curve is drawn.
    This curve goes from the first end point to the last and passes along the randomly generated points.

    Args:
      * ``start_point`` (``list``): coordinates of the first end point of the line
      * ``end_point`` (``list``): coordinates of the second end point of the line
      * ``wave_len`` (``float``): distance between two consecutive disturbances (smaller values yield more bumps)
      * ``amplitude`` (``float``): size of the bumps

    Raises some error text exception when the value of ``wave_len`` is larger or equal to the distance between the two end points.

    Example (see also :ref:`lines.py` and :ref:`scribble.py`)::

      image = mathsvg . SvgImage (file_name = "example.svg", rescaling = 100, shift = [ 4, 4 ])
      image . set_view_box ((800, 800))

      image . set_dash_mode ("dot")
      image . draw_line_segment ([-3., -2.9], [3., 3.1])
      image . draw_line_segment ([-3., -2.7], [3., 3.3])
      image . set_dash_mode ("none")
      image . draw_random_wavy_line ([-3., -2.8], [3., 3.2], 0.1, 0.1)

      image . save ()
    """

    z_start = start_point [0] + 1.j * start_point [1]
    z_end = end_point [0] + 1.j * end_point [1]

    line_direction = z_end - z_start
    distance_from_start_to_end = abs (line_direction)

    if (wave_len >= distance_from_start_to_end):
      # note: rare exception where I check the arguments
      raise Exception ("wave_len too small, should be < distance between start and end points")

    line_direction /= distance_from_start_to_end
    perp_direction = 1j * line_direction

    nb_points_to_compute = int (distance_from_start_to_end / wave_len)

    points = [ self . project_point_to_canvas (start_point) ]

    for point_index in range (nb_points_to_compute):
      center = line_direction * wave_len * (point_index + 1) + z_start
      perturbation = random . uniform (- amplitude, amplitude) * perp_direction
      next_point = center + perturbation
      points . append (self . project_complex_point_to_canvas (next_point))

    points . append (self . project_complex_point_to_canvas (z_end))

    
    nb_points = len (points) # = nb_points_to_compute + 2
   
    control_vectors = self . _compute_autosmooth_control_vectors (points)

    path_command = self . _make_svg_path_M_and_C_command (points, control_vectors)
	
    self . insert_svg_path_command (path_command)

    return

    """
    """

  def insert_svg_path_command (self, svg_path_command):
    """Insert a path command given in the form of a string into the SVG.

    The resulting SVG command will be of the form ``<path d="..." style="..." />``,
    where the first ``"..."`` stands for the content of the argument ``svg_path_command`` and the second ``"..."`` is an automatically generated style option string based on the current state of the ``SvgImage`` object (including: stroke color, width, filling color, dash array, etc.).
    The validity of the argument as a path command is not checked. Errors might or might not raise an exception, depending on the behavior of the module svgwrite.

    Args:
      * ``svg_path_command`` (``str``): the string to be inserted.

    Example::

       image = mathsvg . SvgImage (rescaling = 100, shift = [ 4, 4 ])
       image . set_view_box ((800, 800))
       image . insert_svg_path_command ("M 650, 650 C 650, 650 443, 693 275, 525 107, 357 150, 150 150, 150")
       image . save ("example.svg")



    The result is the following image:
.. image:: svg-command-example.svg
   :width: 200px
   :height: 200px
   :align: center
   :alt: A portion of a Bezier curve
   """

    # so that really anything can be added - no checking
    path = self . svgwrite_object . path (d = svg_path_command,
                                          style = self . _make_svg_style_string ())
    self . svgwrite_object . add (path)


