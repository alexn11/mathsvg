# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2020-01-31
# Copyright (C) 2020, Alexandre De Zotti
# License: MIT License

import unittest

import os
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
  test_object.assertEqual(converted_image.shape, model_image.shape, fail_message + " (image sizes mismatch)")

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
  check_actual_image(test_object, example_name + ".svg", os.path.join(test_models_path, example_name + ".png"), error_message_example_name + " example image very different from model")
  os.remove(example_name + ".svg")

def clean_files(file_list):
  for f in file_list:
    if(os.path.exists(f)):
      os.remove(f)


def prepare_simple_canvas(window_size = 1., pixel_density = 100) :
  return mathsvg.SvgImage(view_window = ((0, window_size), (0, window_size)), pixel_density = pixel_density)


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
    image.save("test.svg")
    check_actual_image(self, "test.svg", os.path.join(test_models_path, "default-arrow.png"), "default arrow image very different from model")

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
    self.assertAlmostEqual(canvas.font_pixel_size, 6., places = 2)
  
  def test_put_text_no_font_size(self) :
    canvas = prepare_simple_canvas()
    canvas.put_text('.', (0.5,0.5))
    # last added object should be a text with the right coords and font size
    xml = canvas.svgwrite_object.get_xml() [-1]
    self._check_text_attributes(xml, '.', 6., 50., 51.)

  def test_put_text_with_font_size(self) :
    canvas = prepare_simple_canvas(window_size = 1., pixel_density = 100)
    canvas.put_text('test text', (0.5, 0.5), font_size = .505)
    xml = canvas.svgwrite_object.get_xml() [-1]
    self._check_text_attributes(xml, 'test text', 50.5, 50., 51.)

  def test_set_font_size(self) :
    canvas = prepare_simple_canvas(window_size = 1., pixel_density = 100)
    canvas.set_font_options(font_size = 1.)
    canvas.put_text('test text', (0.5, 0.5))
    xml = canvas.svgwrite_object.get_xml() [-1]
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
    canvas.set_point_size(1.)
    canvas.draw_point((0.5, 0.5))
    xml = canvas.svgwrite_object.get_xml() [-1]
    self.assertAlmostEqual(float(xml.attrib['r']), 100., places = 2)


  def test_set_point_size_twice(self) :
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    canvas.set_point_size(1.)
    canvas.draw_point((0.5, 0.5))
    canvas.set_point_size(.3)
    canvas.draw_point((0.5, 0.5))
    xml = canvas.svgwrite_object.get_xml() [-1]
    self.assertAlmostEqual(float(xml.attrib['r']), 30., places = 2)
  
  def test_reset_point_size(self) :
    canvas = prepare_simple_canvas(pixel_density = 100, window_size = 1.)
    canvas.set_point_size(1.)
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
  

class TestInternals(unittest.TestCase) :

  def test_smallish_size(self) :
    image = prepare_simple_canvas()
    self.assertEqual(image._compute_a_smallish_size(), 0.02)

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
  

# class TestCurrentBugs(unittest.TestCase) :


if(__name__ == "__main__"):
  unittest.main()






