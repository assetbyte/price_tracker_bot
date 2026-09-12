import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrackingList } from './tracking-list';

describe('TrackingList', () => {
  let component: TrackingList;
  let fixture: ComponentFixture<TrackingList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TrackingList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TrackingList);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
