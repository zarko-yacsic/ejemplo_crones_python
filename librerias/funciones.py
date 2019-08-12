
import re, datetime, time, mandrill
from librerias.conexion import *
conexion = conectarMysql()

# Query principal del cron... 
def mysqlQueryPrincipal(camposBuscar, tabla, watson, limit = 10, orden = ""):
    campos  = ','.join(camposBuscar)
    if limit != "":
        limit = " LIMIT " + str(limit)
    if orden != "":
        orden = " ORDER BY " + orden
    c = conexion.cursor()
    c.execute("SELECT " + campos + " FROM " + tabla + " WHERE watson=" + str(watson) + " AND errores=0" + orden + limit + ";")
    rows = c.fetchall()
    if rows is not None:
        salida = rows
        #salida = c._last_executed # <--- devuelve ultima query ejecutada
    else:
        salida = 0 
    c.close()
    return salida

# Validar correo (nombre@correo.cl) + largo mínimo de 7, 
def validarCorreo(correo):
    if len(correo) > 7:
        regexp = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        if re.match(regexp, convertirMinusculas(correo)) != None:
            salida = True
        else:
            salida = False
    else:
        salida = False
    return salida

# Obtener y retornar 'idEmail_unico' si es que existe,
# en caso de no existir, 'idEmail_unico' es creado en la tabla indicada, y luego se retorna...
def obtenerIDEmailUnico(correo):
    c = conexion.cursor()
    c.execute("SELECT idEmail_unico FROM tga_gleads_mail_unico WHERE email = '" + correo + "' LIMIT 1;")
    row = c.fetchone()
    if row is not None:
        salida = row["idEmail_unico"]
    else:
        salida = mysqlInsert({"email" : correo}, 'tga_gleads_mail_unico', True)
    c.close()
    return salida

# Obtener y retornar 'idPais' si es que existe, si no, retorna 'False' 
def obtenerIDPais(idInmobiliaria):
    c = conexion.cursor()
    c.execute("SELECT idPais FROM tga_gleads_inmobiliaria WHERE idInmobiliaria = '" + str(idInmobiliaria) + "' LIMIT 1;")
    row = c.fetchone()
    if row is not None:
        salida = row["idPais"]
    else:
        salida = False
    c.close()
    return salida

# Valida RUT (Sólo Chile, devuelve True|False)
def validarRut(rut):
    rfiltro = filtrarRut(rut)
    rutx = str(rfiltro[0:len(rfiltro)-1])
    digito = str(rfiltro[-1])
    multiplo = 2
    total = 0
    for reverso in reversed(rutx):
        total += int(reverso) * multiplo
        if multiplo == 7:
            multiplo = 2
        else:
            multiplo += 1
        modulus = total % 11
        verificador = 11 - modulus
        if verificador == 10:
            div = "k"
        elif verificador == 11:
            div = "0"
        else:
            if verificador < 10:
                div = verificador
    if str(div) == str(digito):
        salida = True
    else:
        salida = False
    return salida

# Filtra sólo los caracteres permitidos para un RUT chileno (Previo a validación)...
def filtrarRut(rut):
    caracteres = "1234567890k"
    rutx = ""
    for cambio in rut.lower():
        if cambio in caracteres:
            rutx += cambio
    return rutx

# Valida fecha según formatos de entrada:
# 'yyyy/mm/dd', 'yyyy-mm-dd', 'dd/mm/yyyy', y 'dd-mm-yyyy'
# ...Si fecha es correcta retorna una lista tipo (año, mes, dia)
# En caso de error la función retorna False
def validarFecha(fecha):
    try:
        fecha = fecha.replace('/', '-')
        f = fecha.split('-')
        if len(f[0]) == 4:
            fecha = f[0] + '-' + f[1] + '-' + f[2]
        else:
            fecha = f[2] + '-' + f[1] + '-' + f[0]
        fecha = datetime.datetime.strptime(fecha,'%Y-%m-%d')
        fecha = datetime.datetime.strftime(fecha,"%Y-%m-%d")
        anio, mes, dia = fecha.split('-')
        return anio, mes, anio+mes+dia
    except ValueError:
        return False

# Filtrar fecha (Previo a validación)...
def filtrarFecha(fecha):
    fecha = str(fecha)[0:-9]
    return fecha

# Validar que texto no esté en blanco, devuelve 'False' cuando hay error...
def validarBlancos(texto):
    if len(texto) == 0:
        salida = False
    else:
        salida = True
    return salida

# Validar que texto no contenga etiquetas <HTML>, devuelve 'False' cuando hay...
def validarCaracteresHTML(texto):
    regexp = r'<.*?>.*?<\/.*?>|<.*?>.*?|.*?<\/.*?>|.*?\/.*?>'
    if re.match(regexp, texto) != None:
        salida = False
    else:
        salida = True
    return salida

