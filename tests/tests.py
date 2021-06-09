# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2020-01-31
# Copyright (C) 2020, 2021 Alexandre De Zotti
# License: MIT License

import unittest

import os
import re
import subprocess
import sys
import tempfile

import mathsvg

import cairosvg
import matplotlib.pylab as pylab
import numpy
import numpy.linalg



# TODO
do_save_to_local_dir = True
# if not use tmpfile

test_data_path = "../tests/"
test_models_path = os.path.join(test_data_path, "test-models")
test_scripts_path = os.path.join(test_data_path, "test-scripts")
examples_path = "../examples"


default_drawing_options = "style *= *\"fill *: *.*; *stroke *: *black; *stroke-width *: *1; *stroke-dasharray *: *none; *\""
number_list_re_pattern = "[0-9\\. ,\\-]*"


def check_actual_image(test_object, svg_file_name, image_model_file_name, fail_message, max_dist = 0.001):
  converted_file_name = "test.png"
  f = open(svg_file_name, "rb")
  cairosvg.svg2png(file_obj = f, write_to = converted_file_name)
  f.close()

  model_image = pylab.imread(image_model_file_name)
  converted_image = pylab.imread(converted_file_name)
  test_object.assertEqual(converted_image.shape, model_image.shape, f'{fail_message} (image sizes mismatch)')

  #try :
  test_object.assertTrue(numpy.allclose(model_image, converted_image))  
  #else :
  os.remove(converted_file_name)




def check_file_content(test_object, file_name, regex, fail_message):
  svg_file = open(file_name, "r")
  content = svg_file.read()
  test_object.assertRegex(content, regex, fail_message)
  svg_file.close()


def test_simple_example(test_object, example_name, example_dir, error_message_example_name):
  subprocess.call([ "python", os.path.join(example_dir, example_name + ".py") ])
  check_actual_image(test_object, example_name + ".svg", os.path.join(test_models_path, example_name + ".png"), f'{error_message_example_name} example image very different from model')
  os.remove(example_name + ".svg")

def clean_files(file_list):
  for f in file_list:
    if(os.path.exists(f)):
      os.remove(f)


def prepare_simple_canvas(window_size = 1., pixel_density = 100) :
  return mathsvg.SvgImage(view_window = ((0, 0), (window_size, window_size)), pixel_density = pixel_density)


class TestMain(unittest.TestCase):

  def test_save_image(self):
    clean_files(["test.svg",])
    image = mathsvg.SvgImage(pixel_density = 100, view_window = ( (-4, -4), (4, 4) )) 
    image.save("test.svg")
    self.assertTrue(os.path.exists("test.svg"), "file save failed")
    os.remove("test.svg")

  def test_saved_file_contains_svg(self):
    image = mathsvg.SvgImage(pixel_density = 100, view_window = ( (-4, -4), (4, 4) )) 
    image.save("test.svg")
    check_file_content(self, "test.svg", "<svg.*</svg>$", "saved file doesnt contain svg")
    os.remove("test.svg")

  def test_default_drawing_options(self):
    image = mathsvg.SvgImage(pixel_density = 100, view_window = ( (-4, -4), (4, 4) )) 
    image.draw_arrow([ -2, -2 ], [ 2, 2 ])
    image.save("test.svg")
    check_file_content(self, "test.svg", default_drawing_options, "default drawing options not in use for line")
    os.remove("test.svg")
     
  def test_multiple_save(self):
    output_files = [ "save-1.svg", "save-2.svg" ]
    clean_files(output_files)
    subprocess.call([ "python", os.path.join(test_scripts_path, "multiple-save.py") ])
    self.assertTrue(os.path.exists(output_files[0]), "multiple-save failed at first save")
    self.assertTrue(os.path.exists(output_files[1]), "multiple-save failed at second save")
    clean_files(output_files)
    
  def test_multiple_save_example(self):
    output_files = [ "save-1", "save-2" ]
    subprocess.call([ "python", os.path.join(test_scripts_path, "multiple-save.py") ])
    check_actual_image(self, output_files[0] + ".svg", os.path.join(test_models_path, output_files[0] + ".png"), "multiple-save example: first saved image very different from model")
    check_actual_image(self, output_files[1] + ".svg", os.path.join(test_models_path, output_files[1] + ".png"), "multiple-save example: second saved image very different from model")
    clean_files([ f + ".svg" for f in output_files ])

