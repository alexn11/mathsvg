# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2019-05-18
# Copyright (C) 2019, Alexandre De Zotti
# License: MIT License



import subprocess

test_scripts = [
  [ "cantor-bouquet.py", "disconnected-straight-brush" ],
  [ "cantor-bouquet.py", "compact-cantor-bouquet" ],
  [ "cantor-bouquet.py", "one-sided-hairy-circle" ],
  [ "selfsim-triforce.py", ],
]








for script_params in test_scripts:
  subprocess . call (["python", ] + script_params)


