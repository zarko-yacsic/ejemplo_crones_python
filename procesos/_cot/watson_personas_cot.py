import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 7
tabla     = 'tga_gleads_cotizacion'
campos    = ('idCotizacion', 'idInmobiliaria', 'rut', 'nombre', 'idEmail_unico', 'email', 'fono')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)


if(len(respuesta) == 0):
    exit()

for i in range(len(respuesta)):
    res = list(respuesta[i].values())
    idCotizacion = res[0]
    c = conexion.cursor()
    c.execute("SELECT idPersonas FROM tga_datos_personas WHERE mail = '" + res[5] + "' AND idInmobiliaria = " + str(res[1]) + " LIMIT 1;")
    row = c.fetchone()
    data = {
        "idInmobiliaria" : res[1],
        "idPuente" : 0,
        "idEmail_unico" : res[4],
        "mail" : res[5],
        "nombre" : res[3],
        "apellido" : '--',
        "telefono" : res[6],
        "rut" : res[2],
        "fecNac" : '0000-00-00',
        "fechaIngreso" : datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S"),
        "activo" : 1,
        "idConexion" : 0,
        "prueba" : 0,
        "respaldo" : 0,
        "sexo" : 1,
        "respaldoTable" : 0,
        "estadoRegistro" : 0,
        "conexionRegistro" : 0,
    }
    error = False

    if row is not None:
        if(actualizarPersonaBD(data, row["idPersonas"]) == False):
            error = True
    else:
        if(insertarPersonaBD(data) == False):
            error = True            
    
    where = "idCotizacion = %s" % str(idCotizacion)
    if(error == False):
        if(mysqlUpdate({"watson" : 9}, tabla, where, "1") == False):
            print('> Definir que hacer')
    if(error == True):
        if(mysqlUpdate({"errores" : 12}, tabla, where, "1") == False):
            print('> Definir que hacer')

    c.close()
