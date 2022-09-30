import { Component, OnInit } from '@angular/core';
import { LocalService } from '../../services/local.service';

@Component({
  selector: 'app-confirmation',
  templateUrl: './confirmation.component.html',
  styleUrls: ['./confirmation.component.css']
})
export class ConfirmationComponent implements OnInit {
  fullname: string = '';
  address: string = '';
  constructor(private localService: LocalService) { }

  ngOnInit(): void {
    const data = JSON.parse(this.localService.getData("cartOwner") || '{}')
    this.fullname = data.fullname
    this.address = data.address
  }

}
