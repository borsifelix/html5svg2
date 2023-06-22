import math

from PIL import ImageFont


def vrf(clv, dsc, dt):
	if clv not in dt:
		raise Exception(f"Se esperaba '{clv}' ({dsc}) en datos de entrada")
	return dt[clv]


def str_num(num):
	## convierte un numero en texto
	pdc, pen = math.modf(num)
	if pdc == 0:
		return str(int(pen))
	return str(num)


def wtxt(txt, px):
	h = math.ceil(px)
	return ImageFont.truetype('arialbd.ttf', h).getlength(txt)


def divgrf(ndiv, vmin, vmax):
	#
	# print(f"vmin = {vmin}  vmax = {vmax}")
	try:
		dim = vmax - vmin
		divx = dim / ndiv
		#
		mag = math.pow(10.0, math.floor(math.log10(divx)))
		Pmag = int(divx / mag + 0.5)
		#
		if Pmag > 5:
			Pmag = 10.0
		elif Pmag > 2.0:
			Pmag = 5.0
		elif Pmag > 1.0:
			Pmag = 2.0
		#
		dg = mag * Pmag
		vmn = round(dg * math.floor(vmin / dg), 5)
		vmx = round(dg * math.ceil(vmax / dg), 5)

		# return {'dg':dg, 'vmn':vmn, 'vmx':vmx}
		return {'dg': dg, 'vmng': vmn, 'vmxg': vmx, 'vmn': vmin, 'vmx': vmax}
	except Exception as e:
		err = f"ERROR(divgrf): {e} vmin = {vmin}  vmax = {vmax} ndiv = {ndiv}"
		print(err)
		raise Exception(err)


def g_marco(dt):
	# -- estilo de borde -->>
	e = 1
	cb = 'black'
	# -- estilo de fondo -->>
	cf = 'none'
	op = ''
	#
	if 'marco' in dt:
		jx = dt['marco']
		if 'borde' in jx:
			o = jx['borde']
			if 'e' in o:
				e = o['e']
			if 'c' in o:
				cb = o['c']
		if 'fondo' in jx:
			o = jx['fondo']
			if 'c' in o:
				cf = o['c']
			if 't' in o:
				op = f"opacity:{o['t']};"
	ebr = f"fill:none;stroke:{cb};stroke-width:{e}px;"
	efn = f"stroke:none;fill:{cf};{op}"
	return ebr, efn


def g_fondo(**cv):
	esp = 0
	# -- estilo de linea -- #
	eLn = ""
	k = 'borde'
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
	k = 'fondo'
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


def g_rotulo(h, o):
	OK = True
	if 'ok' in o:
		OK = o['ok']
	# -- rótulo -->
	txt = ""
	if 'txt' in o:
		txt = o['txt']
	# -- estilo -->>
	sAl = "text-anchor:middle;dominant-baseline:middle;"
	stl = "stroke:none;"
	# -- color -->
	if 'c' in o:
		stl += f"fill:{o['c']};"
	# -- nombre tipo -->
	if 'f' in o:
		stl += f"font-family:{o['f']};"
	# -- tamaño tipo -->
	if 'h' in o:
		h = o['h']
	stl += f"font-size:{h}px;"
	# -- negrita -->
	if 'n' in o:
		if o['n']:
			stl += "font-weight:bold;"
	# -- itálica -->
	if 'i' in o:
		if o['i']:
			stl += "font-style:italic;"
	#
	stl += sAl
	#
	return {'ok': OK, 'h': h, 'txt': txt, 'stl': stl}


def grf_xy_limites(dt):
	lerr = []  # lista de errores
	"""| valores extremos a partir de series |"""
	jm = {'xmn': -1, 'xmx': 1, 'ymn': -1, 'ymx': 1}
	if 'series' in dt:
		lmnx = []
		lmxx = []
		lmny = []
		lmxy = []
		for i, jx in enumerate(dt['series']):
			if 'id' not in jx:
				jx['id'] = f"Serie {i + 1}"
			if 'vx' not in jx:
				lerr.append(f"No se ha indicado 'vx' (valores x)  en la serie#{i + 1}")
			if 'vy' not in jx:
				lerr.append(f"No se ha indicado 'vy' (valores y)  en la serie#{i + 1}")
			vx = jx['vx']
			vy = jx['vy']
			nx = len(vx)
			ny = len(vy)
			if nx != ny:
				id = jx['id']
				err = f"No coinciden las dimensiones de 'vx'({nx}) y 'vy'({ny}) en '{id}'"
				lerr.append(err)
			#
			jx['n'] = nx
			lmnx.append(min(vx))
			lmxx.append(max(vx))
			lmny.append(min(vy))
			lmxy.append(max(vy))
		#
		jm['xmn'] = min(lmnx)
		jm['xmx'] = max(lmxx)
		jm['ymn'] = min(lmny)
		jm['ymx'] = max(lmxy)
		#
		if jm['xmx'] == jm['xmn']:
			jm['xmx'] += 1.0
			jm['xmn'] -= 1.0
		if jm['ymx'] == jm['ymn']:
			jm['ymx'] += 1.0
			jm['ymn'] -= 1.0
	else:
		pass
	return jm, lerr


def grf_xy_stl(ls):
	clr = ['red', 'green', 'blue', 'gold', 'orange', 'magenta', 'purple']
	n = len(clr)
	for i, o in enumerate(ls):
		# -- nombre de serie -->>
		if 'id' not in o:
			o['id'] = f"Serie #{i+1}"
		# -- color de línea -->>
		c = clr[i % n]
		if 'c' in o:
			c = o['c']
		# -- espesor de línea -->>
		e = 1
		if 'e' in o:
			e = o['e']
		else:
			o['e'] = e
		# -- tipo de lineas -->>
		
		o['stl'] = f"fill:none;stroke-linejoin:round;stroke:{c};stroke-width:{e};"
		o['over'] = f"resaltar(this,{2 * o['e']})"
		o['out'] = f"resaltar(this,{o['e']})"
		# onmouseover="evt.target.setAttribute('stroke-width', '3');"
		# onmouseout="evt.target.setAttribute('stroke-width', '1');"


def stl_linea(js):
	# -- color de línea -->
	cl = 'black'
	k = 'cl'
	if k in js:
		cl = js[k]
	stl = f"stroke:{cl};"
	# -- espesor de línea -->
	e = 1
	k = 'e'
	if k in js:
		e = js[k]
		if e != 1:
			stl += f"stroke-width:{e}px;"
	# stroke-dasharray:
	k = 'pl'
	if k in js:
		pl = js[k]
		stl += f"stroke-dasharray:{pl};"
	#
	return stl


def stl_fondo(js):
	# -- color de fondo -->>
	cf = 'white'
	k = 'cf'
	if k in js:
		cf = js[k]
	stl = f"stroke:none;fill:{cf};"
	# - trasparencia -->>
	k = 't'
	if k in js:
		t = js[k]
		stl += f"opacity:{t};"
	
	return stl
	
	
def stl_divxy(js):
	# -- color de línea -->
	cl = 'black'
	k = 'c'
	if k in js:
		cl = js[k]
	stl = f"stroke:{cl};"
	# -- espesor de línea -->
	e = 1
	k = 'e'
	if k in js:
		e = js[k]
		if e != 1:
			stl += f"stroke-width:{e}px;"
	# stroke-dasharray:
	k = 'p'
	if k in js:
		pl = js[k]
		stl += f"stroke-dasharray:{pl};"
	#
	return stl
