import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { FlowGraphParams } from 'src/app/shared/types/flow-graph-params';
import { HomeFacade } from '../../home.facade';
import { formatDate } from '@angular/common';

@Component({
  selector: 'app-filter-page',
  templateUrl: './filter-page.component.html',
  styleUrls: ['./filter-page.component.scss'],
})
export class FilterPageComponent implements OnInit {
  form: FormGroup;
  detailLevel: number = 0;
  timeOutState: NodeJS.Timeout = {} as NodeJS.Timeout;
  valueRange: number = 0;

  acquisition!: string; 
  acquisitionFilter!: string[];

  county!: string;
  countyFilter!: string[];

  suggestions: string[] = ["modalit1", "mod2", "mod3"]; 
  @ViewChild('graph', { static: false }) graph!: ElementRef;

  constructor(
    private formbuilder: FormBuilder,
    private homeFacade: HomeFacade
  ) {

    this.form = formbuilder.group({
      startDate: [null],
      endDate: [null],
      detailLevel: [0],
      mode: ['frequency'],
      valueRange: [0],
      acquisition: [null],
      county: [null],
    });

    this.form.valueChanges.subscribe((e) => {
      this.updateBounce();
    });
  }

  ngOnInit(): void {}

  updateBounce() {
    if (this.timeOutState) {
      clearTimeout(this.timeOutState);
    }
    this.timeOutState = setTimeout(() => {
      this.updateFlow();
    }, 1000);
  }

  updateFlow() {
    const formatedDates = {
      start: this.form.controls['startDate'].value
        ? formatDate(this.form.controls['startDate'].value, 'd/MM/yy', 'pt-BR')
        : null,
      end: this.form.controls['endDate'].value
        ? formatDate(this.form.controls['endDate'].value, 'd/MM/yy', 'pt-BR')
        : null,
    };
    const graphParams: FlowGraphParams = {
      start_date: formatedDates.start,
      end_date: formatedDates.end,
      detailLevel: this.form.controls['detailLevel'].value,
      mode: this.form.controls['mode'].value,
    };
    this.homeFacade.setGraphParams(graphParams);
  }

  searchAcquisition(event: any) {

  }

  searchCounty(event: any) {

  }

}
