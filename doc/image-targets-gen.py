
test_scripts = [
  "arrows.py",
  "curved-arrows.py",
  "dashes.py",
  "graphs.py",
  "interpolated-curves.py",
  "lines.py",
  "more-curved-arrows.py",
  "multiple-save.py",
  "parametric-graphs.py",
  "points-crosses-circles-ellipses.py",
  "potato.py",
  "potato-3v.py",
  "potato-regions.py",
  "scribble.py",
  "torus.py",
  "wigglier-potato.py",
  "wiggly-potato.py",
]


size = 250

text = ""

for script in test_scripts:
  name = script [:-3]
  text += (".. image:: ../../examples/examples-images/" + name + ".svg\n")
  text += ("   :width: " + str (size) + "px\n")
  text += ("   :height:  " + str (size) + "px\n")
  text += ("   :target: examples/" + name + ".html\n")
  text += ("\n")


res_rst = open ("source/image-targets.rst", "w")
res_rst . write (text)
res_rst . close ()

