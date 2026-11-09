import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ClientePedido } from './IPizzeria';

@Injectable({
    providedIn: 'root'
})
export class PizzeriaService {
    private readonly api = 'http://127.0.0.1:5000/api';

    cliente: ClientePedido = {
        nombre: '',
        direccion: '',
        telefono: '',
        fecha: ''
    };

    constructor(private http: HttpClient){ }

    public getPizzas(): Observable<any>{
        return this.http.get<any>(`${this.api}/pizzas`);
    }

    agregarPizza(datos: any): Observable<any> {
        return this.http.post<any>(`${this.api}/pizzas`, datos);
    }

    quitarPizza(id: number): Observable<any> {
        return this.http.delete<any>(`${this.api}/pizzas/${id}`);
    }

    terminarPedido(datos: ClientePedido): Observable<any> {
        return this.http.post<any>(`${this.api}/pedidos`, datos);
    }

    public getVentasDia(dia: string): Observable<any>{
        return this.http.get<any>(`${this.api}/ventas/dia/${encodeURIComponent(dia)}`);
    }

    public getVentasMes(mes: string): Observable<any>{
        return this.http.get<any>(`${this.api}/ventas/mes/${encodeURIComponent(mes)}`);
    }

    public getDetallePedido(id: number): Observable<any>{
        return this.http.get<any>(`${this.api}/pedidos/${id}/detalle`);
    }
}
