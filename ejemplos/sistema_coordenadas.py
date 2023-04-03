from html5svg2 import SVG2, rectangulo, polilinea
from html5svg2.prg import texto, circulo, poligono

stl_r = "fill:yellowgreen;opacity:0.15;"
stl_l = "stroke:blue;stroke-width:1.5;fill:none;"
stl_t = "fill:blue;font-size:14pt;text-anchor:middle;dominant-baseline:hanging;"
stl_c1 = "dominant-baseline:hanging;"
stl_xy = "stroke:red;stroke-width:0.5;stroke-dasharray:6 2;fill:none;"

svg = SVG2(W=1000, H=360, letra="Montserrat")
# estilo
lst = [
	"@import url('http://fonts.googleapis.com/css?family=Montserrat|Baumans|Belleza|Josefin Sans:300,600');"
]
svg.estilo(lst)
# marcas
ldb = [circulo((5, 5), 4, style="fill:red;stroke:none;")]
svg.marca("pto", (5, 5), 10, 10, 'auto', ldb)
ldb = [circulo((5, 5), 4, style="fill:navy;stroke:none;")]
svg.marca("xy", (5, 5), 10, 10, 'auto', ldb)
ldb = [poligono([(2, 4), (12, 7), (2, 10)], style="fill:blue;stroke:none;")]
svg.marca("flecha", (5, 7), 14, 14, 'auto-start-reverse', ldb)

jx = {'style': stl_l, 'marker-start': "url(#flecha)", 'marker-mid': "url(#pto)", 'marker-end': "url(#flecha)"}

svg.dibujar(rectangulo((50, 50), 400, 300, style=stl_r))
svg.dibujar(polilinea([(50, 50), (50, 350), (450, 350)], **jx))
svg.dibujar(polilinea([(250, 350), (250, 200), (50, 200)], **{'style': stl_xy, 'marker-mid': "url(#xy)"}))
svg.dibujar(texto((250, 40), "Sistema de coordenadas SVG", style=stl_t))
svg.dibujar(texto((55, 345), "(0, 0)", style=stl_c1))
svg.dibujar(texto((255, 195), "(x, y)", style=stl_c1))

svg.dibujar(rectangulo((550, 50), 400, 300, style=stl_r))
svg.dibujar(polilinea([(550, 350), (550, 50), (950, 50)], **jx))
svg.dibujar(polilinea([(750, 50), (750, 200), (550, 200)], **{'style': stl_xy, 'marker-mid': "url(#xy)"}))
svg.dibujar(texto((750, 40), "Sistema de coordenadas cartesianas", style=stl_t))
svg.dibujar(texto((555, 55), "(0, 0)", ))
svg.dibujar(texto((755, 205), "(x, y)", ))

svg.gravar("../docs/imgs/sistema_coordenadas.svg")

