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
export class TrackingList {
  trackings: Tracking[] = []

  constructor(private cdr: ChangeDetectorRef, private trackingService: TrackingService) {}

  ngOnInit() : void {
    this.loadTrackings()
    console.log(this.trackings)
  }

  loadTrackings() : void {
    this.trackingService.getActiveTrackings().subscribe({
      next: (data: Tracking[]) => {
        this.trackings = data;
        console.log("Ac", this.trackings)
        this.cdr.detectChanges()
      },
      error: (err) => {
        console.log("Error occured", err)
      }
    })
  }
  

}
