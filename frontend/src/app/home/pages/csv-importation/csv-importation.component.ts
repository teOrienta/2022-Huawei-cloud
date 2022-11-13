import { Component, OnInit } from '@angular/core';
import { HomeFacade } from '../../home.facade';
import { SafeHtml } from '@angular/platform-browser';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-csv-importation',
  templateUrl: './csv-importation.component.html',
  styleUrls: ['./csv-importation.component.scss']
})
export class CsvImportationComponent implements OnInit {

  graphSource!: SafeHtml | null;
  form: FormGroup;

  constructor(
    homeFacade: HomeFacade,
    private formbuilder: FormBuilder,
  ) { 
    this.form = formbuilder.group({
      startDate: [null],
      endDate: [null],
      case: [""],
      activity: [""],
      orgResource: [""],
    });
  }

  

  ngOnInit(): void {
  }



}