# Validar que texto no contenga caracteres no permitidos, devuelve 'False' cuando existen
def validarCaracteresRaros(texto):
    regexp = r'^[-.+a-zA-Z0-9 |á|é|í|ó|ú|ñ|Á|É|Í|Ó|Ú|Ñ]*$'
    if re.match(regexp, texto) == None:
        salida = False
    else:
        salida = True
    return salida

# Insertar nuevo registro en tabla personas...
def insertarPersonaBD(data):
    salida = mysqlInsert(data, "tga_datos_personas")
    return salida

# Actualizar registro en tabla personas...
def actualizarPersonaBD(data, idPersonas):
    salida = mysqlUpdate(data, "tga_datos_personas", "idPersonas = %s" % idPersonas, "1")
    return salida

# Buscar una subcadena dentro de un texto...
def buscarTexto(texto, buscar):
    texto = convertirMinusculas(texto)
    buscar = convertirMinusculas(buscar)
    if (texto.find(buscar) != -1): 
        return True
    else:
        return False

# Separa una cadena de tipo 'Nombre ApellidoP ApellidoM' en una lista tipo ['Nombre', 'ApellidoP', 'ApellidoM']...
def separarNombre(texto):
    nombre = texto.split()
    return nombre

# Convierte texto a mayúsculas...
def convertirMayusculas(texto):
    return texto.upper()

# Convierte texto a minuscúlas...
def convertirMinusculas(texto):
    return texto.lower()

# Crear Lead...
def crearLead(data):
    salida = mysqlInsert(data, "tga_glead_lead")
    return salida 
 
# Actualizar Lead...
def actualizarLead(data, idLead):
    salida = mysqlUpdate(data, "tga_glead_lead", "idLead = %s" % idLead, "1")
    return salida

# Crear Lead proyecto mes...
def crearLeadProyectoMes(data):
    salida = mysqlInsert(data, "tga_glead_lead_mensual")
    return salida

# Actualizar Lead proyecto mes...
def actualizarLeadProyectoMes(data, idLeadMensual):
    salida = mysqlUpdate(data, "tga_glead_lead_mensual", "idLeadMensual = %s" % idLeadMensual, "1")
    return salida

# Activación de traspaso...
def activarTraspaso():
    return "Función 99 : Activación de traspaso"

# EJEMPLO : Insertar un registro:
#       mysqlInsert({"campo1" : 1, "campo2" : "VALOR_2"}, "nombre_de_la_tabla", True)
# Nota : El parámetro 'retorna_id' en 'True' devolverá el último ID creado... 
def mysqlInsert(data, tabla, retorna_id = False):
    campos  = ','.join(data.keys())
    valores = list(data.values())
    s = ""
    i = 0
    while i < len(data):
        s += "%s,"
        i = i + 1
    c = conexion.cursor()
    try:
        query = "INSERT INTO " + tabla + " (" + campos + ") VALUES (" + s[:-1] + ");"
        c.execute(query, valores)
        conexion.commit()
        if retorna_id == True:
            salida = c.lastrowid
        else:
            salida = True
    except conexion.IntegrityError:
        salida = False
    c.close()
    return salida

# EJEMPLO : Actualizar un registro :
#       mysqlUpdate({"campo1" : 1, "campo2" : "VALOR_2"}, "nombre_de_la_tabla", 
#               "condition_1=0 AND condition_2=1 OR condition_3=2", "1")
def mysqlUpdate(data, tabla, where = "", limit = ""):
    campos  = list(data.keys())
    valores = list(data.values())
    set_vals = ""
    i = 0
    while i < len(data):
        set_vals += campos[i] + " = %s, "
        i = i + 1
    c = conexion.cursor()
    try:
        if where != "":
            where = " WHERE " + where
        if limit != "":
            limit = " LIMIT " + limit
        query = "UPDATE " + tabla + " SET " + set_vals[:-2] + where + limit + ";"
        c.execute(query, valores)
        conexion.commit()
        salida = c._last_executed # <--- devuelve ultima query ejecutada 
        # salida = True
    except conexion.IntegrityError:
        salida = False
    c.close()
    return print(salida)
    #return salida


# Envío de correos con Mandrill...
def enviar_correo_mandrill(keyMandrill,from_email,from_name,html,subject,tag,to_email,to_name):
    try:
        mandrill_client = mandrill.Mandrill(keyMandrill)
        message = {
            'from_email': from_email,
            'from_name': from_name,
            'html': html,
            'important': False,
            'merge': True,
            'merge_language' : 'mailchimp',
            'subject': subject,
            'tags': [tag],
            'to': [{
                'email': to_email,
                'name': to_name,
                'type': 'to'
                }],
            'track_clicks': True,
            'track_opens': True,
            'tracking_domain': None,
            'url_strip_qs': None,
            'view_content_link': None
        }
        result = mandrill_client.messages.send(message, False, 'Main Pool', time.strftime("%H:%M:%S"))
    except mandrill.Error as e:
        print('A mandrill error occurred: %s - %s' % (e.__class__, e))
        raise