class TestArrows(unittest.TestCase):

  def test_default_arrow_svg(self):
    image = mathsvg.SvgImage(pixel_density = 100, view_window = ( (-4, -4), (4, 4) )) 
    image.draw_arrow([ -2, -2 ], [ 2, 2 ])
    image.save("test.svg")
    arrow_regex = "<line.*x1 *=.*x2 *=.*y1 *=.*y2 *=.*/><path *d *= *\""
    arrow_regex += " *M" + number_list_re_pattern + "C" + number_list_re_pattern + "Z *\" *"
    arrow_regex += default_drawing_options
    check_file_content(self, "test.svg", arrow_regex, "arrow not drawn")

  def test_default_arrow_images(self):
    image = mathsvg.SvgImage(pixel_density = 100, view_window = ( (-4, -4), (4, 4) )) 
    image.draw_arrow([ -2, -2 ], [ 2, 2 ])
    image.save("test-default-arrow.svg")
    check_actual_image(self, "test-default-arrow.svg", os.path.join(test_models_path, "test-default-arrow.png"), "default arrow image very different from model")

  def test_arrow_examples(self):
    test_simple_example(self, "arrows", examples_path, "arrow")

  def test_curved_arrow_examples(self):
    test_simple_example(self, "curved-arrows", examples_path, "curved arrow")

  def test_more_curved_arrow_examples(self):
    test_simple_example(self, "more-curved-arrows", examples_path, "second set of curved arrow")

class TestDashes(unittest.TestCase):

  def test_dashes_examples(self):
    test_simple_example(self, "dashes", test_scripts_path, "dashes")


class TestGraph(unittest.TestCase):

  def test_graph_examples(self):
    test_simple_example(self, "graphs", examples_path, "graph")

  def test_parametric_graph_examples(self):
    test_simple_example(self, "parametric-graphs", examples_path, "parametric graph")

class TestInterpolatedCurve(unittest.TestCase):

  def test_interpolated_curve_examples(self):
    test_simple_example(self, "interpolated-curves", examples_path, "interpolated curve")


class TestLine(unittest.TestCase):

  def test_line_examples(self):
    test_simple_example(self, "lines", test_scripts_path, "line")


class TestPotato(unittest.TestCase):
  # this is unclear what these examples test precisely
  def test_first_potato_example(self):
    test_simple_example(self, "potato", test_scripts_path, "first potato (simple)")

  def test_second_potato_example(self):
    test_simple_example(self, "potato-3v", test_scripts_path, "second potato (3 vertexes)")

  def test_third_potato_example(self):
    test_simple_example(self, "potato-regions", test_scripts_path, "third potato (region compare)")

  def test_fourth_potato_example(self):
    test_simple_example(self, "wigglier-potato", test_scripts_path, "fourth potato (wigglier)")

  def test_fifth_potato_example(self):
    test_simple_example(self, "wiggly-potato", test_scripts_path, "fifth potato (wiggly)")


