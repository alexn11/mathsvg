
import subprocess

test_scripts = [
  "arrows.py",
  "curved-arrows.py",
  "dashes.py",
  "graphs.py",
  "interpolated-curves.py",
  "lines.py",
  "more-curved-arrows.py",
  "points-crosses-circles-ellipses.py",
  "potato.py",
  "potato-3v.py",
  "potato-regions.py",
  "scribble.py",
  "torus.py",
  "wigglier-potato.py",
  "wiggly-potato.py",
]





project_path = "../../../"

image_file_path = project_path + "examples/examples-images/"
rst_dest_path = "source/examples/"
examples_source_path = project_path + "examples/"


for script in test_scripts:
  example_name = script [: -3]
  rst_file_name = rst_dest_path + example_name + ".rst"
  rst = open (rst_file_name, "w")
  rst . write (".. _" + script + ":\n")
  rst . write ("\n")
  rst . write (script + "\n")
  rst . write ((len (script) * "-") + "\n")
  rst . write ("\n")
  rst . write (".. image:: " + image_file_path + example_name + ".svg" + "\n")
  rst . write ("\n")
  rst . write (".. literalinclude:: " + examples_source_path + script)
  rst . write ("\n")
  rst . close ()


