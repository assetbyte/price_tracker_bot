import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { TelegramService } from '../services/telegram'; 

export const telegramAuthInterceptor: HttpInterceptorFn = (req, next) => {
  const telegramService = inject(TelegramService);
  const initData = telegramService.initData;

  let headers = req.headers.set('bypass-tunnel-reminder', 'true');

  if (initData) {
    headers = headers.set('X-Telegram-Init-Data', initData);
  }

  const authReq = req.clone({ headers });
  return next(authReq);
};