class TestPutText(unittest.TestCase):

  def _check_text_attributes(self, xml, text, font_size, x, y) :
    self.assertEqual(xml.tag, 'text')
    self.assertEqual(xml.text, text)
    self.assertAlmostEqual(float(xml.attrib['font-size']), font_size, places = 2)
    self.assertAlmostEqual(float(xml.attrib['x']), x, places = 2)
    self.assertAlmostEqual(float(xml.attrib['y']), y, places = 2)

  def test_font_pixel_size(self) :
    canvas = prepare_simple_canvas()
    self.assertEqual(canvas.rescaling, 100)
    self.assertAlmostEqual(canvas.font_size_svgpx, 6., places = 2)
  
  def test_put_text_no_font_size(self) :
    canvas = prepare_simple_canvas()
    canvas.put_text('.', (0.5,0.5))
    # last added object should be a text with the right coords and font size
    xml = canvas.svgwrite_object.get_xml()[-1]
    self._check_text_attributes(xml, '.', 6., 50., 51.)

  def test_put_text_with_font_size(self) :
    canvas = prepare_simple_canvas(window_size = 1., pixel_density = 100)
    canvas.put_text('test text', (0.5, 0.5), font_size = .505)
    xml = canvas.svgwrite_object.get_xml()[-1]
    self._check_text_attributes(xml, 'test text', 50.5, 50., 51.)
    canvas.put_text('test text', (0.5, 0.5), font_size = 18, units='svg')
    xml = canvas.svgwrite_object.get_xml()[-1]
    self._check_text_attributes(xml, 'test text', 18, 50., 51.)
    canvas.put_text('test text', (0.5, 0.5), font_size = .35, units='math')
    xml = canvas.svgwrite_object.get_xml()[-1]
    self._check_text_attributes(xml, 'test text', 35, 50., 51.)

  def test_set_font_size(self) :
    # TODO check font size, in svg and math units
    canvas = prepare_simple_canvas(window_size = 1., pixel_density = 100)
    canvas.set_font_options(font_size = 1., units = 'math')
    canvas.put_text('test text', (0.5, 0.5))
    xml = canvas.svgwrite_object.get_xml()[-1]
    self._check_text_attributes(xml, 'test text', 100., 50., 51.)

  def test_put_text_examples(self):
    test_simple_example(self, "put-text-example", examples_path, "put_text")

class TestRandomWavyLine(unittest.TestCase):
  def test_random_wavy_line_examples(self):
    test_simple_example(self, "scribble", test_scripts_path, "random wavy line")

class TestCollections(unittest.TestCase):
  # should isolated each element from these collections for testing
  def test_point_cross_circle_ellipse_examples(self):
    test_simple_example(self, "points-crosses-circles-ellipses", examples_path, "point+cross+circle+ellipse ")

  def test_torus_example(self):
    test_simple_example(self, "torus", examples_path, "torus")

