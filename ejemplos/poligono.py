from pathlib import Path

from html5svg2 import SVG2, poligono

svg = SVG2('ajustable', W=330, H=130, letra="Consolas", color_fondo="rgb(250,250,230)")
svg.cuadricula(10, style="stroke:SlateBlue;stroke-width:0.1px;")
pts_1 = [(130, 30), (80, 30), (80, 10), (10, 65), (80, 120), (80, 100), (130, 100)]
pts_2 = [(200, 30), (250, 30), (250, 10), (320, 65), (250, 120), (250, 100), (200, 100)]
svg.dibujar(poligono(pts_1, style="fill:none;stroke:blue;"))
svg.dibujar(poligono(pts_2, style="fill:gold;stroke:blue;"))
svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
