import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { HomeFacade } from '../../home.facade';

@Component({
  selector: 'app-filter-page',
  templateUrl: './filter-page.component.html',
  styleUrls: ['./filter-page.component.scss'],
})
export class FilterPageComponent implements OnInit {
  form: FormGroup;
  detailLevel: number = 0;

  constructor(
    private formbuilder: FormBuilder,
    private homeFacade: HomeFacade
  ) {
    this.form = formbuilder.group({
      startDate: [null],
      endDate: [null],
      detailLevel: [null],
      mode: ['frequency'],
    });
  }

  ngOnInit(): void {}
}
