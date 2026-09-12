import { Routes } from '@angular/router';
import { TrackingList } from './components/tracking-list/tracking-list';
import { TrackingCreate } from './components/tracking-create/tracking-create';



export const routes: Routes = [
    { path: 'trackings', component: TrackingList},
    { path: 'tracking-create', component: TrackingCreate},
    
];
