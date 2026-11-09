from datetime import datetime
from flask import Blueprint, jsonify, request
from blueprints.database import mysql, fila_a_diccionario

pedidos_bp = Blueprint(
    'pedidos',
    __name__
)


def leer_pedido_bd(id_pedido):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT id_pedido, nombre_cliente, direccion, telefono, fecha_compra, total FROM pedidos WHERE id_pedido = %s"
        cursor.execute(sql, (id_pedido,))
        datos = cursor.fetchone()
        if datos is not None:
            return fila_a_diccionario(cursor, datos)
        else:
            return None
    except Exception as ex:
        raise ex
    finally:
        if cursor is not None:
            cursor.close()


@pedidos_bp.route('', methods=['POST'])
def registrar_pedido():
    cursor = None
    try:
        datos = request.get_json(silent=True) or {}
        nombre = datos.get('nombre')
        direccion = datos.get('direccion')
        telefono = datos.get('telefono')
        fecha = datos.get('fecha')
        if nombre in (None, '') or direccion in (None, '') or telefono in (None, '') or fecha in (None, ''):
            return jsonify({'mensaje': 'Faltan los datos del cliente', 'exito': False}), 400
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            return jsonify({'mensaje': 'La fecha no es válida', 'exito': False}), 400
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*), IFNULL(SUM(subtotal), 0) FROM temp_pizza")
        cantidad, total = cursor.fetchone()
        if cantidad == 0:
            return jsonify({'mensaje': 'El pedido no tiene pizzas', 'exito': False}), 400
        sql = "INSERT INTO pedidos (nombre_cliente, direccion, telefono, fecha_compra, total) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nombre, direccion, telefono, fecha, total))
        id_pedido = cursor.lastrowid
        sql = """INSERT INTO detalle_pedido (id_pedido, tamano, ingredientes, num_pizzas, subtotal)
                 SELECT %s, tamano, ingredientes, num_pizzas, subtotal FROM temp_pizza"""
        cursor.execute(sql, (id_pedido,))
        cursor.execute("DELETE FROM temp_pizza")
        mysql.connection.commit()
        return jsonify({
            'id_pedido': id_pedido,
            'total': float(total),
            'mensaje': "Pedido registrado. Total a pagar: ${:,.2f}".format(total),
            'exito': True
        }), 201

    except Exception as ex:
        try:
            mysql.connection.rollback()
        except Exception:
            pass
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()


@pedidos_bp.route('/<int:id_pedido>/detalle', methods=['GET'])
def detalle_pedido(id_pedido):
    cursor = None
    try:
        pedido = leer_pedido_bd(id_pedido)
        if pedido is None:
            return jsonify({'detalle': [], 'mensaje': 'Pedido no encontrado', 'exito': False}), 404
        cursor = mysql.connection.cursor()
        sql = """
            SELECT id_detalle, tamano, ingredientes, num_pizzas, subtotal
            FROM detalle_pedido
            WHERE id_pedido = %s
            ORDER BY id_detalle
        """
        cursor.execute(sql, (id_pedido,))
        datos = cursor.fetchall()
        detalle = [fila_a_diccionario(cursor, fila) for fila in datos]

        return jsonify({
            'pedido': pedido,
            'detalle': detalle,
            'mensaje': 'Detalle del pedido',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()
