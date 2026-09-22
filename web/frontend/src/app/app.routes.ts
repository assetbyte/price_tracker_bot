import { Routes } from '@angular/router';
import { TrackingList } from './components/tracking-list/tracking-list';
import { TrackingCreate } from './components/tracking-create/tracking-create';
import { Dashboard } from './components/dashboard/dashboard';



export const routes: Routes = [
    { path: '', component: Dashboard},
    { path: 'trackings', component: TrackingList},
    { path: 'tracking-create', component: TrackingCreate},
    {path: 'dashboard', component: Dashboard},
    
];
