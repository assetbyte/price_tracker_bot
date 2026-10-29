import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {environment} from '../../environments/environment';
import { HttpClient, HttpParams } from '@angular/common/http';
export interface Station {
  name: string; 
  code: string;
}

@Injectable({
  providedIn: 'root',
})


export class Stations {
  private apiURL = environment.apiUrl + '/api/stations/';
  constructor(private http: HttpClient) {}

  getStations(query?: string): Observable<Station[]> {
    let params = new HttpParams();
    if (query) {
      params = params.set('query', query);
    }
    return this.http.get<Station[]>(this.apiURL, { params });
  }

}
