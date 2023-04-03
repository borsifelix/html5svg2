
from pathlib import Path
from html5svg2 import SVG2, texto, polilinea, rectangulo, linea

stl_fg = "fill:green;font-size:11pt;font-style:italic;text-anchor:middle;dominant-baseline:middle;"
stl_ds = "fill:navy;font-size:12pt;dominant-baseline:middle;"
stl_tx = "fill:blue;font-size:14pt;dominant-baseline:middle;"
stl_ln = "stroke:red;stroke-width:0.5;stroke-dasharray:6 2;fill:none;"
stl_cd = "fill:rgb(228, 250, 246);"

svg = SVG2(W=600, H=470, letra="Consolas")
# svg.dibujar(linea((0, 0), (540, 470), style=stl_ln))
svg.dibujar(polilinea([(100, 50), (50, 50), (50, 420), (100, 420)], style=stl_ln))
svg.dibujar(polilinea([(130, 80), (80, 80), (80, 250), (130, 250)], style=stl_ln))
svg.dibujar(polilinea([(130, 290), (80, 290), (80, 390), (130, 390)], style=stl_ln))

svg.dibujar(rectangulo((170, 310), 360, 60, style=stl_cd))
svg.dibujar(rectangulo((170, 100), 360, 130, style=stl_cd))

svg.dibujar(texto((110, 450), "&#60;!DOCTYPE html&#62;", style=stl_tx))
svg.dibujar(texto((110, 420), "&#60;html&#62;", style=stl_tx))
svg.dibujar(texto((140, 390), "&#60;head&#62;", style=stl_tx))
svg.dibujar(texto((140, 290), "&#60;&#47;head&#62;", style=stl_tx))
svg.dibujar(texto((140, 250), "&#60;body&#62;", style=stl_tx))
svg.dibujar(texto((140, 80), "&#60;&#47;body&#62;", style=stl_tx))
svg.dibujar(texto((110, 50), "&#60;&#47;html&#62;", style=stl_tx))

svg.dibujar(texto((190, 350), "Bloque de codificación para", style=stl_ds))
svg.dibujar(texto((190, 325), "metadatos, referencias, estilos, etc.", style=stl_ds))

svg.dibujar(texto((190, 200), "Bloque de codificación para", style=stl_ds))
svg.dibujar(texto((190, 175), "mostrar el contenido de la", style=stl_ds))
svg.dibujar(texto((190, 150), "página web.", style=stl_ds))

svg.dibujar(texto((300, 15), "Estructura básica de un documento HTML", style=stl_fg))

svg.gravar(f"../docs/imgs/{Path(__file__).stem}.svg")
