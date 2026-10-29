import { TestBed } from '@angular/core/testing';

import { Stations } from './stations';

describe('Stations', () => {
  let service: Stations;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Stations);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
