from pathlib import Path

from html5svg2 import SVG2, rectangulo

svg = SVG2('ajustable', W=330, H=130, letra="Consolas", color_fondo="rgb(250,250,230)")
svg.cuadricula(10, style="stroke:SlateBlue;stroke-width:0.1px;")

stl = "fill:PaleGreen;opacity:0.5;stroke:green;stroke-width:0.5px;"
stl2 = "fill:yellow;opacity:0.5;stroke:magenta;stroke-width:1.5px;"
l_db = [
	rectangulo((20, 20), 50, 30, style=stl),
	rectangulo((20, 80), 50, 30, rx=5, style=stl),
	rectangulo((100, 80), 50, 30, rx=10, ry=5, style=stl),
	rectangulo((100, 20), 50, 30, rx=5, ry=10, style=stl),
	rectangulo((220, 20), 80, 50, style=stl2),
	rectangulo((220, 20), 80, 50, ang=30, style=stl2),
	rectangulo((220, 20), 80, 50, ang=60, style=stl2),
]

for db in l_db:
	svg.dibujar(db)

svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
