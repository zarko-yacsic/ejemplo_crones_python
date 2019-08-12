import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 2
tabla     = 'tga_gleads_cotizacion'
campos    = ('idCotizacion', 'idInmobiliaria', 'email')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)

if(len(respuesta) == 0):
	exit()

for res in respuesta:
	idEmail = obtenerIDEmailUnico(res['email'])
	idPais = obtenerIDPais(res['idInmobiliaria'])
	if idPais == 30:
		data = { "watson" : 3, "idEmail_unico" : idEmail}
	else:
		data = { "watson" : 4, "idEmail_unico" : idEmail}
        where = "idCotizacion = %s" % str(res['idCotizacion'])
	if mysqlUpdate(data, tabla, where, limit = "1") == False:
		data = { "errores" : 2 }
        where = "idCotizacion = %s" % str(res['idCotizacion'])
		if mysqlUpdate(data, tabla, where, limit = "1") == False:
			print('> Definir que hacer')
