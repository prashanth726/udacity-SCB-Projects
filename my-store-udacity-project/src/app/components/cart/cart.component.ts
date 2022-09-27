import { Component, OnInit } from '@angular/core';
import { LocalService } from '../../services/local.service';
import { Product } from '../../models/Product';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit {

  products: Product[] = [];
  fullname: string = '';
  address: string = '';
  creditcard: string = '';
  totalPrice: number =0;
  constructor(private localService: LocalService, private route: ActivatedRoute, private router: Router) { }

  ngOnInit(): void {
    const data = this.localService.getAllData()
    for (const key of Object.keys(data)) {
      this.products.push(JSON.parse(data[key]));
  }
  this.totalPrice = 0;
  this.products.forEach( (item, index) =>
  {
    this.totalPrice += (item.price * item.qty);
  });
  }

  submitForm(): void
  {
    this.localService.clearData()
    this.router.navigate(['/confirmation']);
  }


}
