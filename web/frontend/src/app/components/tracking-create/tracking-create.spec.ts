import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrackingCreate } from './tracking-create';

describe('TrackingCreate', () => {
  let component: TrackingCreate;
  let fixture: ComponentFixture<TrackingCreate>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TrackingCreate]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TrackingCreate);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
