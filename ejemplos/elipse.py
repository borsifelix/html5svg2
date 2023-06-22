import math
from pathlib import Path

from html5svg2 import SVG2, elipse

svg = SVG2('ajustable', W=330, H=130, letra="Consolas", color_fondo="rgb(250,250,230)")
svg.cuadricula(10, style="stroke:SlateBlue;stroke-width:0.1px;")

stl1 = "stroke:blue;stroke-width:0.5;fill:gold;opacity:0.6;"
stl2 = "stroke:red;stroke-width:1.5;fill:OrangeRed;opacity:0.3;"
xo = 165
yo = 65
rd = 30
n = 3
ang = 2 * math.pi / n
svg.dibujar(elipse((xo, yo), 25, 25, 0, style=stl1))
for i in range(n):
	x = xo + rd * math.cos(ang * i)
	y = yo + rd * math.sin(ang * i)
	angr = i * 360 / n
	svg.dibujar(elipse((x, y), 30, 10, angr, style=stl2))

svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
