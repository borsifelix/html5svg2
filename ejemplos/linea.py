from pathlib import Path

from html5svg2 import SVG2, linea

svg = SVG2('ajustable', W=330, H=130, letra="Consolas", color_fondo="rgb(240,250,240)")
svg.cuadricula(10, style="stroke:green;stroke-width:0.1px;")

l_db = [
	linea((10, 90), (150, 120), style="stroke:red;stroke-width:0.5px;"),
	linea((10, 70), (150, 100), style="stroke:red;stroke-width:5px;"),
	linea((10, 50), (150, 80), style="stroke:red;stroke-width:10px;"),
	linea((10, 30), (150, 60), style="stroke:blue;"),
	linea((10, 10), (150, 40), style="stroke:black;"),
	linea((180, 100), (320, 100), style="stroke:black;stroke-dasharray:10 2"),
	linea((180, 80), (320, 80), style="stroke:black;stroke-dasharray:10 5"),
	linea((180, 60), (320, 60), style="stroke:black;stroke-dasharray:5"),
	linea((180, 40), (320, 40), style="stroke:black;stroke-dasharray:10"),
	linea((180, 20), (320, 20), style="stroke:black;"),
]

for db in l_db:
	svg.dibujar(db)

svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
