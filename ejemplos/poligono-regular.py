from pathlib import Path
from html5svg2 import SVG2, poligono_regular

svg = SVG2('ajustable', W=330, H=130, letra="Consolas", color_fondo="rgb(250,250,230)")
svg.cuadricula(10, style="stroke:SlateBlue;stroke-width:0.1px;")

l_db = [
	poligono_regular((80, 65), 5, 60, 18, style="fill:gold;stroke:crimson;"),
	poligono_regular((80, 65), 4, 40, 45, style="fill:yellow;stroke:blue;"),
	poligono_regular((80, 65), 3, 20, -30, style="fill:lime;stroke:green;"),
	poligono_regular((250, 65), 10, 60, 18, style="fill:gold;stroke:crimson;"),
	poligono_regular((250, 65), 8, 40, 22.5, style="fill:yellow;stroke:blue;"),
	poligono_regular((250, 65), 6, 20, 0, style="fill:lime;stroke:green;"),
]

for db in l_db:
	svg.dibujar(db)
	
svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
