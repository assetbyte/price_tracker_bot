import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { TrackingService } from '../../services/tracking';

interface Station {
  name: string;
  code: string;
}

@Component({
  selector: 'app-tracking-create',
  imports: [FormsModule],
  templateUrl: './tracking-create.html',
  styleUrl: './tracking-create.css',
})
export class TrackingCreate {
  
  stations: Station[] = [
    { name: 'Астана', code: '2708001' },
    { name: 'Алматы', code: '2700000' },
    { name: 'Шымкент', code: '2700770' },
  ];

  formData = {
    user_id: '',
    origin_name: '',
    origin_code: '',
    destination_name: '',
    destination_code: '',
    departure_date: '',
    car_type: '',
    target_price: '',
  };

  constructor(private trackingService: TrackingService, public router: Router) {}

  onOriginChange(stationName: string): void {
    const found = this.stations.find((s) => s.name === stationName);
    if (found) {
      this.formData.origin_code = found.code;
    }
  }

  onDestinationChange(stationName: string): void {
    const found = this.stations.find((s) => s.name === stationName);
    if (found) {
      this.formData.destination_code = found.code;
    }
  }

  onSubmit(): void {
    this.trackingService.createTracking(this.formData as any).subscribe({
      next: (data) => {
        this.router.navigate(['/trackings']);
      },
      error: (err) => {
        console.error('Error creating tracking:', err);
      },
    });
  }
}