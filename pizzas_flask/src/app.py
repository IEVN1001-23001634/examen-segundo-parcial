from flask import Flask
from flask_cors import CORS
from config import config
from blueprints.database import mysql
from blueprints.pizzas.routes import pizzas_bp
from blueprints.pedidos.routes import pedidos_bp
from blueprints.ventas.routes import ventas_bp

app = Flask(__name__)

CORS(app)
app.config.from_object(config['development'])
mysql.init_app(app)

app.register_blueprint(pizzas_bp, url_prefix='/api/pizzas')
app.register_blueprint(pedidos_bp, url_prefix='/api/pedidos')
app.register_blueprint(ventas_bp, url_prefix='/api/ventas')


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "<h1> Pagina no encontrada</h1>", 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
