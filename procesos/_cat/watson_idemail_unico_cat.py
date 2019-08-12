import sys
sys.path.append('../..')

from librerias.funciones import *

watson    = 2
tabla     = 'tga_gleads_categorizado'
campos    = ('idCategorizado', 'idInmobiliaria', 'email')
limit     = 30
orden     = '';
respuesta = mysqlQueryPrincipal(campos,tabla,watson,limit,orden)

if(len(respuesta) == 0):
	exit()

for res in respuesta:
	idEmail = obtenerIDEmailUnico(res['email'])
	idPais = obtenerIDPais(res['idInmobiliaria'])
	data = { "watson" : 4, "idEmail_unico" : idEmail}
	where = "idCategorizado = %s" % str(res['idCategorizado'])
	if mysqlUpdate(data, tabla, where, limit = "1") == False:
		data = { "errores" : 2 }
		where = "idCategorizado = %s" % str(res['idCategorizado'])
		if mysqlUpdate(data, tabla, where, limit = "1") == False:
			print('> Definir que hacer')
