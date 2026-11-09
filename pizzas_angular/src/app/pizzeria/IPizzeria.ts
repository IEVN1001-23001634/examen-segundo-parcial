export interface ClientePedido {
    nombre: string;
    direccion: string;
    telefono: string;
    fecha: string;
}

export interface PizzaTemp {
    id_temp: number;
    tamano: string;
    ingredientes: string;
    num_pizzas: number;
    subtotal: number;
}

export interface PedidoVenta {
    id_pedido: number;
    nombre_cliente: string;
    direccion: string;
    telefono: string;
    fecha_compra: string;
    total: number;
}

export interface DetallePedido {
    id_detalle: number;
    tamano: string;
    ingredientes: string;
    num_pizzas: number;
    subtotal: number;
}
