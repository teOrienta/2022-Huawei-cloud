import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { FlowGraphParams } from 'src/app/shared/types/flow-graph-params';
import { HomeFacade } from '../../home.facade';
import { formatDate } from '@angular/common';
import { Subscription } from 'rxjs';
import { SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-filter-page',
  templateUrl: './filter-page.component.html',
  styleUrls: ['./filter-page.component.scss'],
})
export class FilterPageComponent implements OnInit, OnDestroy {
  form: FormGroup;
  detailLevel: number = 0;
  timeOutState: NodeJS.Timeout = {} as NodeJS.Timeout;
  mode: string = 'frequency';

  subscriptionP!: Subscription;
  subscriptionF!: Subscription;

  frequencyGraph!: SafeHtml | null;
  performanceGraph!: SafeHtml | null;
  graphSource!: SafeHtml | null;

  constructor(
    private formbuilder: FormBuilder,
    private homeFacade: HomeFacade
  ) {

    this.form = formbuilder.group({
      startDate: [null],
      endDate: [null],
      detailLevel: [0],
      mode: ['frequency'],
    });

    this.form.valueChanges.subscribe((e) => {
      this.updateBounce();
    });

    this.homeFacade.filterFlowGraph(this.form.value);
    this.setGraph();
  }

  ngOnInit(): void {
    this.changeMode('frequency');
  }

  updateBounce() {
    if (this.timeOutState) {
      clearTimeout(this.timeOutState);
    }
    this.timeOutState = setTimeout(() => {
      this.updateFlow();
    }, 1000);
  }

  setGraph() {
    this.subscriptionP = this.homeFacade.getPerformanceGraph().subscribe({
      next: (flow) => {
        this.performanceGraph = flow;
      },
    });
    this.subscriptionF = this.homeFacade.getFrequencyGraph().subscribe({
      next: (flow) => {
        this.frequencyGraph = flow;
      },
    });
  }

  changeMode(mode: string) {
    if (mode === 'frequency') {
      this.graphSource = this.frequencyGraph;
    } else {
      this.graphSource = this.performanceGraph;
    }
  }

  updateFlow() {
    const formattedDates = {
      start: this.form.controls['startDate'].value
        ? formatDate(this.form.controls['startDate'].value, 'y-MM-dd', 'pt-BR')
        : null,
      end: this.form.controls['endDate'].value
        ? formatDate(this.form.controls['endDate'].value, 'y-MM-dd', 'pt-BR')
        : null,
    };
    const graphParams: FlowGraphParams = {
      startDate: formattedDates.start,
      endDate: formattedDates.end,
      detailLevel: this.form.controls['detailLevel'].value,
    };
    this.homeFacade.filterFlowGraph(graphParams);
  }

  ngOnDestroy(): void {
    if (this.subscriptionP) {
      this.subscriptionP.unsubscribe();
    }
    if (this.subscriptionF) {
      this.subscriptionF.unsubscribe();
    }
  }
}
