import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class TelegramService {
  private tg = window.Telegram?.WebApp
  constructor(){
    if (this.tg) {
      this.tg.ready();
      this.tg.expand();
    }
    console.warn('Errpr');

  }
  get initData(): string {
    return this.tg?.initData || '';
  }

  
  get user() {
    return this.tg?.initDataUnsafe?.user;
  }

   
   
  get isInsideTelegram(): boolean {
    return !!this.tg && this.initData.length > 0;
  }
  
}
