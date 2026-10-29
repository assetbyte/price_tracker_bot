import { HttpInterceptorFn } from '@angular/common/http';
import { environment } from '../../environments/environment';

export const tunnelBypassInterceptor: HttpInterceptorFn = (req, next) => {
  
  if (req.url.startsWith(environment.apiUrl)) {
    const modifiedReq = req.clone({
      setHeaders: {
        'bypass-tunnel-reminder': 'true'
      }
    });
    return next(modifiedReq);
  }
  return next(req);
};