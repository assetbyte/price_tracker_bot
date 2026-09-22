import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class TelegramService {
  private readonly STORAGE_KEY = 'tg_init_data';

  private get tg() {
    return window.Telegram?.WebApp;
  }

  constructor() {
    if (this.tg) {
      this.tg.ready();
      this.tg.expand();
    } else {
      console.warn('Telegram WebApp SDK not found');
    }
  }

  get initData(): string {
    const freshData = this.tg?.initData;

    if (freshData && freshData.includes('hash=')) {
      localStorage.setItem(this.STORAGE_KEY, freshData);
      return freshData;
    }

    const cachedData = localStorage.getItem(this.STORAGE_KEY);
    if (cachedData && cachedData.includes('hash=')) {
      return cachedData;
    }

    return '';
  }

  get user() {
    return this.tg?.initDataUnsafe?.user;
  }

  get isInsideTelegram(): boolean {
    return !!this.tg && this.initData.length > 0;
  }
}