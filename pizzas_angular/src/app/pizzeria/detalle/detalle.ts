import { Component, OnInit, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { PizzeriaService } from '../pizzeria.service';
import { PizzaTemp } from '../IPizzeria';

@Component({
  imports: [CommonModule, RouterLink],
  selector: 'app-detalle',
  templateUrl: './detalle.html',
})
export class Detalle implements OnInit {
  dataSource = signal<PizzaTemp[]>([]);
  mensaje = signal('');
  exito = signal(true);

  total = computed(() =>
    this.dataSource().reduce((suma, pizza) => suma + Number(pizza.subtotal), 0)
  );

  constructor(public pizzeria: PizzeriaService) {}

  ngOnInit(): void {
    this.cargarPizzas();
  }

  cargarPizzas(): void {
    this.pizzeria.getPizzas().subscribe({
      next: (response: any) => {
        this.dataSource.set(response.pizzas);
      },
      error: (error) => {
        console.error('Error:', error);
        this.exito.set(false);
        this.mensaje.set('No se pudo cargar el pedido, revisa que la API esté corriendo');
      }
    });
  }

  quitar(id: number): void {
    this.pizzeria.quitarPizza(id).subscribe({
      next: (response: any) => {
        if (response && response.exito) {
          this.mensaje.set('');
          this.cargarPizzas();
        }
      },
      error: (error) => {
        console.error('Error al quitar la pizza:', error);
        this.exito.set(false);
        this.mensaje.set(error?.error?.mensaje ?? 'No se pudo quitar la pizza');
      }
    });
  }

  terminar(): void {
    const cliente = this.pizzeria.cliente;

    if (!cliente.nombre || !cliente.direccion || !cliente.telefono || !cliente.fecha) {
      this.exito.set(false);
      this.mensaje.set('Captura los datos del cliente en la página Pedido antes de terminar');
      return;
    }

    if (this.dataSource().length === 0) {
      this.exito.set(false);
      this.mensaje.set('Agrega al menos una pizza al pedido');
      return;
    }

    this.pizzeria.terminarPedido(cliente).subscribe({
      next: (response: any) => {
        if (response && response.exito) {
          this.exito.set(true);
          this.mensaje.set(response.mensaje);
          this.pizzeria.cliente = { nombre: '', direccion: '', telefono: '', fecha: '' };
          this.cargarPizzas();
        }
      },
      error: (error) => {
        console.error('Error al terminar el pedido:', error);
        this.exito.set(false);
        this.mensaje.set(error?.error?.mensaje ?? 'No se pudo guardar el pedido, revisa que la API esté corriendo');
      }
    });
  }
}
