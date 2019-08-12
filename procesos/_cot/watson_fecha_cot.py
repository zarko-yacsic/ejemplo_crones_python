import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 4
tabla     = 'tga_gleads_cotizacion'
campos    = ('idCotizacion', 'fechaCotizacion')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)

if(len(respuesta) == 0):
    exit()

for res in respuesta:
    fecha = validarFecha(filtrarFecha(res['fechaCotizacion']))
    if fecha != False:
        anio, mes, fechaNum = fecha
        data = { "watson" : 5, "fechaAnio" : anio, "fechaMes" : mes, "fechaNum" : fechaNum}
        where = "idCotizacion = %s" % str(res['idCotizacion'])
    else:
        data = { "errores" : 4 }
        where = "idCotizacion = %s" % str(res['idCotizacion'])
    if mysqlUpdate(data, tabla, where, limit = "1") == False:
        print('> Definir que hacer')
