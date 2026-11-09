from decimal import Decimal
from datetime import date
from flask_mysqldb import MySQL

mysql = MySQL()

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    datos = dict(zip(columnas, fila))
    for clave, valor in datos.items():
        if isinstance(valor, Decimal):
            datos[clave] = float(valor)
        elif isinstance(valor, date):
            datos[clave] = valor.strftime('%Y-%m-%d')
    return datos