class TestPoints(unittest.TestCase) :

  def test_draw_point(self) :
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    canvas.draw_point((0.5, 0.5))
    xml = canvas.svgwrite_object.get_xml() [-1]
    self.assertEqual(xml.tag, 'circle')
    attrib = xml.attrib
    self.assertAlmostEqual(float(attrib['cx']), 50, places = 2)
    self.assertAlmostEqual(float(attrib['cy']), 51, places = 2.)
    self.assertAlmostEqual(float(attrib['r']), 6., places = 2)
    self.assertEqual(attrib['style'], 'fill : black; stroke : black; stroke-width : 1; stroke-dasharray : none;')

  def test_draw_cross(self) :
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    canvas.draw_cross((0.5, 0.5))
    xml = canvas.svgwrite_object.get_xml() [-2:]
    self.assertEqual(xml[0].tag, 'line')
    attrib = xml[0].attrib
    self.assertAlmostEqual(float(attrib['x1']), 44, places = 2)
    self.assertAlmostEqual(float(attrib['x2']), 56, places = 2)
    self.assertAlmostEqual(float(attrib['y1']), 45, places = 2)
    self.assertAlmostEqual(float(attrib['y2']), 57, places = 2)
    self.assertEqual(attrib['style'], 'fill : none; stroke : black; stroke-width : 1; stroke-dasharray : none;')
    self.assertEqual(xml[1].tag, 'line')
    attrib = xml[1].attrib
    self.assertAlmostEqual(float(attrib['x2']), 44, places = 2)
    self.assertAlmostEqual(float(attrib['x1']), 56, places = 2)
    self.assertAlmostEqual(float(attrib['y1']), 45, places = 2)
    self.assertAlmostEqual(float(attrib['y2']), 57, places = 2)
    self.assertEqual(attrib['style'], 'fill : none; stroke : black; stroke-width : 1; stroke-dasharray : none;')
  
  def test_draw_plus(self) :
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    canvas.draw_plus((0.5, 0.5))
    xml = canvas.svgwrite_object.get_xml() [-2:]
    self.assertEqual(xml[0].tag, 'line')
    attrib = xml[0].attrib
    self.assertAlmostEqual(float(attrib['x1']), 44, places = 2)
    self.assertAlmostEqual(float(attrib['x2']), 56, places = 2)
    self.assertAlmostEqual(float(attrib['y1']), 51, places = 2)
    self.assertAlmostEqual(float(attrib['y2']), 51, places = 2)
    self.assertEqual(attrib['style'], 'fill : none; stroke : black; stroke-width : 1; stroke-dasharray : none;')
    self.assertEqual(xml[1].tag, 'line')
    attrib = xml[1].attrib
    self.assertAlmostEqual(float(attrib['y1']), 45, places = 2)
    self.assertAlmostEqual(float(attrib['y2']), 57, places = 2)
    self.assertAlmostEqual(float(attrib['x1']), 50, places = 2)
    self.assertAlmostEqual(float(attrib['x2']), 50, places = 2)
    self.assertEqual(attrib['style'], 'fill : none; stroke : black; stroke-width : 1; stroke-dasharray : none;')

  def test_set_point_size(self) :
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    canvas.set_point_size(1., units = 'math')
    canvas.draw_point((0.5, 0.5))
    xml = canvas.svgwrite_object.get_xml() [-1]
    self.assertAlmostEqual(float(xml.attrib['r']), 100., places = 2)


  def test_set_point_size_twice(self) :
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    canvas.set_point_size(1., units = 'math')
    canvas.draw_point((0.5, 0.5))
    canvas.set_point_size(.3, units = 'math')
    canvas.draw_point((0.5, 0.5))
    xml = canvas.svgwrite_object.get_xml() [-1]
    self.assertAlmostEqual(float(xml.attrib['r']), 30., places = 2)
  
  def test_reset_point_size(self) :
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    canvas.set_point_size(1., units = 'svg')
    canvas.draw_point((0.5, 0.5))
    canvas.reset_point_size()
    canvas.draw_point((0.5, 0.5))
    xml = canvas.svgwrite_object.get_xml() [-1]
    self.assertAlmostEqual(6., float(xml.attrib['r']), places = 2)
    

