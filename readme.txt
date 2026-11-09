# Pizzería API (Flask + MySQL)

1. Ejecutar `schema.sql` en MySQL (crea la base `pizzeria_db` y sus 3 tablas).
2. Revisar usuario y contraseña en `src/config.py`.
3. Crear el entorno virtual e instalar dependencias:
   ```
   python -m venv venv
   venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```
4. Entrar a la carpeta `src` y correr:
   ```
   cd src
   python app.py
   ```
   La API queda en http://127.0.0.1:5000

## Rutas
| Método | Ruta | Qué hace |
|---|---|---|
| GET | /api/pizzas | Lista la tabla temporal `temp_pizza` |
| POST | /api/pizzas | Agrega una pizza a `temp_pizza` |
| DELETE | /api/pizzas/<id_temp> | Quita una pizza de `temp_pizza` |
| POST | /api/pedidos | Termina el pedido: guarda en `pedidos` y `detalle_pedido` y vacía `temp_pizza` |
| GET | /api/pedidos/<id_pedido>/detalle | Detalle de un pedido |
| GET | /api/ventas/dia/<dia> | Ventas por día de la semana |
| GET | /api/ventas/mes/<mes> | Ventas por mes |
