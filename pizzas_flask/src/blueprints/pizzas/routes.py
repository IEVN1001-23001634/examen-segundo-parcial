from flask import Blueprint, jsonify, request
from blueprints.database import mysql, fila_a_diccionario

pizzas_bp = Blueprint(
    'pizzas',
    __name__
)

PRECIOS_TAMANO = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
PRECIO_INGREDIENTE = 10


def leer_pizza_bd(id_temp):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT id_temp, tamano, ingredientes, num_pizzas, subtotal FROM temp_pizza WHERE id_temp = %s"
        cursor.execute(sql, (id_temp,))
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


@pizzas_bp.route('', methods=['GET'])
def lista_pizzas():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id_temp, tamano, ingredientes, num_pizzas, subtotal
            FROM temp_pizza
            ORDER BY id_temp
        """)
        datos = cursor.fetchall()
        pizzas = [fila_a_diccionario(cursor, fila) for fila in datos]

        return jsonify({
            'pizzas': pizzas,
            'mensaje': 'Lista de pizzas del pedido',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': "Error al consultar las pizzas: {}".format(ex),
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()


@pizzas_bp.route('', methods=['POST'])
def registrar_pizza():
    cursor = None
    try:
        datos = request.get_json(silent=True) or {}
        tamano = datos.get('tamano')
        ingredientes = datos.get('ingredientes') or ''
        num_pizzas = datos.get('num_pizzas')
        if tamano not in PRECIOS_TAMANO:
            return jsonify({'mensaje': 'El tamaño de la pizza no es válido', 'exito': False}), 400
        try:
            num_pizzas = int(num_pizzas)
        except (TypeError, ValueError):
            return jsonify({'mensaje': 'El número de pizzas no es válido', 'exito': False}), 400
        if num_pizzas < 1:
            return jsonify({'mensaje': 'El número de pizzas no es válido', 'exito': False}), 400
        cantidad_ingredientes = len([i for i in ingredientes.split(',') if i.strip() != ''])
        subtotal = (PRECIOS_TAMANO[tamano] + cantidad_ingredientes * PRECIO_INGREDIENTE) * num_pizzas
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO temp_pizza (tamano, ingredientes, num_pizzas, subtotal) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (tamano, ingredientes, num_pizzas, subtotal))
        mysql.connection.commit()
        return jsonify({'mensaje': "Pizza agregada al pedido", 'exito': True}), 201

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()


@pizzas_bp.route('/<int:id_temp>', methods=['DELETE'])
def quitar_pizza(id_temp):
    cursor = None
    try:
        pizza = leer_pizza_bd(id_temp)
        if pizza is not None:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM temp_pizza WHERE id_temp = %s", (id_temp,))
            mysql.connection.commit()
            return jsonify({'mensaje': "Pizza quitada del pedido", 'exito': True}), 200
        else:
            return jsonify({'mensaje': "Pizza no encontrada para quitar", 'exito': False}), 404

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()