class TestSvgOptions(unittest.TestCase) :

  def test_default_stroke_width(self) :
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    self.assertEqual(canvas.stroke_width, 1)
    canvas = prepare_simple_canvas(pixel_density = 10, window_size = 1.)
    self.assertEqual(canvas.stroke_width, 1)
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 10.)
    self.assertEqual(canvas.stroke_width, 1)
  
  def test_svg_vs_math_units(self):
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    
    canvas.set_dash_dot_structure(0.01)
    self.assertAlmostEqual(canvas.dot_dasharray_svgpx[0], canvas.stroke_width, places=2)
    self.assertAlmostEqual(canvas.dot_dasharray_svgpx[1], 1, places=2)
    canvas.set_dash_dot_structure(2, units='svg')
    self.assertAlmostEqual(canvas.dot_dasharray_svgpx[0], canvas.stroke_width, places=2)
    self.assertAlmostEqual(canvas.dot_dasharray_svgpx[1], 2, places=2)
    canvas.set_dash_dot_structure(0.1, units='math')
    self.assertAlmostEqual(canvas.dot_dasharray_svgpx[0], canvas.stroke_width, places=2)
    self.assertAlmostEqual(canvas.dot_dasharray_svgpx[1], 10, places=2)
    
    canvas.set_dash_dash_structure(0.1, 0.2)
    self.assertAlmostEqual(canvas.dash_dasharray_svgpx[0], 10, places=2)
    self.assertAlmostEqual(canvas.dash_dasharray_svgpx[1], 20, places=2)
    canvas.set_dash_dash_structure(3, 1, units='svg')
    self.assertAlmostEqual(canvas.dash_dasharray_svgpx[0], 3, places=2)
    self.assertAlmostEqual(canvas.dash_dasharray_svgpx[1], 1, places=2)
    canvas.set_dash_dash_structure(0.02, 0.03, units='math')
    self.assertAlmostEqual(canvas.dash_dasharray_svgpx[0], 2, places=2)
    self.assertAlmostEqual(canvas.dash_dasharray_svgpx[1], 3, places=2)
    
    canvas.set_font_options(font_size=0.1)
    self.assertAlmostEqual(canvas.font_size_svgpx, 10., places=2)
    canvas.set_font_options(font_size=10, units='svg')
    self.assertAlmostEqual(canvas.font_size_svgpx, 10., places=2)
    canvas.set_font_options(font_size=0.2, units='math')
    self.assertAlmostEqual(canvas.font_size_svgpx, 20., places=2)
    
    canvas.set_point_size(0.01)
    self.assertAlmostEqual(canvas.point_size_svgpx, 1, places=2)
    canvas.set_point_size(1, units='svg')
    self.assertAlmostEqual(canvas.point_size_svgpx, 1, places=2)
    canvas.set_point_size(0.03, units='math')
    self.assertAlmostEqual(canvas.point_size_svgpx, 3, places=2)
    
    # check for minimal width of stroke
    canvas.set_svg_options(stroke_width=0.001)
    self.assertEqual(canvas.stroke_width, 1)

    canvas.set_svg_options(stroke_width=.15, dash_array=[ 0.1, 0.01, 0.02 ])
    self.assertAlmostEqual(canvas.stroke_width, 15, places=2)
    self.assertAlmostEqual(canvas.dasharray_dasharray_svgpx[0], 10, places=2)
    self.assertAlmostEqual(canvas.dasharray_dasharray_svgpx[1], 1, places=2)
    self.assertAlmostEqual(canvas.dasharray_dasharray_svgpx[2], 2, places=2)
    canvas.set_svg_options(stroke_width=2, dash_array=[ 3, 4, 5 ], units='svg')
    self.assertAlmostEqual(canvas.stroke_width, 2, places=2)
    self.assertAlmostEqual(canvas.dasharray_dasharray_svgpx[0], 3, places=2)
    self.assertAlmostEqual(canvas.dasharray_dasharray_svgpx[1], 4, places=2)
    self.assertAlmostEqual(canvas.dasharray_dasharray_svgpx[2], 5, places=2)
    canvas.set_svg_options(stroke_width=0.07, dash_array=[ 0.08, 9 ], units='math')
    self.assertAlmostEqual(canvas.stroke_width, 7, places=2)
    self.assertAlmostEqual(canvas.dasharray_dasharray_svgpx[0], 8, places=2)
    self.assertAlmostEqual(canvas.dasharray_dasharray_svgpx[1], 900, places=2)
    
    canvas.set_arrow_options(width = .2)
    self.assertAlmostEqual(20, canvas.arrow_width_svgpx, places = 2)
    canvas.set_arrow_options(width = 5, units='svg')
    self.assertAlmostEqual(5, canvas.arrow_width_svgpx, places = 2)
    canvas.set_arrow_options(width = 0.18, units='math')
    self.assertAlmostEqual(18, canvas.arrow_width_svgpx, places = 2)

