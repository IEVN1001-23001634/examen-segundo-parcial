CREATE DATABASE IF NOT EXISTS pizzeria_db;
USE pizzeria_db;

CREATE TABLE temp_pizza (
    id_temp INT AUTO_INCREMENT PRIMARY KEY,
    tamano VARCHAR(20) NOT NULL,
    ingredientes VARCHAR(100) NOT NULL,
    num_pizzas INT NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL
);

CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    nombre_cliente VARCHAR(100) NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    fecha_compra DATE NOT NULL,
    total DECIMAL(10, 2) NOT NULL
);

CREATE TABLE detalle_pedido (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    tamano VARCHAR(20) NOT NULL,
    ingredientes VARCHAR(100) NOT NULL,
    num_pizzas INT NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE
);
