# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 18:11:20 2023

@author: Borsi Romero
"""
import math
from datetime import datetime

# import numpy as np

from html5svg2.utl import vrf, divgrf, grf_xy_limites, g_rotulo, grf_xy_stl, wtxt, str_num, g_marco, g_fondo, stl_linea, \
	stl_fondo, stl_divxy


def __dTag(tag, txt, **js):
	#
	p = "".join(f' {k}="{js[k]}"' for k in js)
	s = f"<{tag}{p}>{txt}</{tag}>"
	return [s]


def __dTagl(tag, ls, **js):
	#
	p = "".join(f' {k}="{js[k]}"' for k in js)
	rs = [f"<{tag}{p}>"]
	for tx in ls:
		rs.append(f"  {tx}")
	rs.append(f"</{tag}>")
	return rs


def dTag(tag, obj, **js):
	"""
	Codifica lenguaje de marcado tipo <tag clave1="valor1" .. > obj </tag>
	:param tag: nombre. Ej. h1.
	:param obj: texto o lista de textos.
	:param js: diccionario de parámetros. Ej. {'id':'ID01', }
	:return: list
	"""
	if type(obj).__name__ == 'list':
		rs = __dTagl(tag, obj, **js)
	else:
		rs = __dTag(tag, obj, **js)
	return rs


def dEtq(etq, **js):
	"""
	Codifica lenguaje de marcado tipo <etiqueta clave1="valor1" .. />
	:param etq: nombre de etiqueta.
	:param js: diccionario de parámetros. Ej. {'color': 'blue', }
	:return: list
	"""
	p = "".join(f' {k}="{js[k]}"' for k in js)
	p = f"<{etq}{p} />"
	return [p]


def dCmt(obj):
	"""
	Codifica comentario tipo <!-- este es un comentario -->
	:param obj: texto o lista de textos.
	:return: list
	"""
	if type(obj).__name__ == 'list':
		if len(obj) == 0:
			ls = []
		elif len(obj) == 1:
			ls = [f"<!-- {obj[0]} -->"]
		else:
			ls = ["<!--"]
			for tx in obj:
				ls.append(f"  {tx}")
			ls.append("-->")
	else:
		ls = [f"<!-- {obj} -->"]
	return ls


def cdg(etq, jx, js):
	for k, v in jx.items():
		js[k] = v
	return dEtq(etq, **js)


def __obj(nombre, jx, js):
	for k, v in jx.items():
		js[k] = v
	return dict(obj=nombre, arg=js)


def title(tx, **jx):
	try:
		js = {'txt': tx}
		return __obj('title', jx, js)
	except Exception as e:
		raise Exception(f"ERROR(title)> {e}")


def linea(p1, p2, **jx):
	try:
		x1, y1 = p1
		x2, y2 = p2
		js = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
		return __obj('line', jx, js)
	except Exception as e:
		raise Exception(f"ERROR(linea)> {e}")


def rectangulo(px, w, h, **jx):
	try:
		x, y = px
		js = {'x': x, 'y': y, 'width': w, 'height': h}
		if 'ang' not in jx:
			js['ang'] = 0
		return __obj('rect', jx, js)
	except Exception as e:
		raise Exception(f"ERROR(rectangulo)> {e}")


def circulo(po, r, **jx):
	try:
		x, y = po
		js = {'cx': x, 'cy': y, 'r': r}
		return __obj('circle', jx, js)
	except Exception as e:
		raise Exception(f"ERROR(circulo)> {e}")


def elipse(po, rx, ry, ang, **jx):
	try:
		cx, cy = po
		js = {'cx': cx, 'cy': cy, 'rx': rx, 'ry': ry, 'ang': ang}
		return __obj('ellipse', jx, js)
	except Exception as e:
		raise Exception(f"ERROR(elipse)> {e}")


def polilinea(pts, **jx):
	try:
		js = {'pts': pts}
		return __obj('polyline', jx, js)
	except Exception as e:
		raise Exception(f"ERROR(polilinea)> {e}")


def poligono(pts, **jx):
	try:
		js = {'pts': pts}
		return __obj('polygon', jx, js)
	except Exception as e:
		raise Exception(f"ERROR(poligono)> {e}")


def trayectoria(ldx, **jx):
	try:
		js = {'ldx': ldx}
		return __obj('path', jx, js)
	except Exception as e:
		raise Exception(f"ERROR(trayectoria)> {e}")


def arco_circular(po, r, angi, angf, **cv):
	xo, yo = po
	ai = math.radians(angi)
	af = math.radians(angf)
	xi = xo + r * math.cos(ai)
	yi = yo + r * math.sin(ai)
	xf = xo + r * math.cos(af)
	yf = yo + r * math.sin(af)
	laf = 0
	if angf - angi > 180:
		laf = 1
	ltr = [
		{'M': (xi, yi)},
		{'A': [(r, r), 0, laf, 0, (xf, yf)]}
	]
	return trayectoria(ltr, **cv)


def arco_eliptico(po, rx, ry, angi, angf, **cv):
	xo, yo = po
	ai = math.radians(angi)
	af = math.radians(angf)
	#
	r = 1 / math.sqrt((math.cos(ai) / rx) ** 2 + (math.sin(ai) / ry) ** 2)
	xi = xo + r * math.cos(ai)
	yi = yo + r * math.sin(ai)
	#
	r = 1 / math.sqrt((math.cos(af) / rx) ** 2 + (math.sin(af) / ry) ** 2)
	xf = xo + r * math.cos(af)
	yf = yo + r * math.sin(af)
	
	laf = 0
	if angf - angi > 180:
		laf = 1
	ltr = [
		{'M': (xi, yi)},
		{'A': [(rx, ry), 0, laf, 0, (xf, yf)]}
	]
	return trayectoria(ltr, **cv)


def poligono_regular(po, n, r, ang, **cv):
	xo, yo = po
	ai = math.radians(ang)
	an = math.pi * 2 / n
	lp = []
	for i in range(n):
		ax = ai + an * i
		x = xo + r * math.cos(ax)
		y = yo + r * math.sin(ax)
		lp.append((x, y))
	return poligono(lp, **cv)


def texto(px, tx, **jx):
	try:
		x, y = px
		js = {'x': x, 'y': y, 'txt': tx}
		if 'ang' not in jx:
			js['ang'] = 0
		return __obj('text', jx, js)
	except Exception as e:
		raise Exception(f"ERROR(texto)> {e}")


def xx__estilo(**cv):
	esp = 0
	# -- estilo de linea -- #
	eLn = ""
	k = 'eLinea'
	if k in cv:
		o = cv[k]
		# -- color de linea -->
		c = 'none'
		if 'c' in o:
			c = o['c']
		eLn += f"stroke:{c};"
		# -- espesor de linea -->
		e = 1
		if 'e' in o:
			e = o['e']
		eLn += f"stroke-width:{e}px;"
		esp = e
	# -- estilo de área -- #
	eAr = ""
	k = 'eArea'
	if k in cv:
		o = cv[k]
		# -- color del area -->
		c = 'none'
		if 'c' in o:
			c = o['c']
		eAr += f"fill:{c};"
		# -- transparencia -->
		if 't' in o:
			eAr += f"opacity:{o['t']}"
	#
	return esp, eLn, eAr


class HTML5:
	def __init__(s):
		s.lh = []  # lista de objetos contenidos en head
		s.lb = []  # lista de objetos contenidos en body
	
	def cabecera(s, o):
		if type(o).__name__ == 'list':
			s.lh.extend(o)
		else:
			s.lh.append(o)
	
	def contenido(s, o):
		if type(o).__name__ == 'list':
			s.lb.extend(o)
		else:
			s.lb.append(o)
	
	def listado(s):
		lo = ['<!DOCTYPE html>']
		ls = dCmt('cabecera')
		ls.extend(dTag('head', s.lh))
		ls.append('')
		ls.extend(dCmt('contenido'))
		ls.extend(dTag('body', s.lb))
		ls.append('')
		lo.extend(dTag('html', ls))
		lo.extend(dCmt(f'Generado por HTML5SVG5 {datetime.now()}'))
		return lo
	
	def gravar(s, arch):
		lo = s.listado()
		with open(arch, mode='w', encoding='utf-8') as f:
			for tx in lo:
				f.write(f"{tx}\n")


class SVG2:
	
	def __init__(s, *ld, **js):
		s.W = 800
		s.H = 500
		s.lst = []  # lista de estilos
		s.lmk = []  # lista de marcas
		s.ld = []  # lista de definiciones
		s.lc = []  # lista de contenido
		if 'W' in js:
			s.W = js['W']
		if 'H' in js:
			s.H = js['H']
		s.Wo = s.W
		s.Ho = s.H
		s.letra = None
		if 'letra' in js:
			s.letra = js['letra']
		s.color_fondo = None
		if 'color_fondo' in js:
			s.color_fondo = js['color_fondo']
		s.color_linea = 'black'
		if 'color_linea' in js:
			s.color_linea = js['color_linea']
		s.ajustable = False
		if 'ajustable' in ld:
			s.ajustable = True
		s.__gravar = True
	
	def __codigo(s):
		ld = dTag('style', s.lst, **{'type': 'text/css'})
		ld.extend(s.lmk)
		ls = dTag('defs', ld)
		ls.extend(s.lc)
		return ls
	
	def __arg(s, **d):
		#
		jx = {}
		if 'id' in d:
			jx['id'] = d['id']
		if 'x' in d:
			jx['x'] = d['x']
		if 'y' in d:
			jx['y'] = d['y']
		if s.ajustable:
			jx['width'] = '100%'
			jx['height'] = '100%'
		else:
			jx['width'] = s.Wo
			jx['height'] = s.Ho
		jx['viewBox'] = f'0 0 {s.W} {s.H}'
		#
		if s.letra is not None:
			jx['font-family'] = s.letra
		#
		stl = f"stroke:{s.color_linea};"
		if s.color_fondo is not None:
			stl = f"background-color:{s.color_fondo};{stl}"
		jx['style'] = stl
		#
		if s.__gravar:
			jx['xmlns'] = "http://www.w3.org/2000/svg"
			jx['xmlns:xlink'] = "http://www.w3.org/1999/xlink"
		#
		return jx
	
	def exp(s, **d):
		#
		s.__gravar = False
		jx = s.__arg(**d)
		return dTag('svg', s.__codigo(), **jx)
	
	def gravar(s, arch, **d):
		try:
			jx = s.__arg(**d)
			ls = dTag('svg', s.__codigo(), **jx)
			with open(arch, 'w', encoding='utf-8') as f:
				for o in ls:
					f.write(f"{o}\n")
		except Exception as e:
			raise Exception(e)
	
	def svg_xy(s, jo):
		try:
			obj = jo['obj']
			jx = jo['arg']
			
			id_obj = 'title'
			if obj == id_obj:
				txt = jx['txt']
				return dTag(id_obj, txt)
			
			id_obj = 'text'
			if obj == id_obj:
				txt = jx['txt']
				jx['y'] = s.H - jx['y']
				if jx['ang'] != 0:
					jx['transform'] = f"rotate({-jx['ang']},{jx['x']},{jx['y']})"
				del jx['ang']
				del jx['txt']
				return dTag(id_obj, txt, **jx)
			
			id_obj = 'line'
			if obj == id_obj:
				jx['y1'] = s.H - jx['y1']
				jx['y2'] = s.H - jx['y2']
				return dEtq(id_obj, **jx)
			
			id_obj = 'rect'
			if obj == id_obj:
				jx['y'] = s.H - jx['y'] - jx['height']
				if jx['ang'] != 0:
					jx['transform'] = f"rotate({-jx['ang']},{jx['x']},{jx['y'] + jx['height']})"
				del jx['ang']
				return dEtq(id_obj, **jx)
			
			id_obj = 'circle'
			if obj == id_obj:
				jx['cy'] = s.H - jx['cy']
				return dEtq(id_obj, **jx)
			
			id_obj = 'ellipse'
			if obj == id_obj:
				jx['cy'] = s.H - jx['cy']
				if jx['ang'] != 0:
					jx['transform'] = f"rotate({-jx['ang']},{jx['cx']},{jx['cy']})"
				del jx['ang']
				return dEtq(id_obj, **jx)
			
			id_obj = 'polyline'
			if obj == id_obj:
				pts = jx['pts']
				jx['points'] = " ".join(f"{x},{s.H - y}" for x, y in pts)
				del jx['pts']
				return dEtq(id_obj, **jx)
			
			id_obj = 'polygon'
			if obj == id_obj:
				pts = jx['pts']
				jx['points'] = " ".join(f"{x},{s.H - y}" for x, y in pts)
				del jx['pts']
				return dEtq(id_obj, **jx)
			
			id_obj = 'path'
			if obj == id_obj:
				ldx = jx['ldx']
				#
				d = ""
				for dx in ldx:
					for k, v in dx.items():
						if k in ['Z', 'z']:
							d += f"{k} "
						if k in ['H', 'h']:
							d += f"{k} {v} "
						if k == 'V':
							d += f"{k} {s.H - v} "
						if k == 'v':
							d += f"{k} {-v} "
						if k in ['M', 'L', 'T']:
							d += f"{k} {v[0]},{s.H - v[1]} "
						if k in ['m', 'l', 't']:
							d += f"{k} {v[0]},{- v[1]} "
						if k in ['Q', 'S']:
							d += f"{k} {v[0][0]},{s.H - v[0][1]} {v[1][0]},{s.H - v[1][1]} "
						if k in ['q', 's']:
							d += f"{k} {v[0][0]},{- v[0][1]} {v[1][0]},{- v[1][1]} "
						if k == 'C':
							d += f"{k} {v[0][0]},{s.H - v[0][1]} {v[1][0]},{s.H - v[1][1]} {v[2][0]},{s.H - v[2][1]} "
						if k == 'A':
							d += f"{k} {v[0][0]},{v[0][1]} {v[1]} {v[2]} {v[3]} {v[4][0]},{s.H - v[4][1]} "
						if k == 'a':
							d += f"{k} {v[0][0]},{v[0][1]} {v[1]} {v[2]},{v[3]} {v[4][0]},{-v[4][1]} "
				jx['d'] = d
				#
				del jx['ldx']
				return dEtq(id_obj, **jx)
			# print(obj)
			raise Exception(f"El objeto '{obj}' no está implementado")
		except Exception as e:
			raise Exception(f"ERROR(SVG2.svg_xy)> {e}")
	
	def dibujar(s, jd):
		try:
			s.lc.extend(s.svg_xy(jd))
		except Exception as e:
			raise Exception(f"ERROR(SVG2.dibujar)> {e}")
	
	def agrupar(s, ljd, **jx):
		try:
			ls = []
			for jd in ljd:
				ls.extend(s.svg_xy(jd))
			s.lc.extend(dTag('g', ls, **jx))
		except Exception as e:
			raise Exception(f"ERROR(SVG2.grupo)> {e}")
	
	def marca(s, id, xy, mw, mh, orn, ldb):
		try:
			x, y = xy
			js = {
				'id': id,
				'viewBox': f"-1 -1 {mw + 2} {mh + 2}",
				'markerWidth': mw,
				'markerHeight': mh,
				'refX': x,
				'refY': y,
				'orient': orn
			}
			
			lo = []
			for jo in ldb:
				obj = jo['obj']
				jx = jo['arg']
				if obj == 'polygon':
					pts = jx['pts']
					jx['points'] = " ".join(f"{x},{y}" for x, y in pts)
					del jx['pts']
				
				lo.extend(dEtq(obj, **jx))
			
			ls = dTag('marker', lo, **js)
			s.lmk.extend(ls)
		except Exception as e:
			raise Exception(f"ERROR(SVG2.marca)> {e}")
	
	def estilo(s, obj):
		try:
			if type(obj).__name__ == 'list':
				s.lst.extend(obj)
			else:
				s.lst.append(obj)
		except Exception as e:
			raise Exception(f"ERROR(SVG2.estilo)> {e}")
	
	def lineaV(s, x, **jx):
		try:
			p1 = (x, 0)
			p2 = (x, s.H)
			s.dibujar(linea(p1, p2, **jx))
		except Exception as e:
			raise Exception(f"ERROR(SVG2.lineaV)> {e}")
	
	def lineaH(s, y, **jx):
		try:
			p1 = (0, y)
			p2 = (s.W, y)
			s.dibujar(linea(p1, p2, **jx))
		except Exception as e:
			raise Exception(f"ERROR(SVG2.lineaH)> {e}")
	
	def cuadricula(s, w, **jx):
		try:
			# lineas verticales
			m = int(s.W / w)
			x = 0
			for i in range(m):
				x = w * i
				s.lineaV(x, **jx)
			if x != s.W:
				s.lineaV(s.W, **jx)
			# lineas horizontales
			n = int(s.H / w)
			y = 0
			for i in range(n):
				y = w * i
				s.lineaH(y, **jx)
			if y != s.H:
				s.lineaH(s.H, **jx)
		except Exception as e:
			raise Exception(f"ERROR(SVG2.cuadricula)> {e}")
	
	def rotar(self, po, ang, l_db):
		x, y = po
		jx = {'transform': f"rotate({-ang},{x},{self.H - y})"}
		self.agrupar(l_db, **jx)
	
	def grafico(s, po, ang, grf):
		assert grf.__class__.__name__ == 'GRF', "ERROR(SVG.grafico)> Se esperaba la clase GRF"
		xo, yo = po
		s.lc.extend(grf.exp(x=xo, y=s.H - (yo + grf.H)))


class GRF(SVG2):
	def __init__(self, *ld, **js):
		super().__init__(*ld, **js)
		self.MRG_DER = 10
		self.MRG_IZQ = 10
		self.MRG_SUP = 10
		self.MRG_INF = 10
		self.MRG_INT = 10
		self.FKT = 1.5  # ratio alto caja texto / alto letra.
		self.HTLG = 0
		self.HTLX = 0
		self.HTLY = 0
		self.HVLX = 0
		self.HVLY = 0
		self.HETX = 0
		self.WVLY = 0
		self.DIVX = 50
		self.DIVY = 50
		self.lmnx = []
		self.lmxx = []
		self.lmny = []
		self.lmxy = []
		self.ttlg = {'ok': False}
		self.ttlx = {'ok': False}
		self.ttly = {'ok': False}
		self.vlrx = {'ok': True}
		self.vlry = {'ok': True}
		self.etqx = {'ok': True}
		self.divh = {'ok': True}
		self.divv = {'ok': True}
		self.lyn = {'ok': False, 'h': 15, 'wlm': 30, 'mrg': 5, 'wPnLy': 0, 'hPnLy': 0}
		self.rng = {'dx': None, 'xmn': None, 'xmx': None, 'dy': None, 'ymn': None, 'ymx': None}
		self.lc.extend(dTag('script', ['function resaltar(x,el) { x.style.strokeWidth = el; }'], ))
	
	def __fondo(self, **cv):
		#
		l_db = []
		r = 0
		k = 'r'
		if k in cv:
			r = cv[k]
		esp, eLn, eAr = g_fondo(**cv)
		
		k = 'fondo'
		if k in cv:
			jx = {}
			if r > 0:
				jx['rx'] = r
				jx['ry'] = r
			jx['style'] = f"stroke:none;{eAr}"
			l_db.append(rectangulo((esp / 2, esp / 2), self.W - esp, self.H - esp, **jx))

		k = 'borde'
		if k in cv:
			jx = {}
			if r > 0:
				jx['rx'] = r
				jx['ry'] = r
			jx['style'] = f"fill:none;{eLn}"
			l_db.append(rectangulo((esp / 2, esp / 2), self.W - esp, self.H - esp, **jx))
		
		for o in l_db:
			self.dibujar(o)
	
	def procesar(self, dt):
		try:
			#
			tipo_ = vrf('tipo', 'tipo de gráfico', dt)
			tipo = f"{tipo_}".lower()
			if tipo == 'xy':
				self.__grf_xy(dt)
			else:
				raise Exception(f"El tipo de gráfico '{tipo_}' no está implementado")
		# self.__graficar()
		except Exception as e:
			raise Exception(f"ERROR(GRF)> {e}")
	
	def __marca(self, i, d):
		id = f"mk{i}"
		e = 0.5
		if 'el' in d:
			e = d['el']
		cl = 'none'
		if 'cl' in d:
			cl = d['cl']
		cf = 'black'
		if 'cf' in d:
			cf = d['cf']
		stl = f"fill:{cf};stroke:{cl};stroke-width:{e};"
		r = 4
		if 'r' in d:
			r = d['r']
		w = 2 * r
		h = 2 * r
		nn = 0
		if 'id' in d:
			nn = d['id']
		if nn == 1:  # cuadrado
			ldb = [rectangulo((0, 0), w, h, style=stl)]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		elif nn == 2:  # rombo
			ldb = [poligono([(r, 0), (w, r), (r, h), (0, r)], style=stl)]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		elif nn == 3:  # triangulo
			ldb = [poligono_regular((r, r), 3, r, 30, style=stl)]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		elif nn == 4:  # triangulo invertido
			ldb = [poligono_regular((r, r), 3, r, -30, style=stl)]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		elif nn == 5:  # pentágono
			ldb = [poligono_regular((r, r), 5, r, -18, style=stl)]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		elif nn == 6:  # hexágono
			ldb = [poligono_regular((r, r), 6, r, 0, style=stl)]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		elif nn == 7:  # octógono
			ldb = [poligono_regular((r, r), 8, r, 0, style=stl)]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		elif nn == 8:  # --
			ldb = [poligono([(0, 0), (w, 0), (0, h), (w, h)], style=stl)]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		elif nn == 9:  # --
			ldb = [poligono([(0, 0), (w, h), (w, 0), (0, h)], style=stl)]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		elif nn == 10:  # --
			pts = [
				(0, r / 2), (r / 2, r / 2), (r / 2, 0), (1.5 * r, 0), (1.5 * r, r / 2),
				(w, r / 2), (w, 1.5 * r), (1.5 * r, 1.5 * r), (1.5 * r, h),
				(r / 2, h), (r / 2, 1.5 * r), (0, 1.5 * r)
			]
			ldb = [poligono(pts, style=stl)]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		elif nn == 11:
			d = f"M {0.75 * r}, {0.75 * r} q {0.25 * r},{-1.5 * r} {0.5 * r},0 q {1.5 * r},{0.25 * r} 0,{0.5 * r}"
			d += f" q {-0.25 * r},{1.5 * r} {-0.5 * r},0 q {-1.5 * r},{-0.25 * r} 0,{-0.5 * r} z"
			db = {'obj': 'path', 'arg': {'d': d, 'style': stl}}
			ldb = [db]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		else:
			ldb = [circulo((r, r), r, style=stl)]
			self.marca(id, (r, r), w, h, 'auto', ldb)
		return id
	
	def __grf_xy(self, dt):
		# print(self.lc)
		# -- valores extremos a partir de series -->>
		jm, lerr = grf_xy_limites(dt)
		if len(lerr) > 0:
			self.__error(lerr)
			return
		# print(jm)
		# -- dimensiones para rótulos -->>
		self.__grf_xy_dim_rotulos(dt)
		self.__grf_xy_dim_valores(jm, dt)
		self.__grf_xy_div(dt)
		self.__grf_xy_rng(dt)
		js = self.__grf_xy_dim_area(jm, dt)
		xo = js['xo']
		yo = js['yo']
		dXG = js['dXG']
		dYG = js['dYG']
		XmnV = js['XmnV']
		XmxV = js['XmxV']
		XmnG = js['XmnG']
		YmnV = js['YmnV']
		YmxV = js['YmxV']
		YmnG = js['YmnG']
		WCRV = js['WCRV']
		HCRV = js['HCRV']
		sclX = js['sclX']
		sclY = js['sclY']
		#
		if 'fondo' in dt:
			self.__fondo(**dt['fondo'])
		#
		ebr_m, efn_m = g_marco(dt)
		js['efn_m'] = efn_m
		"""| graficar ventana de gráfico xy |"""
		self.__grf_xy_svg_curvas(dt, js)
		"""
		# -- trazado de series, líneas divisorias, etc. -->>
		#
		l_db = []
		svg = SVG2(W=WCRV, H=HCRV)
		svg.dibujar(rectangulo((0, 0), WCRV, HCRV, style=efn_m))
		# -- trazado de líneas divisorias/horizontal -->>
		o = self.divh
		if o['ok']:
			w = svg.W
			ldx = []
			y = YmnG
			while y < YmxV:
				y_ = (y - YmnV) * sclY
				if y_ > 0:
					ldx.append({'M': (0, y_)})
					ldx.append({'l': (w, 0)})
				y += dYG
			l_db.append(trayectoria(ldx, style=o['stl']))
		# -- trazado de líneas divisorias/vertical -->>
		o = self.divv
		if o['ok']:
			h = svg.H
			ldx = []
			x = XmnG
			while x < XmxV:
				x_ = (x - XmnV) * sclX
				if x_ > 0:
					ldx.append({'M': (x_, 0)})
					ldx.append({'l': (0, h)})
				x += dXG
			l_db.append(trayectoria(ldx, style=o['stl']))
		
		for o in l_db:
			svg.dibujar(o)
		
		# -- trazado de series -->>
		if 'series' in dt:
			grf_xy_stl(dt['series'])
			for k, d in enumerate(dt['series']):
				pts = []
				for i in range(d['n']):
					x = (d['vx'][i] - XmnV) * sclX
					y = (d['vy'][i] - YmnV) * sclY
					pts.append((x, y))
				if 'mk' in d:
					mk = self.__marca(k, d['mk'])
					d['stl'] = f"{d['stl']}marker-start:url(#{mk});marker-mid:url(#{mk});marker-end:url(#{mk});"
				lo = [title(d['id']), polilinea(pts, style=d['stl'], onmouseover=d['over'], onmouseout=d['out'])]
				svg.agrupar(lo, id=f"sxy{k + 1}")
		
		self.lc.extend(svg.exp(x=xo, y=self.H - (yo + HCRV)))
		"""
		
		"""| graficar rotulos, valores, leyenda, etc. |"""
		l_db = []
		# -- rotulos -->>
		o = self.ttlg
		if o['ok']:
			x = xo + WCRV / 2
			y = self.H - (self.MRG_SUP + self.HTLG / 2)
			l_db.append(texto((x, y), o['txt'], style=o['stl']))
		# l_db.append(linea((xo, y), (xo + WCRV, y), style="stroke:magenta"))
		o = self.ttlx
		if o['ok']:
			x = xo + WCRV / 2
			y = yo - (self.MRG_INT + self.HVLX + self.HETX + self.HTLX / 2)
			l_db.append(texto((x, y), o['txt'], style=o['stl']))
		o = self.ttly
		if o['ok']:
			x = xo - (self.MRG_INT + self.WVLY + self.HTLY / 2)
			y = yo + HCRV / 2
			
			l_db.append(texto((x, y), o['txt'], ang=90, style=o['stl']))
		
		# -- valores x, y -->>
		w = self.MRG_INT
		# -- valores y -->>
		o = self.vlry
		if o['ok']:
			y = YmnG
			while y <= YmxV:
				y = round(y, 5)
				if y >= YmnV:
					y_ = yo + (y - YmnV) * sclY
					l_db.append(texto((xo - w, y_), f"{str_num(round(y, 5))}", style=o['stl']))
				# l_db.append(linea((xo-w, y_), (xo, y_)))
				y += dYG
		# -- valores x -->>
		o = self.vlrx
		if o['ok']:
			x = XmnG
			y = yo - self.MRG_INT  # - self.HVLX/2
			while x <= XmxV:
				x = round(x, 5)
				if x >= XmnV:
					x_ = xo + (x - XmnV) * sclX
					l_db.append(texto((x_, y), f"{str_num(x)}", style=o['stl']))
				# l_db.append(linea((x_, yo), (x_, yo - w)))
				x += dXG
		# -- etiquetas x -->>
		if 'etqx' in dt:
			y = yo - (self.MRG_INT + self.HVLX + self.HETX/2)
			for o in dt['etqx']:
				x = xo + (o[0] - XmnV) * sclX
				st = g_rotulo(10, o[2])
				l_db.append(texto((x, y), o[1], style=st['stl']))
				#print(o, x, st)
		
		# -- leyenda -->>
		self.__grf_xy_svg_leyenda(dt, xo, yo, WCRV, HCRV, l_db)
		# -- marco borde -->
		l_db.append(rectangulo((xo, yo), WCRV, HCRV, style=ebr_m))
		
		for o in l_db:
			self.dibujar(o)
	
	def __grf_xy_svg_curvas(self, dt, js):
		xo = js['xo']
		yo = js['yo']
		dXG = js['dXG']
		dYG = js['dYG']
		XmnV = js['XmnV']
		XmxV = js['XmxV']
		XmnG = js['XmnG']
		YmnV = js['YmnV']
		YmxV = js['YmxV']
		YmnG = js['YmnG']
		WCRV = js['WCRV']
		HCRV = js['HCRV']
		sclX = js['sclX']
		sclY = js['sclY']
		efn_m = js['efn_m']
		# -- trazado de series, líneas divisorias, etc. -->>
		#
		svg = SVG2(W=WCRV, H=HCRV)
		svg.dibujar(rectangulo((0, 0), WCRV, HCRV, style=efn_m))
		# -- trazado de extras en el fondo -->
		grf_xy_svg_curvas_extras(False, dt, js, svg)
		#
		l_db = []
		# -- trazado de líneas divisorias/horizontal -->>
		o = self.divh
		if o['ok']:
			w = svg.W
			ldx = []
			y = YmnG
			while y < YmxV:
				y_ = (y - YmnV) * sclY
				if y_ > 0:
					ldx.append({'M': (0, y_)})
					ldx.append({'l': (w, 0)})
				y += dYG
			l_db.append(trayectoria(ldx, style=o['stl']))
		# -- trazado de líneas divisorias/vertical -->>
		o = self.divv
		if o['ok']:
			h = svg.H
			ldx = []
			x = XmnG
			while x < XmxV:
				x_ = (x - XmnV) * sclX
				if x_ > 0:
					ldx.append({'M': (x_, 0)})
					ldx.append({'l': (0, h)})
				x += dXG
			l_db.append(trayectoria(ldx, style=o['stl']))
		# -- divisor horizontal cuando hay valores y negativos -->>
		if YmnG < 0:
			y = (0 - YmnV) * sclY
			l_db.append(trayectoria([{'M': (0, y)}, {'l': (svg.W, 0)}],))
		
		for o in l_db:
			svg.dibujar(o)
		
		# -- trazado de series -->>
		if 'series' in dt:
			grf_xy_stl(dt['series'])
			for k, d in enumerate(dt['series']):
				pts = []
				for i in range(d['n']):
					x = (d['vx'][i] - XmnV) * sclX
					y = (d['vy'][i] - YmnV) * sclY
					pts.append((x, y))
				if 'mk' in d:
					mk = self.__marca(k, d['mk'])
					d['stl'] = f"{d['stl']}marker-start:url(#{mk});marker-mid:url(#{mk});marker-end:url(#{mk});"
				lo = [title(d['id']), polilinea(pts, style=d['stl'], onmouseover=d['over'], onmouseout=d['out'])]
				svg.agrupar(lo, id=f"sxy{k + 1}")
		# -- trazado de extras en primer plano -->
		grf_xy_svg_curvas_extras(True, dt, js, svg)
		#
		self.lc.extend(svg.exp(x=xo, y=self.H - (yo + HCRV)))
		
	def __grf_xy_svg_leyenda(self, dt, xo, yo, WCRV, HCRV, l_db):
		ly = self.lyn
		if not ly['ok']:
			return
		if 'series' not in dt:
			return
		lsr = dt['series']
		hly = ly['h'] * self.FKT
		stx = f"stroke:none;font-size:{ly['h']}px;dominant-baseline:middle;"
		stl = "fill:none;stroke:red;stroke-width:0.5px;stroke-dasharray:5 2"
		if ly['ubc'] == 'der':
			xr = xo + WCRV + self.MRG_INT
			# l_db.append(rectangulo((xr, yo), ly['wPnLy'], HCRV, style=stl))
			yr = yo + (HCRV + len(lsr) * hly)/2
			for i, s in enumerate(lsr):
				x = xr + ly['mrg']
				y = yr - hly * (i + 0.5)
				slm = s['stl'].replace('marker-start', '-x-').replace('marker-end', '-y-')
				p1 = (x, y)
				p2 = (x + ly['wlm']/2, y)
				p3 = (x + ly['wlm'], y)
				l_db.append(polilinea([p1, p2, p3], style=slm))
				l_db.append(texto((x + ly['wlm'] + ly['mrg'], y), s['id'], style=stx))
		if ly['ubc'] == 'izq':
			xr = self.MRG_IZQ + ly['wPnLy']
			yr = yo + (HCRV + len(lsr) * hly) / 2
			for i, s in enumerate(lsr):
				x = xr - ly['mrg']
				y = yr - hly * (i + 0.5)
				slm = s['stl'].replace('marker-start', '-x-').replace('marker-end', '-y-')
				stx += "text-anchor:end;"
				p1 = (x, y)
				p2 = (x - ly['wlm']/2, y)
				p3 = (x - ly['wlm'], y)
				l_db.append(polilinea([p1, p2, p3], style=slm))
				l_db.append(texto((x - ly['wlm'] - ly['mrg'], y), s['id'], style=stx))
		if ly['ubc'] in ['sup', 'inf']:
			yr = 0
			if ly['ubc'] == 'sup':
				yr = yo + HCRV + self.MRG_INT + ly['hPnLy']
			if ly['ubc'] == 'inf':
				yr = self.MRG_INF + ly['hPnLy']
			# l_db.append(rectangulo((xo, yr-ly['hPnLy']), WCRV, ly['hPnLy'], style=stl))
			dy = WCRV / ly['ncol']
			for k, s in enumerate(lsr):
				i = int(k / ly['ncol'])
				j = k % ly['ncol']
				x = xo + ly['mrg'] + dy * j
				y = yr - hly * (i + 0.5)
				slm = s['stl'].replace('marker-start', '-x-').replace('marker-end', '-y-')
				p1 = (x, y)
				p2 = (x + ly['wlm'] / 2, y)
				p3 = (x + ly['wlm'], y)
				l_db.append(polilinea([p1, p2, p3], style=slm))
				l_db.append(texto((x + ly['wlm'] + ly['mrg'], y), s['id'], style=stx))
		
	def __grf_xy_rng(self, dt):
		if 'limites' in dt:
			o = dt['limites']
			k = 'xmn'
			if k in o:
				self.rng[k] = o[k]
			k = 'xmx'
			if k in o:
				self.rng[k] = o[k]
			k = 'dx'
			if k in o:
				self.rng[k] = o[k]
			k = 'ymn'
			if k in o:
				self.rng[k] = o[k]
			k = 'ymx'
			if k in o:
				self.rng[k] = o[k]
			k = 'dy'
			if k in o:
				self.rng[k] = o[k]
	
	def __grf_xy_dim_rotulos(self, dt):
		h = 20  # tamaño de letra prefijado
		if 'rotulos' in dt:
			jx = dt['rotulos']
			k = 'grf'
			if k in jx:
				self.ttlg = g_rotulo(h, jx[k])
				if self.ttlg['ok']:
					self.HTLG = self.FKT * self.ttlg['h']
			k = 'eje-x'
			if k in jx:
				self.ttlx = g_rotulo(h, jx[k])
				if self.ttlx['ok']:
					self.HTLX = self.FKT * self.ttlx['h']
			k = 'eje-y'
			if k in jx:
				self.ttly = g_rotulo(h, jx[k])
				if self.ttly['ok']:
					self.HTLY = self.FKT * self.ttly['h']
	
	def __grf_xy_dim_valores(self, jm, dt):
		h = 20  # tamaño de letra prefijado
		#
		if 'etqx' in dt:
			js = {'ok': True}
			he = h
			ls = dt['etqx']
			for lo in dt['etqx']:
				o = lo[2]
				if 'h' in o:
					if o['h'] > he: he = o['h']
				#print(lo)
			self.etqx = js
			self.HETX = self.FKT * he
			
		if 'valores' in dt:
			jx = dt['valores']
			k = 'x'
			if k in jx:
				self.vlrx = g_rotulo(h, jx[k])
			else:
				self.vlrx = g_rotulo(h, {})
			k = 'y'
			if k in jx:
				self.vlry = g_rotulo(h, jx[k])
			else:
				self.vlry = g_rotulo(h, {})
		else:
			self.vlrx = g_rotulo(h, {})
			self.vlry = g_rotulo(h, {})
		#
		if self.vlrx['ok']:
			stl = self.vlrx['stl'].replace('dominant-baseline:middle', 'dominant-baseline:hanging')
			self.vlrx['stl'] = stl
			self.HVLX = self.FKT * self.vlrx['h']
		# print(self.HVLX, self.vlrx['h'])
		if self.vlry['ok']:
			stl = self.vlry['stl'].replace('text-anchor:middle', 'text-anchor:end')
			stl = stl.replace('dominant-baseline:middle', 'dominant-baseline:central')
			self.vlry['stl'] = stl
			WVLY = 30
			ym = round(max(abs(jm['ymn']), abs(jm['ymx'])), 4)
			""" NOTA: mejorar código para dimensionar adecuadamente """
			w = wtxt(f"+{ym}", self.vlry['h'])
			if w > WVLY:
				self.WVLY = w
			else:
				self.WVLY = WVLY
			#print(f"ym = {ym}")
		# -- recalcular DIVX -->>
		xm = round(max(abs(jm['xmn']), abs(jm['xmx'])), 4)
		w = wtxt(f"+{xm}", self.vlrx['h'])
		if xm > self.DIVX:
			self.DIVX = w
		#print(f"w = {w}")
		
	def __grf_xy_div(self, dt):		
		stl = "stroke:blue;stroke-width:0.25px;stroke-dasharray:5 2"
		self.divh['stl'] = stl
		self.divv['stl'] = stl
		if 'divxy' not in dt: return
		dv = dt['divxy']
		if 'x' in dv:
			o = dv['x']
			if o['ok']:
				self.divv['stl'] = stl_divxy(o)
			else:
				self.divv['ok'] = False
		
	
	def __grf_xy_dim_leyenda(self, dt):
		uLyIzq = 0
		uLyInf = 0
		uLyDer = 0
		uLySup = 0
		wPnLy = 0
		hPnLy = 0
		ok = False
		if 'leyenda' in dt:
			ly = dt['leyenda']
			if 'ok' in ly:
				ok = ly['ok']
				self.lyn['ok'] = ok
		wtx = 0
		nsr = 0
		if 'series' in dt:
			h = self.lyn['h']
			lw = []
			for s in dt['series']:
				w = wtxt(s['id'], h)
				lw.append(w)
			wtx = round(max(lw), 0)
			nsr = len(dt['series'])
		w_lyn = wtx + self.lyn['wlm'] + self.lyn['mrg'] * 2
		
		if ok:
			ly = dt['leyenda']
			
			ubc = 'der'
			if 'ubc' in ly:
				ubc = ly['ubc']
			self.lyn['ubc'] = ubc
			if ubc == 'der':
				uLyDer = 1
			if ubc == 'izq':
				uLyIzq = 1
			if ubc == 'sup':
				uLySup = 1
			if ubc == 'inf':
				uLyInf = 1
			if ubc in ['izq', 'der']:
				wPnLy = w_lyn
			if ubc in ['sup', 'inf']:
				if nsr > 0:
					ncol = int(self.W * 0.8 / w_lyn)
					nfil = int(math.ceil(nsr/ncol))
					hPnLy = nfil * self.lyn['h'] * self.FKT
					self.lyn['ncol'] = ncol
					self.lyn['nfil'] = nfil
			self.lyn['wPnLy'] = wPnLy
			self.lyn['hPnLy'] = hPnLy
			
		return uLyIzq, uLyInf, uLyDer, uLySup, wPnLy, hPnLy
	
	def __grf_xy_dim_area(self, jm, dt):
		if 'margenes' in dt:
			cv = dt['margenes']
			k = 'izq'
			if k in cv:
				self.MRG_IZQ = cv[k]
			k = 'der'
			if k in cv:
				self.MRG_DER = cv[k]
			k = 'sup'
			if k in cv:
				self.MRG_SUP = cv[k]
			k = 'inf'
			if k in cv:
				self.MRG_INF = cv[k]
		"""| dimensiones para leyenda |"""
		uLyIzq, uLyInf, uLyDer, uLySup, wPnLy, hPnLy = self.__grf_xy_dim_leyenda(dt)
		
		"""| define la ventana o área para el gráfico |"""
		xo = self.MRG_IZQ + uLyIzq * (wPnLy + self.MRG_INT) + self.HTLY + self.WVLY + self.MRG_INT
		yo = self.MRG_INF + uLyInf * (hPnLy + self.MRG_INT) + self.HTLX + self.HVLX + self.MRG_INT + self.HETX
		mgDer = uLyDer * (self.MRG_INT + wPnLy) + self.MRG_DER
		mgSup = self.MRG_SUP + self.HTLG + uLySup * (hPnLy + self.MRG_INT) + self.MRG_INT
		WCRV = self.W - (xo + mgDer)
		HCRV = self.H - (yo + mgSup)
		#print('(WCRV, HCRV', WCRV, HCRV)
		WMIN = 200
		if WCRV < WMIN or HCRV < WMIN:
			WCRV = WMIN
			HCRV = self.H * (xo + WCRV + mgDer) / (self.W - (yo + mgSup))
			self.W = xo + WCRV + mgDer
			self.H = yo + HCRV + mgSup
			"""
			if self.ajustable:
				self.W = xo+WCRV+mgDer
				self.H = yo+HCRV+mgSup
			else:
				self.vb['ok'] = True
				self.vb['W'] = xo+WCRV+mgDer
				self.vb['H'] = yo+HCRV+mgSup
			"""
		#print('xo + WCRV + mgDer', xo + WCRV + mgDer, WCRV)
		#print('yo + HCRV + mgSup', yo + HCRV + mgSup, HCRV)
		"""| cálculo de escalas |"""
		#
		# -- escala eje X -->>
		NDIVX = WCRV / self.DIVX
		#print(f"NDIVX = {NDIVX}")
		vmin = jm['xmn']
		vmax = jm['xmx']
		if self.rng['xmn'] is not None:
			vmin = self.rng['xmn']
		if self.rng['xmx'] is not None:
			vmax = self.rng['xmx']
		dv = divgrf(NDIVX, vmin, vmax)
		dXG = dv['dg']
		XmnG = dv['vmng']
		XmxG = dv['vmxg']
		XmnV = XmnG
		XmxV = XmxG
		if self.rng['dx'] is not None:
			dXG = self.rng['dx']
		if self.rng['xmn'] is not None:
			XmnV = dv['vmn']
		if self.rng['xmx'] is not None:
			XmxV = dv['vmx']
		# print(f"dXG = {s.dXG}")
		if XmxV == XmnV:
			self.__error(['XmxV == XmnV'])
			return
		sclX = WCRV / (XmxV - XmnV)
		#
		# -- escala eje Y -->>
		NDIVY = HCRV / self.DIVY
		#print(f"NDIVY = {NDIVY} HCRV = {HCRV}")
		vmin = jm['ymn']
		vmax = jm['ymx']
		if self.rng['ymn'] is not None:
			vmin = self.rng['ymn']
		if self.rng['ymx'] is not None:
			vmax = self.rng['ymx']
		try:
			dv = divgrf(NDIVY, vmin, vmax)
		except ValueError:
			dv = {'dg': 1, 'vmng': -1, 'vmxg': 1, 'vmn': -1, 'vmx': 1}
		dYG = dv['dg']
		YmnG = dv['vmng']
		YmxG = dv['vmxg']
		YmxV = YmxG
		YmnV = YmnG
		if self.rng['dy'] is not None:
			dYG = self.rng['dy']
		if self.rng['ymn'] is not None:
			YmnV = dv['vmn']
		if self.rng['ymx'] is not None:
			YmxV = dv['vmx']
		if YmxV == YmnV:
			self.__error(['YmxV == YmnV'])
			return False
		sclY = HCRV / (YmxV - YmnV)
		js = {
			'xo': xo,
			'yo': yo,
			'dXG': dXG,
			'dYG': dYG,
			'XmnV': XmnV,
			'XmxV': XmxV,
			'XmnG': XmnG,
			'XmxG': XmxG,
			'YmnV': YmnV,
			'YmxV': YmxV,
			'YmnG': YmnG,
			'YmxG': YmxG,
			'WCRV': WCRV,
			'HCRV': HCRV,
			'sclX': sclX,
			'sclY': sclY
		}
		return js
	
	def __error(self, lerr):
		stl = "stroke:none;fill:red;font-size:10px;"
		for i, tx in enumerate(lerr):
			pt = (self.MRG_DER, self.H - self.MRG_SUP - 15 * (i + 1))
			self.dibujar(texto(pt, tx, style=stl))


def grf_xy_svg_curvas_extras(pp, dt, js, svg):
	if 'extras' not in dt:
		return
	#
	XmnV = js['XmnV']
	YmnV = js['YmnV']
	sclX = js['sclX']
	sclY = js['sclY']
	
	lex = dt['extras']
	for ex in lex:
		ok = False
		if 'pp' in ex:
			ok = ex['pp']
		if ok != pp:
			continue
		if 'obj' not in ex:
			continue
		if 'arg' not in ex:
			continue
		# print(ex)
		obj = ex['obj']
		arg = ex['arg']
		if obj == 'linea-v':
			if 'd' in arg:
				for x in arg['d']:
					x_ = (x - XmnV) * sclX
					svg.lineaV(x_, style=stl_linea(arg))
		if obj == 'linea-h':
			if 'd' in arg:
				for y in arg['d']:
					y_ = (y - YmnV) * sclY
					svg.lineaH(y_, style=stl_linea(arg))
		if obj == 'franja-v':
			if 'd' in arg and 'h' in arg:
				x = (arg['d'] - XmnV) * sclX
				h = arg['h'] * sclX
				stl = stl_fondo(arg)
				svg.dibujar(rectangulo((x, 0), h, svg.H, style=stl))
		if obj == 'franja-h':
			if 'd' in arg and 'h' in arg:
				y = (arg['d'] - YmnV) * sclY
				h = arg['h'] * sclY
				stl = stl_fondo(arg)
				svg.dibujar(rectangulo((0, y), svg.W, h, style=stl))