class TestInternals(unittest.TestCase) :

  def test_smallish_size(self) :
    image = prepare_simple_canvas() # 0, 0 -> 100, 100 + 1px
    self.assertEqual(image._compute_a_smallish_size_in_svg_units(), 2.)
    self.assertEqual(image._compute_a_smallish_size_in_math_units(), 0.02)

  def project_point_to_canvas(self) :
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    projected_point = canvas.project_point_to_canvas((0.5, 0.5))
    self.assertAlmostEqual(projected_point[0], 50, places = 2)
    self.assertAlmostEqual(projected_point[1], 51, places = 2)
    projected_point = canvas.project_point_to_canvas((0.3, 0.41))
    self.assertAlmostEqual(projected_point[0], 30, places = 2)
    self.assertAlmostEqual(projected_point[1], 42, places = 2)
    
  def test_y_pixel_shift(self) :
    # the y coordinate has to be shifted by 1 pixel because the screen coordinates are flipped upside down
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    canvas.draw_plus((0.5, 0.5))
    xml = canvas.svgwrite_object.get_xml() [-2]
    self.assertAlmostEqual(51, float(xml.attrib['y1']), places = 2)
  

class TestShapes(unittest.TestCase):

  def test_rectangle_and_polygons(self):
    image = mathsvg.SvgImage(pixel_density = 20, view_window = ((0, 0), (8, 8)))
    point_list = [ (2.5,5), (4.5,7), (2.5,4), (0.5,3), (6,2) ]
    image.draw_polygon(point_list)
    image.draw_rectangle(7,1,1,7)
    xml_data = image.svgwrite_object.get_xml()
    
    self.assertEqual(xml_data[1].tag, 'polygon')
    coords = [ round(float(c)) for c in xml_data[1].attrib['points'].replace(',', ' ').split() ]
    self.assertSequenceEqual(coords, [ 50, 61, 90, 21, 50, 81, 10, 101, 120, 121 ])
    
    xml_rect_data = xml_data[2]
    self.assertEqual(xml_rect_data.tag, 'polygon')
    coords = [ round(float(c)) for c in xml_rect_data.attrib['points'].replace(',', ' ').split() ]
    self.assertSequenceEqual(coords, [ 20, 21, 20, 141, 140, 141, 140, 21, 20, 21 ])
    

