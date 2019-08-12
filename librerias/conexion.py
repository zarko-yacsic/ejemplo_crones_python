import pymysql

def conectarMysql():
    conexion = pymysql.connect(host='52.53.87.233',
                                user='puente_tga',
                                password='_b8DfHt_',
                                db='puente',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    return conexion
