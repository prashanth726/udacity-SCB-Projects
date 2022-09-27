import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LocalService {

  constructor() { }

  public saveData(key: any, value: any) {
    localStorage.setItem(key, value);
  }

  public getData(key: any) {
    return localStorage.getItem(key)
  }

  public getAllData() {
    return localStorage
  }

  public removeData(key: any) {
    localStorage.removeItem(key);
  }

  public clearData() {
    localStorage.clear();
  }
}