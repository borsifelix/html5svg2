from pathlib import Path

from html5svg2 import SVG2, circulo, linea

svg = SVG2('ajustable', W=330, H=130, letra="Consolas", color_fondo="rgb(250,250,230)")
svg.cuadricula(10, style="stroke:SlateBlue;stroke-width:0.1px;")
st1 = "fill:none;stroke:blue;stroke-width:2px;"
st2 = "fill:none;stroke:red;stroke-width:2px;"
st3 = "fill:red;stroke:red;"

po = (165, 65)
px = (220, 65)

l_db = [
	linea(po, px, style=st2),
	circulo(px, 3, style=st3),
	circulo(px, 10, style=st1),
]

for ang in [60, 180, 300]:
	svg.rotar(po, ang, l_db)

svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
