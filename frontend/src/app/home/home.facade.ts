import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import { FlowGraphParams } from '../shared/types/flow-graph-params';
import { HomeState } from './state/home.state';
import { HomeApi } from './api/home.api';
import { HomeService } from './services/home.service';

@Injectable()
export class HomeFacade {
  constructor(
    private homeService: HomeService,
    private readonly state: HomeState,
    private readonly flowGraphApi: HomeApi
  ) {}

  getPerformanceGraph() {
    return this.state.getPerformanceGraph();
  }

  getFrequencyGraph() {
    return this.state.getFrequencyGraph();
  }

  getGraphSource() {
    return this.state.getGraphSource();
  }

  downloadFlow() {
    return this.homeService.downloadFlow();
  }

  setGraphParams(params: FlowGraphParams) {
    return this.state.setGraphGenerationParams(params);
  }

  fetchFlowGraph(
    fetchParams = {
      successfulCallback: () => {},
    }
  ) {
    const { successfulCallback } = fetchParams;
    this.state.setLoading(true);
    this.flowGraphApi
      .getLiveFlowGraph()
      .pipe(first())
      .subscribe({
        next: (data) => {
          this.state.setGraphSource(data);
          successfulCallback();
        },
        complete: () => this.state.setLoading(false),
        error: (error: Error) => {
          this.state.setErrorMessage(error.message);
          this.state.setLoading(false);
        },
      });
  }

  filterFlowGraph(params: FlowGraphParams) {
    this.state.setLoading(true);
    this.flowGraphApi
      .filterFlowGraph(params)
      .pipe(first())
      .subscribe({
        next: (data) => {
          this.state.setGraphGenerationParams(params);
          this.state.setFrequencyGraph(data.freq_svg);
          this.state.setPerformanceGraph(data.perf_svg);
          this.state.setStatistics(data.statistics);
        },
        complete: () => this.state.setLoading(false),
        error: (error: Error) => {
          this.state.setErrorMessage(error.message);
          this.state.setLoading(false);
        },
      });
  }
}
