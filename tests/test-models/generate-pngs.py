# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2020-01-31
# Copyright (C) 2020, Alexandre De Zotti
# License: MIT License


import cairosvg
import glob





svg_files = glob.glob("./*.svg")

for svg_file in svg_files:
  cairosvg.svg2png(file_obj = open(svg_file, "rb"), write_to = svg_file[:-3] + "png")




