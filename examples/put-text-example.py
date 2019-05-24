# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2019-05-25
# Copyright (C) 2019, Alexandre De Zotti
# License: MIT License

import mathsvg

image = mathsvg . SvgImage (view_window = ((0., 0.), (4., 4.)), pixel_density = 100)
image . draw_circle ((1., 3.), 0.6)
image . draw_circle ((3., 3.), 0.6)
image . draw_circle ((1., 1.), 0.6)
image . draw_arrow ((1., 1.7), (1., 2.3))
image . draw_arrow ((1.5, 1.5), (2.5, 2.5))
image . draw_arrow ((1.7, 3.), (2.3, 3.))
image . put_text ("Z", (.9, .9), font_size = 30)
image . put_text ("A", (.9, 2.9), font_size = 30)
image . put_text ("B", (2.9, 2.9), font_size = 30)

image . save ("put-text-example.svg")
