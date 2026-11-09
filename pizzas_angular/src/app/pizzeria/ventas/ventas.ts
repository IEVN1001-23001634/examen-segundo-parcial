import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { PizzeriaService } from '../pizzeria.service';
import { DetallePedido, PedidoVenta } from '../IPizzeria';

@Component({
  imports: [FormsModule, CommonModule, RouterLink],
  selector: 'app-ventas',
  templateUrl: './ventas.html',
})
export class Ventas implements OnInit {
  dia: string = '';
  mes: string = '';
  titulo = signal('Ventas');
  dataSource = signal<PedidoVenta[]>([]);
  total = signal(0);
  detalle = signal<DetallePedido[]>([]);
  ventaAbierta = signal<number | null>(null);
  error = signal('');

  dias: string[] = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'];
  meses: string[] = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
  ];

  constructor(public pizzeria: PizzeriaService) {}

  ngOnInit(): void {
    this.dia = new Date().toLocaleDateString('es-MX', { weekday: 'long' });
    this.consultarDia();
  }

  consultarDia(): void {
    if (!this.dia.trim()) {
      return;
    }
    this.pizzeria.getVentasDia(this.dia.trim()).subscribe({
      next: (response: any) => {
        this.mostrar(response, 'Ventas del día: ' + this.dia.trim());
      },
      error: (error) => this.fallo(error)
    });
  }

  consultarMes(): void {
    if (!this.mes.trim()) {
      return;
    }
    this.pizzeria.getVentasMes(this.mes.trim()).subscribe({
      next: (response: any) => {
        this.mostrar(response, 'Ventas del mes: ' + this.mes.trim());
      },
      error: (error) => this.fallo(error)
    });
  }

  verDetalle(id: number): void {
    if (this.ventaAbierta() === id) {
      this.ventaAbierta.set(null);
      this.detalle.set([]);
      return;
    }
    this.pizzeria.getDetallePedido(id).subscribe({
      next: (response: any) => {
        this.detalle.set(response.detalle);
        this.ventaAbierta.set(id);
      },
      error: (error) => this.fallo(error)
    });
  }

  private mostrar(response: any, titulo: string): void {
    this.dataSource.set(response.ventas);
    this.total.set(response.total);
    this.titulo.set(titulo);
    this.error.set('');
    this.ventaAbierta.set(null);
    this.detalle.set([]);
  }

  private fallo(error: any): void {
    console.error('Error:', error);
    this.error.set(error?.error?.mensaje ?? 'No se pudo consultar la API');
  }
}
