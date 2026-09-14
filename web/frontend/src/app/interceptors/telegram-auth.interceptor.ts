import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { TelegramService } from '../services/telegram'; 

export const telegramAuthInterceptor: HttpInterceptorFn = (req, next) => {
  const telegramService = inject(TelegramService);
  const initData = telegramService.initData;

  if (initData) {
    const authReq = req.clone({
      headers: req.headers.set('X-Telegram-Init-Data', initData),
    });
    return next(authReq);
  }

  return next(req);
};