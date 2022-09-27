import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Product } from '../../models/Product';
import { ProductService } from '../../services/product.service';

@Component({
  selector: 'app-product-item-detail',
  templateUrl: './product-item-detail.component.html',
  styleUrls: ['./product-item-detail.component.css']
})
export class ProductItemDetailComponent implements OnInit {
  id:number;
  product: Product;
  qty:number =1;
  constructor(private route: ActivatedRoute, private productService: ProductService, private router: Router) {
    this.id=0;
    this.product = {
      id: 0,
      name: '',
      description: '',
      price: 0,
      url: ''
    }
   }

   ngOnInit(): void {

    this.route.params.subscribe((params) => {
      this.id = params['id'];
    });

    this.productService.getProducts().subscribe(data => {
      let result = data.filter(obj => {
        return obj.id == this.id;
      });
      if(result.length>0){
        this.product = result[0]
      }
     else{
      // no product with given id, so redirect to homepage
      this.router.navigate(['/']);
     }
      
    })
  }

}
