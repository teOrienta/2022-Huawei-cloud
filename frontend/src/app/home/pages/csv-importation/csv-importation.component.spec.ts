import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CsvImportationComponent } from './csv-importation.component';

describe('CsvImportationComponent', () => {
  let component: CsvImportationComponent;
  let fixture: ComponentFixture<CsvImportationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CsvImportationComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CsvImportationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
