import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 3
tabla     = 'tga_gleads_cotizacion'
campos    = ('idCotizacion', 'rut')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)

if(len(respuesta) == 0):
	exit()

for res in respuesta:
	if validarRut(res['rut']) == True:
		data = { "watson" : 4 }
		where = "idCotizacion = '%s'" % res['idCotizacion']
	else:
		data = { "errores" : 3 }
		where = "idCotizacion = '%s'" % res['idCotizacion']
	if mysqlUpdate(data, tabla, where, limit = "1") == False:
		print('> Definir que hacer')
