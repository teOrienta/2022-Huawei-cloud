import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { FlowGraphParams } from 'src/app/shared/types/flow-graph-params';
import { HomeFacade } from '../../home.facade';
import { formatDate } from '@angular/common';
import { Subscription } from 'rxjs';
import { SafeHtml } from '@angular/platform-browser';
import Statistics from 'src/app/shared/types/statistics';

@Component({
  selector: 'app-filter-page',
  templateUrl: './filter-page.component.html',
  styleUrls: ['./filter-page.component.scss'],
})
export class FilterPageComponent implements OnInit, OnDestroy {
  form: FormGroup;
  detailLevel: number = 0;
  mode: string = 'frequency';

  statistics: Statistics = {} as Statistics;

  subscriptionP!: Subscription;
  subscriptionF!: Subscription;
  subscriptionS!: Subscription;
  subscriptionA!: Subscription;

  frequencyGraph!: SafeHtml | null;
  performanceGraph!: SafeHtml | null;
  graphSource!: SafeHtml | null;

  initialDate: Date = new Date();
  maxDate: Date = new Date();
  analysis: string[] = [];

  constructor(
    private formbuilder: FormBuilder,
    private homeFacade: HomeFacade
  ) {
    this.form = formbuilder.group({
      startDate: [null],
      endDate: [this.maxDate],
      detailLevel: [0],
      mode: ['frequency'],
      analysis: 'live',
    });
    this.setGraph();
  }

  ngOnInit(): void {
    this.changeMode('frequency');
  }

  setGraph() {
    this.subscriptionA = this.homeFacade.getAnalysis().subscribe((value) => {
      this.analysis = value;
    });
    this.subscriptionP = this.homeFacade.getPerformanceGraph().subscribe({
      next: (flow) => {
        this.performanceGraph = flow;
      },
    });
    this.subscriptionF = this.homeFacade.getFrequencyGraph().subscribe({
      next: (flow) => {
        this.frequencyGraph = flow;
        this.graphSource = flow;
      },
    });
    this.subscriptionS = this.homeFacade.getFilterStatistics().subscribe({
      next: (value) => {
        this.statistics = value;
      },
    });
    this.homeFacade.filterFlowGraph(this.form.value);
    this.homeFacade.fetchAnalysis();
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
      start: formatDate(
        this.form.controls['startDate'].value,
        'y-MM-dd',
        'pt-BR'
      ),
      end: formatDate(this.form.controls['endDate'].value, 'y-MM-dd', 'pt-BR'),
    };
    const graphParams: FlowGraphParams = {
      startDate: formattedDates.start,
      endDate: formattedDates.end,
      analysis: this.form.controls['analysis'].value,
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
    if (this.subscriptionS) {
      this.subscriptionS.unsubscribe();
    }
    if (this.subscriptionA) {
      this.subscriptionA.unsubscribe();
    }
  }
}
