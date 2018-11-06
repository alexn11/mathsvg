# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License


import setuptools

setuptools . setup (name = "mathsvg",
                    version = "0.0.1",
                    description = "Mathematics oriented SVG creation",
                    url = "http://github.com/alexn11/mathsvg",
                    author = "Alexandre De Zotti",
                    author_email = "alexn11.gh@gmail.com",
                    license = "MIT",
                    packages = setuptools . find_packages (),
                    classifiers = [
                      "Programming Language :: Python :: 3",
                      "License :: OSI Approved :: MIT License",
                      "Operating System :: OS Independent",
                    ],
                    install_requires = [
                      "svgwrite",
                    ])

