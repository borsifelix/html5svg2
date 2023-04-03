# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 18:11:20 2023

@author: Borsi Romero
"""
from datetime import datetime


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


def texto(px, tx, **jx):
	try:
		x, y = px
		js = {'x': x, 'y': y, 'txt': tx}
		if 'ang' not in jx:
			js['ang'] = 0
		return __obj('text', jx, js)
	except Exception as e:
		raise Exception(f"ERROR(texto)> {e}")


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
		s.W = 100
		s.H = 100
		s.lst = []  # lista de estilos
		s.lmk = []  # lista de marcas
		s.ld = []  # lista de definiciones
		s.lc = []  # lista de contenido
		if 'W' in js:
			s.W = js['W']
		if 'H' in js:
			s.H = js['H']
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
			jx['viewBox'] = f'0 0 {s.W} {s.H}'
		else:
			jx['width'] = s.W
			jx['height'] = s.H
		#
		if s.letra is not None:
			jx['font-family'] = s.letra
		#
		stl = f"stroke:{s.color_linea};"
		if s.color_fondo is not None:
			stl = f"background-color:{s.color_fondo};{stl}"
		jx['style'] = stl
		#
		jx['xmlns'] = "http://www.w3.org/2000/svg"
		jx['xmlns:xlink'] = "http://www.w3.org/1999/xlink"
		#
		return jx
	
	def exp(s, **d):
		#
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
					jx['transform'] = f"rotate({-jx['ang']},{jx['x']},{jx['y']+jx['height']})"
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
						if k in ['Q', 'S']:
							d += f"{k} {v[0][0]},{s.H - v[0][1]} {v[1][0]},{s.H - v[1][1]} "
						if k in ['q', 's']:
							d += f"{k} {v[0][0]},{- v[0][1]} {v[1][0]},{- v[1][1]} "
						if k == 'C':
							d += f"{k} {v[0][0]},{s.H - v[0][1]} {v[1][0]},{s.H - v[1][1]} {v[2][0]},{s.H - v[2][1]} "
						if k == 'A':
							d += f"{k} {v[0][0]},{  v[0][1]} {v[1]} {v[2]} {v[3]} {v[4][0]},{s.H - v[4][1]} "
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