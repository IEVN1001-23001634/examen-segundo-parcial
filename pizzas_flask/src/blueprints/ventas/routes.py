import unicodedata
from flask import Blueprint, jsonify
from blueprints.database import mysql, fila_a_diccionario

ventas_bp = Blueprint(
    'ventas',
    __name__
)

DIAS = {
    'domingo': 1,
    'lunes': 2,
    'martes': 3,
    'miercoles': 4,
    'jueves': 5,
    'viernes': 6,
    'sabado': 7
}

MESES = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'setiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12
}

def quitar_acentos(texto):
    texto = unicodedata.normalize('NFD', texto.strip().lower())
    return ''.join(c for c in texto if unicodedata.category(c) != 'Mn')

def consultar_ventas(condicion, parametro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = """
            SELECT id_pedido, nombre_cliente, direccion, telefono, fecha_compra, total
            FROM pedidos
            WHERE {0}
            ORDER BY fecha_compra DESC, id_pedido DESC
        """.format(condicion)
        cursor.execute(sql, (parametro,))
        datos = cursor.fetchall()
        ventas = [fila_a_diccionario(cursor, fila) for fila in datos]
        total = sum(venta['total'] for venta in ventas)
        return ventas, total
    except Exception as ex:
        raise ex
    finally:
        if cursor is not None:
            cursor.close()

@ventas_bp.route('/dia/<dia>', methods=['GET'])
def ventas_por_dia(dia):
    try:
        numero = DIAS.get(quitar_acentos(dia))
        if numero is None:
            return jsonify({'ventas': [], 'total': 0, 'mensaje': 'Día inválido: {}'.format(dia), 'exito': False}), 400
        ventas, total = consultar_ventas("DAYOFWEEK(fecha_compra) = %s", numero)
        return jsonify({
            'ventas': ventas,
            'total': total,
            'mensaje': 'Ventas del día {}'.format(dia),
            'exito': True
        }), 200
    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500

@ventas_bp.route('/mes/<mes>', methods=['GET'])
def ventas_por_mes(mes):
    try:
        numero = MESES.get(quitar_acentos(mes))
        if numero is None:
            return jsonify({'ventas': [], 'total': 0, 'mensaje': 'Mes inválido: {}'.format(mes), 'exito': False}), 400
        ventas, total = consultar_ventas("MONTH(fecha_compra) = %s", numero)
        return jsonify({
            'ventas': ventas,
            'total': total,
            'mensaje': 'Ventas del mes {}'.format(mes),
            'exito': True
        }), 200
    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
