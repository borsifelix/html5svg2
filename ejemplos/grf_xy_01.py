from pathlib import Path

from html5svg2 import GRF

dt = dict(
	tipo="xy",
	rotulos={
		'grf': {'txt': "Título Gráfico", 'c': 'blue', 'f': "Broadway", 'h': 10, 'n': False, 'i': False},
		'eje-x': {'txt': "Eje X", 'c': 'red', 'h': 10},
		'eje-y': {'txt': "Eje Y - con rotación de 90°C - HTML5SVG2", }
	},
	valores={
		'x': {'c': 'green', 'h': 8},
		'y': {'c': 'red', 'h': 8}
	},
	series=[
		{'c': 'indigo', 'e': 3, 'vx': [5, 10, 12, 20, ], 'vy': [120, 50, 200, 250]},
		{'vx': [0, 30], 'vy': [50, 150]}
	],
	marco={
		'borde': {'e': 2, 'c': 'violet'},
		'fondo': {'c': 'white', 't': 0.5}
	}
)

try:
	grf = GRF('ajustable', W=800/2, H=500/2, letra='Open Sans')
	#grf.cuadricula(10, style="stroke:SlateBlue;stroke-width:0.1px;")
	grf.fondo(rEsq=10, eLinea={'e': 0.5, 'c': 'red'}, eArea={'c': 'gold', 't': 0.5})
	grf.procesar(dt)
	grf.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
except Exception as e:
	print(e)