class TestInlineExamples(unittest.TestCase):

  def _check_line_coords(self, attribs, x1, x2, y1, y2, places=2):
    self.assertAlmostEqual(x1, float(attribs['x1']), places=places)
    self.assertAlmostEqual(x2, float(attribs['x2']), places=places)
    self.assertAlmostEqual(y1, float(attribs['y1']), places=places)
    self.assertAlmostEqual(y2, float(attribs['y2']), places=places)

  def test_main_doc_example(self):
    image = mathsvg.SvgImage(pixel_density = 100, view_window = (( -1, -1 ), ( 1, 1 )))
    image.draw_circle([0, 0], 1.1)
    xml_data = image.svgwrite_object.get_xml()[1]
    self.assertEqual(xml_data.tag, 'ellipse')
    self.assertEqual(int(xml_data.attrib['cx']), 100)
    self.assertEqual(int(xml_data.attrib['cy']), 101)
    self.assertEqual(round(float(xml_data.attrib['rx'])), 110)
    self.assertEqual(round(float(xml_data.attrib['ry'])), 110)
 
  def test_set_dash_mode_example(self):
    image = mathsvg.SvgImage(pixel_density = 20, view_window = ((0, 0), (10, 10)))
    image.set_dash_mode("dash")
    image.draw_line_segment([0, 0], [10, 10])
    image.set_dash_mode("dot")
    image.draw_line_segment([0, 10], [10, 0])
    image.set_svg_options(dash_array = [18, 3, 1, 3, 7, 3, 1, 3], units='svg')
    image.set_dash_mode("dasharray")
    image.draw_planar_potato([5, 5], 2, 4, 8)
    xml_data = image.svgwrite_object.get_xml()
    
    line_data = xml_data[1]
    self.assertEqual('line', line_data.tag)
    line_data = line_data.attrib
    self.assertEqual(0, round(float(line_data['x1'])))
    self.assertEqual(200, round(float(line_data['x2'])))
    self.assertEqual(201, round(float(line_data['y1'])))
    self.assertEqual(1, round(float(line_data['y2'])))
    style = line_data['style']
    match = re.search(r'stroke-dasharray *: *([0-9\.]+), *([0-9\.]+);', style)
    self.assertIsNotNone(match)
    self.assertAlmostEqual(4., float(match.groups()[0]), places=3)
    self.assertAlmostEqual(4., float(match.groups()[1]), places=3)
    
    line_data = xml_data[2]
    self.assertEqual('line', line_data.tag)
    line_data = line_data.attrib
    self.assertEqual(0, round(float(line_data['x1'])))
    self.assertEqual(200, round(float(line_data['x2'])))
    self.assertEqual(1, round(float(line_data['y1'])))
    self.assertEqual(201, round(float(line_data['y2'])))
    style = line_data['style']
    match = re.search(r'stroke-dasharray *: *([0-9\.]+), *([0-9\.]+);', style)
    self.assertIsNotNone(match)
    self.assertAlmostEqual(1., float(match.groups()[0]), places=3)
    self.assertAlmostEqual(2., float(match.groups()[1]), places=3)
    
    line_data = xml_data[3]
    self.assertEqual('path', line_data.tag)
    style = line_data.attrib['style']
    match = re.search(r'stroke-dasharray *: *([0-9\., ]+);', style)
    self.assertIsNotNone(match)
    values = [ round(float(v)) for v in match.groups()[0].split(', ') ]
    self.assertEqual(len(values), 8)
    self.assertSequenceEqual([ 18, 3, 1, 3, 7, 3, 1, 3 ], values)

  def test_set_arrow_options_example(self):
    image = mathsvg.SvgImage(pixel_density = 20, view_window = ((-4, -4), (4, 4)))
    image.set_arrow_options(curvature = 0.55)
    image.draw_arrow([ -2, -2 ], [ 2, 1.7 ])
    image.set_arrow_options(width = 4 * image.arrow_width_svgpx, units='svg')
    image.draw_arrow([ -2, -2 ], [ 2, 1.2 ])
    image.reset_arrow_options()
    image.set_arrow_options(curvature = 0)
    image.draw_arrow([ -2, -2 ], [ 2, 0.6 ])
    xml_data = image.svgwrite_object.get_xml()
    tags = [ d.tag for d in xml_data[1:7] ]
    self.assertSequenceEqual([ 'line', 'path', 'line', 'path', 'line', 'path' ], tags)
    self._check_line_coords(xml_data[1].attrib, 40, 120, 121, 47)
    self._check_line_coords(xml_data[3].attrib, 40, 120, 121, 57)
    self._check_line_coords(xml_data[5].attrib, 40, 120, 121, 69)
    path = xml_data[2].attrib['d'].strip().split()
    self.assertEqual(21, len(path))
    self.assertEqual('M', path[0])
    self.assertEqual('C', path[7])
    self.assertEqual('Z', path[-1])
    path = xml_data[4].attrib['d'].strip().split()
    self.assertEqual(21, len(path))
    self.assertEqual('M', path[0])
    self.assertEqual('C', path[7])
    self.assertEqual('Z', path[-1])
    path = xml_data[6].attrib['d'].strip().split()
    self.assertEqual(21, len(path))
    self.assertEqual('M', path[0])
    self.assertEqual('C', path[7])
    self.assertEqual('Z', path[-1])



# class TestCurrentBugs(unittest.TestCase):


if(__name__ == "__main__"):
  unittest.main()






