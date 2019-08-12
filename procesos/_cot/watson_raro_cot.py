import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 5
tabla     = 'tga_gleads_cotizacion'
campos    = ('idCotizacion', 'nombre','fono','rut')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)


if(len(respuesta) == 0):
    exit()

for i in range(len(respuesta)):
    res = list(respuesta[i].values())
    idCotizacion = res[0]
    where = "idCotizacion = %s" % str(idCotizacion)
    error = False

    for z in range(len(res)):
        if(z > 0):
            if(validarBlancos(res[z]) == False):
                data = {"errores" : 7}
                error = True
                if(mysqlUpdate(data, tabla, where, "1") == False):
                    print('> Definir que hacer')
                break
            if(validarCaracteresHTML(res[z]) == False):
                data = {"errores" : 6}
                error = True
                if(mysqlUpdate(data, tabla, where, "1") == False):
                    print('> Definir que hacer')
                break
            if(validarCaracteresRaros(res[z]) == False):
                data = {"errores" : 5}
                error = True
                if(mysqlUpdate(data, tabla, where, "1") == False):
                    print('> Definir que hacer')
                break
    
    if(error == False):
        data = {"watson" : 6}
        if(mysqlUpdate(data, tabla, where, "1") == False):
            print('> Definir que hacer')
    
