import { TestBed } from '@angular/core/testing';

import { EdaRaportServiceService } from './eda-raport-service.service';

describe('EdaRaportServiceService', () => {
  let service: EdaRaportServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EdaRaportServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
