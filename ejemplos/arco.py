from pathlib import Path

from html5svg2 import SVG2, arco_circular, arco_eliptico

svg = SVG2('ajustable', W=330, H=130, letra="Consolas", color_fondo="rgb(250,250,230)")
svg.cuadricula(10, style="stroke:SlateBlue;stroke-width:0.1px;")
st1 = "fill:none;stroke:blue;stroke-width:2px;"
st2 = "fill:none;stroke:red;stroke-width:2px;"

l_db = [
	arco_circular((80, 65), 50, 00, 120, style=st1),
	arco_circular((80, 65), 50, 120, 360, style=st2),
	arco_eliptico((245, 65), 50, 30, 0, 290, style=st1),
	arco_eliptico((245, 65), 50, 30, 290, 360, style=st2)
]

for db in l_db:
	svg.dibujar(db)
	
svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
