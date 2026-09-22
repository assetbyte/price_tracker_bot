import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TrackingService, Tracking, PriceHistory } from '../../services/tracking';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {
  trackings: Tracking[] = [];
  
  priceHistories: { [trackingId: number]: PriceHistory[] } = {};

  constructor(
    private cdr: ChangeDetectorRef, 
    private trackingService: TrackingService
  ) {}

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {
    this.trackingService.getActiveTrackings().subscribe({
      next: (trackings) => {
        this.trackings = trackings;

        this.trackings.forEach((tracking) => {
          if (tracking.id) {
            this.loadHistoryForTracking(tracking.id);
          }
        });

        this.cdr.detectChanges();
      },
      error: (err) => console.error('Error', err)
    });
  }

  loadHistoryForTracking(trackingId: number): void {
    this.trackingService.getPriceHistory(trackingId).subscribe({
      next: (history) => {
      
        this.priceHistories[trackingId] = history;
        this.cdr.detectChanges();
      },
      error: (err) => console.error(`Error loading history for ${trackingId}:`, err)
    });
  }
}