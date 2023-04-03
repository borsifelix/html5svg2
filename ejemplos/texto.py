from pathlib import Path

from html5svg2 import SVG2, texto, trayectoria

svg = SVG2('ajustable', W=330, H=150, letra="Consolas", color_fondo="rgb(250,250,230)")
svg.cuadricula(10, style="stroke:SlateBlue;stroke-width:0.1px;")
ldx = [
	{'M': (20, 120)}, {'h': 290}, {'M': (20, 140)}, {'h': 290}, {'M': (80, 5)}, {'v': 80},
	{'M': (190, 20)}, {'h': 130}, {'M': (190, 40)}, {'h': 130}, {'M': (190, 60)}, {'h': 130},
	{'M': (190, 80)}, {'h': 130},
]
stl_ = "stroke:none;fill:royalblue;font-family:Arial;"
stl_1 = f"{stl_}font-size:20px;"
stl_2 = f"{stl_}font-size:10px;"

txt = "20px: abc ABC jql Ñ/Q Ó 0 .. 9"
l_db = [
	trayectoria(ldx, style="stroke:red;stroke-width:0.25px;"),
	texto((165, 120), txt, style=f"{stl_1} text-anchor:middle;"),
	texto((80, 100), "Alineamiento horizontal:", style=f"{stl_2} text-anchor:middle;font-weight:bold"),
	texto((80, 70), "predefinido", style=f"{stl_2}"),
	texto((80, 50), "text-anchor:middle", style=f"{stl_2} text-anchor:middle;"),
	texto((80, 30), "text-anchor:end", style=f"{stl_2} text-anchor:end;"),
	texto((80, 10), "text-anchor:start", style=f"{stl_2} text-anchor:start;"),
	texto((250, 100), "Alineamiento vertical:", style=f"{stl_2} text-anchor:middle;font-weight:bold"),
	texto((190, 80), "dominant-baseline:auto", style=f"{stl_2} dominant-baseline:auto;"),
	texto((190, 60), "dominant-baseline:middle", style=f"{stl_2} dominant-baseline:middle;"),
	texto((190, 40), "dominant-baseline:central", style=f"{stl_2} dominant-baseline:central;"),
	texto((190, 20), "dominant-baseline:hanging", style=f"{stl_2} dominant-baseline:hanging;"),
	texto((165, 75), "texto rotado", ang=45, style=f"{stl_2} text-anchor:middle;"),
]

for db in l_db:
	svg.dibujar(db)
	
svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")