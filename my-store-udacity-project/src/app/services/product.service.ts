import { Injectable } from '@angular/core';
import { Product } from '../models/Product';
import { Observable } from 'rxjs';
import { HttpClient } from "@angular/common/http";
import { LocalService } from '../services/local.service';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  constructor(private httpClient: HttpClient, private localStore: LocalService) { 


  }

  addToCart(p: Product, qty: number): void

  {
    console.log("Product: ", p);
    this.localStore.saveData(p.id, JSON.stringify({...p,qty:qty}) );
  }

  // getProductsFromCart(): void
  // {
  //   return this.localStore.getAllData;
  // }

  getProducts(): Observable<Product[]>
  {
    const url = "assets/data.json";
    return this.httpClient.get<Product[]>(url);
  }

}
