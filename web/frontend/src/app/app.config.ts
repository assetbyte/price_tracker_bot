import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { telegramAuthInterceptor } from './interceptors/telegram-auth.interceptor';
import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { tunnelBypassInterceptor } from './interceptors/tunnel-bypass.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideHttpClient(withInterceptors([telegramAuthInterceptor])),
    provideHttpClient(withInterceptors([tunnelBypassInterceptor])),
  ]
};
