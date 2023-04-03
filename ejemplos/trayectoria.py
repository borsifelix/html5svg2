from pathlib import Path

from html5svg2 import SVG2, trayectoria

svg = SVG2('ajustable', W=330, H=130, letra="Consolas", color_fondo="rgb(250,250,230)")
svg.cuadricula(10, style="stroke:SlateBlue;stroke-width:0.1px;")

# Trazado de una onda
ldx = [{'M': (10, 65)}, {'q': [(20, 50), (40, 0)]}, {'q': [(20, -50), (40, 0)]}]
svg.dibujar(trayectoria(ldx, style="stroke:blue;stroke-width:1.5px;fill:none;"))

# Trazado de una aríbalo inca
ldx = [
	{'M': (140, 120)}, {'q': [(-4, 0), (-4, -2)]}, {'q': [(0, -2), (4, -2)]},
	{'q': [(10, 0), (10, -30)]}, {'q': [(-20, -10), (-20, -40)]},
	{'q': [(-5, 0), (-5, -5)]}, {'q': [(0, -5), (5, -5)]},
	{'q': [(0, -20), (25, -20)]},
	{'q': [(5, -5), (10, 0)]},	 # base
	{'q': [(25, 0), (25, 20)]},
	{'q': [(5, 0), (5, 5)]}, {'q': [(0, 5), (-5, 5)]},
	{'q': [(0, 30), (-20, 40)]}, {'q': [(0, 30), (10, 30)]},
	{'q': [(4, 0), (4, 2)]}, {'q': [(0, 2), (-4, 2)]},
	{'z': ''}
]
svg.dibujar(trayectoria(ldx, style="stroke:peru;stroke-width:0.75px;fill:orange;"))

# Trazado de un anillo. Lo 'hueco' se obtiene con fill-rule:evenodd;
ldx = [
	{'M': (240, 65)}, {'a': [(35, 35), 0, 0, 1, (70, 0)]}, 	{'a': [(35, 35), 0, 0, 1, (-70, 0)]},
	{'M': (250, 65)}, {'a': [(25, 25), 0, 0, 1, (50, 0)]}, 	{'a': [(25, 25), 0, 0, 1, (-50, 0)]},
]
svg.dibujar(trayectoria(ldx, style="stroke:blue;stroke-width:1.5px;fill:cyan;fill-rule:evenodd;"))

svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
