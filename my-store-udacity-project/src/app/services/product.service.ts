import { Injectable } from '@angular/core';
import { Product } from '../models/Product';
import { Observable } from 'rxjs';
import { HttpClient } from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  constructor(private httpClient: HttpClient) { 


  }

  getProducts(): Observable<Product[]>
  {
    const url = "assets/data.json";
    return this.httpClient.get<Product[]>(url);
  }

}
