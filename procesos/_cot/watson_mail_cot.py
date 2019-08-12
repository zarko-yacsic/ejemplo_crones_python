import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 1
tabla     = 'tga_gleads_cotizacion'
campos    = ('idCotizacion', 'email', 'nombre')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)

if(len(respuesta) == 0):
	exit()

for res in respuesta:
    if buscarTexto(res['email'], 'prueba') == True:
        data = { "errores" : 14, 'prueba' : 1 }
        where = "idCotizacion = %s" % str(res['idCotizacion'])
        if mysqlUpdate(data, tabla, where, limit = "1") == False:
            print('> Definir que hacer')
        continue
    if buscarTexto(res['nombre'], 'prueba') == True:
        data = { "errores" : 14, 'prueba' : 1 }
        where = "idCotizacion = %s" % str(res['idCotizacion'])
        if mysqlUpdate(data, tabla, where, limit = "1") == False:
            print('> Definir que hacer')
        continue
    if validarCorreo(res['email']) == False:
        data = { "errores" : 1 }
        where = "idCotizacion = %s" % str(res['idCotizacion'])
        if mysqlUpdate(data, tabla, where, limit = "1") == False:
            print('> Definir que hacer')
        continue
    data = {"watson" : 2, "errores" : 0}
    where = "idCotizacion = %s" % str(res['idCotizacion'])
    if mysqlUpdate(data, tabla, where, limit = "1") == False:
        print('> Definir que hacer')
