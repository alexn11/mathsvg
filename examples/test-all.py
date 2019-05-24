# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License



import subprocess

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
  "put-text-example.py",
  "scribble.py",
  "torus.py",
  "wigglier-potato.py",
  "wiggly-potato.py",
]








for script in test_scripts:
  subprocess . call (["python", script])


