import { Component, OnInit, Input } from '@angular/core';
import { Product } from '../../models/Product';
import { ProductService } from '../../services/product.service';

@Component({
  selector: 'app-product-item',
  templateUrl: './product-item.component.html',
  styleUrls: ['./product-item.component.css']
})
export class ProductItemComponent implements OnInit {

  @Input() product: Product;
  qty:number =1;
  constructor(private productService: ProductService) {
    this.product = {
    id: 0,
    name: '',
    description: '',
    price: 0,
    url: '',
    qty:0
  }
 }

  ngOnInit(): void {
  }

  addProductsToCart(p: Product, num: number): void
  {
    if(num > 0)
    {
      this.productService.addToCart(p, this.qty);
      window.alert(`${num} ${p.name} 's added to cart sucessfully, please click on cart to proceed`);
      this.qty = 1;
    }
    else
    {
      window.alert(`can not  order items`);
    }
  }

}
