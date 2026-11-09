import { Component, OnInit, signal } from '@angular/core';
import { FormGroup, FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { PizzeriaService } from '../pizzeria.service';

@Component({
  imports: [ReactiveFormsModule, CommonModule, RouterLink],
  selector: 'app-pedido',
  templateUrl: './pedido.html',
})
export class Pedido implements OnInit {
  formGroup!: FormGroup;
  mensaje = signal('');
  exito = signal(true);

  tamanos = [
    { valor: 'Chica', precio: 40 },
    { valor: 'Mediana', precio: 80 },
    { valor: 'Grande', precio: 120 }
  ];

  constructor(
    private fb: FormBuilder,
    public pizzeria: PizzeriaService
  ) {}

  ngOnInit(): void {
    this.formGroup = this.initForm();
  }

  initForm(): FormGroup {
    return this.fb.group({
      nombre: [this.pizzeria.cliente.nombre, [Validators.required, Validators.minLength(3)]],
      direccion: [this.pizzeria.cliente.direccion, [Validators.required]],
      telefono: [this.pizzeria.cliente.telefono, [Validators.required, Validators.pattern(/^[0-9\-\s]{7,15}$/)]],
      fecha: [this.pizzeria.cliente.fecha || this.hoy(), [Validators.required]],
      tamano: ['', [Validators.required]],
      jamon: [false],
      pina: [false],
      champinones: [false],
      numPizzas: ['', [Validators.required, Validators.min(1), Validators.max(50)]]
    });
  }

  hoy(): string {
    const fecha = new Date();
    const mes = String(fecha.getMonth() + 1).padStart(2, '0');
    const dia = String(fecha.getDate()).padStart(2, '0');
    return `${fecha.getFullYear()}-${mes}-${dia}`;
  }

  invalido(campo: string): boolean {
    const control = this.formGroup.get(campo);
    return !!control && control.touched && control.invalid;
  }

  onSubmit(): void {
    if (this.formGroup.invalid) {
      this.formGroup.markAllAsTouched();
      this.exito.set(false);
      this.mensaje.set('Revisa los campos marcados en rojo');
      return;
    }

    const datos = this.formGroup.getRawValue();

    this.pizzeria.cliente = {
      nombre: datos.nombre,
      direccion: datos.direccion,
      telefono: datos.telefono,
      fecha: datos.fecha
    };

    const ingredientes: string[] = [];
    if (datos.jamon) ingredientes.push('Jamón');
    if (datos.pina) ingredientes.push('Piña');
    if (datos.champinones) ingredientes.push('Champiñones');

    const pizza = {
      tamano: datos.tamano,
      ingredientes: ingredientes.join(', '),
      num_pizzas: Number(datos.numPizzas)
    };

    this.pizzeria.agregarPizza(pizza).subscribe({
      next: (respuesta) => {
        this.exito.set(true);
        this.mensaje.set(respuesta?.mensaje ?? 'Pizza agregada al pedido');

        this.formGroup.patchValue({
          tamano: '',
          jamon: false,
          pina: false,
          champinones: false,
          numPizzas: ''
        });
        this.formGroup.get('tamano')?.markAsUntouched();
        this.formGroup.get('numPizzas')?.markAsUntouched();
      },
      error: (error) => {
        console.error('Error al agregar la pizza:', error);
        this.exito.set(false);
        this.mensaje.set(error?.error?.mensaje ?? 'No se pudo agregar la pizza, revisa que la API esté corriendo');
      }
    });
  }
}
