import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 10
tabla     = 'tga_gleads_categorizado'
campos    = ('idCategorizado','idInmobiliaria','idEmail_unico','email','idProyecto','fechaPuntos','fechaAnio','fechaMes','fechaNum')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)

if(len(respuesta) == 0):
	exit()

for i in range(len(respuesta)):
    res = list(respuesta[i].values())
    idCategorizado = res[0]
    sql = "SELECT idLeadMensual FROM tga_glead_lead_mensual"
    sql += " WHERE idInmobiliaria = " + str(res[1]) + " AND idProyecto = " + str(res[4])
    sql += " AND idEmail_unico = " + str(res[2]) + " AND fechaAnio = " + str(res[6])
    sql += " AND fechaMes = " + str(res[7]) + " LIMIT 1;"
    c = conexion.cursor()
    c.execute(sql)
    row = c.fetchone()
    if row is None:
        data = {
            "idInmobiliaria" : res[1],
            "idProyecto" : res[4],
            "idEmail_unico" : res[2],
            "fecha" : res[5],
            "fechaLead" : res[5],
            "fechaAnio" : res[6],
            "fechaMes" : res[7],
            "fechaNum" : res[8],
            "email" : res[3]
        }
        where = "idCategorizado = %s" % str(idCategorizado)
        if(crearLeadProyectoMes(data) == True):
            if(mysqlUpdate({"watson" : 99}, tabla, where, "1") == False):
                print('> Definir que hacer')
        else:
            if(mysqlUpdate({"errores" : 10}, tabla, where, "1") == False):
                print('> Definir que hacer')
    else:
        if(mysqlUpdate({"watson" : 99}, tabla, where, "1") == False):
            print('> Definir que hacer')
    c.close()
