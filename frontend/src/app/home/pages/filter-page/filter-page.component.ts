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
  timeOutState: NodeJS.Timeout = {} as NodeJS.Timeout;

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
    console.log(this.form.value);
  }
}
