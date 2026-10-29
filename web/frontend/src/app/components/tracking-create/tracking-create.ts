import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CreateTrackingPayload, TrackingService } from '../../services/tracking';
import { TelegramService } from '../../services/telegram';
import { Stations, Station } from '../../services/stations'; 

@Component({
  selector: 'app-tracking-create',
  imports: [FormsModule],
  templateUrl: './tracking-create.html',
  styleUrl: './tracking-create.css',
})
export class TrackingCreate implements OnInit {
  
  stations: Station[] = [];

  formData: CreateTrackingPayload = {
    origin_name: '',
    origin_code: '',
    destination_name: '',
    destination_code: '',
    departure_date: '',
    car_type: '',
    target_price: '',
  };

  constructor(
    private trackingService: TrackingService,
    private stationsService: Stations, 
    public router: Router,
    private telegram: TelegramService
  ) {}

  ngOnInit(): void {
    const rawData = this.telegram.initData;
    console.log(rawData);
    if (this.telegram.user) {
      console.log('Привет,', this.telegram.user.first_name);
    }

    this.loadStations();
  }

  loadStations(query?: string): void {
    this.stationsService.getStations(query).subscribe({
      next: (data: Station[]) => { 
        this.stations = data;
      },
      error: (err: any) => { 
        console.error('Error fetching stations:', err);
      }
    });
  }

  onOriginChange(stationName: string): void {
    const found = this.stations.find((s) => s.name === stationName);
    if (found) {
      this.formData.origin_name = found.name; 
      this.formData.origin_code = found.code;
    }
  }

  onDestinationChange(stationName: string): void {
    const found = this.stations.find((s) => s.name === stationName);
    if (found) {
      this.formData.destination_name = found.name;
      this.formData.destination_code = found.code;
    }
  }

  onSubmit(): void {
    this.trackingService.createTracking(this.formData).subscribe({
      next: () => {
        this.router.navigate(['/trackings']);
      },
      error: (err: any) => {
        console.error('Error creating tracking:', err);
      },
    });
  }
}