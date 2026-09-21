import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { TrackingService, Tracking } from '../../services/tracking';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-tracking-list',
  imports: [CommonModule, RouterLink],
  templateUrl: './tracking-list.html',
  styleUrl: './tracking-list.css',
})
export class TrackingList implements OnInit {
  trackings: Tracking[] = [];

  constructor(
    private cdr: ChangeDetectorRef, 
    private trackingService: TrackingService
  ) {}

  ngOnInit(): void {
    this.loadTrackings();
  }

  loadTrackings(): void {
    this.trackingService.getActiveTrackings().subscribe({
      next: (data: Tracking[]) => {
        this.trackings = data;
        this.cdr.detectChanges();
      },
      error: (err) => console.error("Error occurred", err)
    });
  }


  togglePause(item: Tracking): void {
    if (!item.id) return;
    const request$ = item.is_active ? this.trackingService.pauseTracking(item.id): this.trackingService.resumeTracking(item.id);

    request$.subscribe({
      next: (updated: Tracking) => {
        item.is_active = updated.is_active;
        this.cdr.detectChanges();
      },
      error: (err) => console.error('Failed to toggle tracking status', err)
    });
  }

  deleteTracking(item: Tracking): void {
    if (!item.id) return;

    this.trackingService.deleteTracking(item.id).subscribe({
      next: (data) => {
        this.trackings = this.trackings.filter(t => t.id !== item.id);
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error("Something went wrong")
      }
    })

  }

  
}