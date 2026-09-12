import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Tracking {
  id?: number;
  user_id: number;
  origin_code: string;
  destination_code: string;
  origin_name: string;
  destination_name: string;
  departure_date: string;
  transport_type: string;
  price?: number | null;
  target_price: number;
  car_type: string;
  is_active?: boolean;
  created_at?: string;
}

@Injectable({
  providedIn: 'root',
})
export class TrackingService {

  private apiUrl = 'http://localhost:8000/api/trackings/';

  constructor(private http: HttpClient) {}
  

  getActiveTrackings() : Observable<Tracking[]> {
    return this.http.get<Tracking[]>(this.apiUrl);
  }

  createTracking(data: Tracking) :  Observable<Tracking> {
    return this.http.post<Tracking>(this.apiUrl, data)
  }

  deleteTracking(id: number, userId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/?user_id=${userId}`)
  }

}
