import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 9
tabla     = 'tga_gleads_cotizacion'
campos    = ('idCotizacion','idInmobiliaria','idEmail_unico','email')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)

if(len(respuesta) == 0):
    exit()

for i in range(len(respuesta)):
    res = list(respuesta[i].values())
    idCotizacion = res[0]
    c = conexion.cursor()
    c.execute("SELECT idLead FROM tga_glead_lead WHERE idEmail_unico = " + str(res[2]) + " AND idInmobiliaria = " + str(res[1]) + " LIMIT 1;")
    row = c.fetchone()
    if row is None:
        data = {
            "idInmobiliaria" : res[1],
            "idEmail_unico" : res[2],
            "email" : res[3]
        }
        where = "idCotizacion = %s" % str(idCotizacion)
        if(crearLead(data) == True):
            if(mysqlUpdate({"watson" : 10}, tabla, where, "1") == False):
                print('> Definir que hacer')
        else:
            if(mysqlUpdate({"errores" : 9}, tabla, where, "1") == False):
                print('> Definir que hacer')
    else:
        if(mysqlUpdate({"watson" : 10}, tabla, where, "1") == False):
            print('> Definir que hacer')
    c.close()
