import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 1
tabla     = 'tga_gleads_categorizado'
campos    = ('idCategorizado', 'email')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)

if(len(respuesta) == 0):
    exit()

for res in respuesta:
    if buscarTexto(res['email'], 'prueba') == True:
        data = { "errores" : 14, 'prueba' : 1 }
        where = "idCategorizado = %s" % str(res['idCategorizado'])
        if mysqlUpdate(data, tabla, where, limit = "1") == False:
            print('> Definir que hacer')
        continue
    if validarCorreo(res['email']) == False:
        data = { "errores" : 1 }
        where = "idCategorizado = %s" % str(res['idCategorizado'])
        if mysqlUpdate(data, tabla, where, limit = "1") == False:
            print('> Definir que hacer')
        continue
    data = {"watson" : 2, "errores" : 0}
    where = "idCategorizado = %s" % str(res['idCategorizado'])
    if mysqlUpdate(data, tabla, where, limit = "1") == False:
        print('> Definir que hacer')
