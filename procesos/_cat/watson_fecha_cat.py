import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 4
tabla     = 'tga_gleads_categorizado'
campos    = ('idCategorizado', 'fechaPuntos')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)

if(len(respuesta) == 0):
    exit()

for res in respuesta:
    fecha = validarFecha(filtrarFecha(res['fechaPuntos']))
    if fecha != False:
        anio, mes, fechaNum = fecha
        data = { "watson" : 9, "fechaAnio" : anio, "fechaMes" : mes, "fechaNum" : fechaNum}
        where = "idCategorizado = %s" % str(res['idCategorizado'])
    else:
        data = { "errores" : 4 }
        where = "idCategorizado = %s" % str(res['idCategorizado'])
    if mysqlUpdate(data, tabla, where, limit = "1") == False:
        print('> Definir que hacer')
