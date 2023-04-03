import json
from pathlib import Path

from html5svg2 import SVG2, trayectoria

svg = SVG2('ajustable', W=1200, H=600, letra="Consolas", color_fondo="goldenrod")

with open('jirish-nazca.json') as js:
	ldx = json.load(js)
	
svg.dibujar(trayectoria(ldx, style="fill:none;stroke:white;stroke-width:2px;"))

svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
