import {ChangeDetectorRef,Component,ElementRef,OnInit,QueryList,ViewChildren,OnDestroy} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Chart, registerables } from 'chart.js';
import { TrackingService, Tracking, PriceHistory } from '../../services/tracking';

Chart.register(...registerables);

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit, OnDestroy {
  trackings: Tracking[] = [];
  priceHistories: { [trackingId: number]: PriceHistory[] } = {};

  @ViewChildren('chartCanvas') chartCanvases!: QueryList<ElementRef<HTMLCanvasElement>>;

  private chartInstances: { [trackingId: number]: Chart } = {};

  constructor(
    private cdr: ChangeDetectorRef,
    private trackingService: TrackingService
  ) {}

  ngOnInit(): void {
    this.loadDashboard();
  }

  ngOnDestroy(): void {
    Object.values(this.chartInstances).forEach((chart) => chart.destroy());
  }

  loadDashboard(): void {
    this.trackingService.getActiveTrackings().subscribe({
      next: (trackings) => {
        this.trackings = trackings;
        this.cdr.detectChanges();

        this.trackings.forEach((tracking) => {
          if (tracking.id) {
            this.loadHistoryForTracking(tracking.id);
          }
        });
      },
      error: (err) => console.error('Ошибка загрузки трекингов:', err),
    });
  }

  loadHistoryForTracking(trackingId: number): void {
    this.trackingService.getPriceHistory(trackingId).subscribe({
      next: (history) => {
        this.priceHistories[trackingId] = history;
        this.cdr.detectChanges();
        
        this.renderChartForTracking(trackingId);
      },
      error: (err) => console.error(`Ошибка истории для ${trackingId}:`, err),
    });
  }

  private renderChartForTracking(trackingId: number): void {
    const history = this.priceHistories[trackingId];
    if (!history || history.length === 0) return;

    const canvasRef = this.chartCanvases.find(
      (ref) => ref.nativeElement.getAttribute('data-id') === String(trackingId)
    );

    if (!canvasRef) return;

    if (this.chartInstances[trackingId]) {
      this.chartInstances[trackingId].destroy();
    }

    const ctx = canvasRef.nativeElement.getContext('2d');
    if (!ctx) return;

    const labels = history.map((item) => {
      const d = new Date(item.time);
      return `${d.getDate().toString().padStart(2, '0')}.${(d.getMonth() + 1).toString().padStart(2, '0')} ${d.getHours()}:00`;
    });

    const prices = history.map((item) => item.price);

    const gradient = ctx.createLinearGradient(0, 0, 0, 150);
    gradient.addColorStop(0, 'rgba(36, 129, 204, 0.35)');
    gradient.addColorStop(1, 'rgba(36, 129, 204, 0.0)');

    this.chartInstances[trackingId] = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Price (₸)',
            data: prices,
            borderColor: '#2481cc',
            borderWidth: 2,
            backgroundColor: gradient,
            fill: true,
            tension: 0.3,
            pointRadius: 3,
            pointBackgroundColor: '#2481cc',
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: { grid: { display: false }, ticks: { font: { size: 10 } } },
          y: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { font: { size: 10 } } },
        },
      },
    });
  }
}