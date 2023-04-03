import math
from pathlib import Path

from html5svg2 import SVG2, circulo

svg = SVG2('ajustable', W=330, H=130, letra="Consolas", color_fondo="rgb(250,250,230)")
svg.cuadricula(10, style="stroke:SlateBlue;stroke-width:0.1px;")

stl1 = "stroke:blue;stroke-width:0.5;fill:gold;opacity:0.6;"
stl2 = "stroke:blue;stroke-width:0.75;fill:cyan;opacity:0.3;"
xo = 165
yo = 65
rd = 50
n = 24
ang = 2 * math.pi / n
sn = math.sin(ang / 2)
r = rd * sn
svg.dibujar(circulo((xo, yo), rd - r, style=stl1))
for i in range(n):
	x = xo + rd * math.cos(ang * i)
	y = yo + rd * math.sin(ang * i)
	svg.dibujar(circulo((x, y), r, style=stl2))

svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
