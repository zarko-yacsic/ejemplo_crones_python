import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 6
tabla     = 'tga_gleads_cotizacion'
campos    = ('idCotizacion', 'nombre')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)

if(len(respuesta) == 0):
	exit()

for res in respuesta:
	data = { "watson" : 7 , "nombre" : convertirMayusculas(res['nombre'])}
	where = "idCotizacion = '%s'" % res['idCotizacion']
	if mysqlUpdate(data, tabla, where, limit = "1") == False:
		data = { "errores" : 11 }
		where = "idCotizacion = '%s'" % res['idCotizacion']
		if mysqlUpdate(data, tabla, where, limit = "1") == False:
			print('> Definir que hacer')
