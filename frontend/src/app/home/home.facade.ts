import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import { FetchFlowGraph } from '../shared/types/flow-graph-params';
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

  getGraphSource() {
    return this.state.getGraphSource();
  }

  downloadFlow() {
    return this.homeService.downloadFlow();
  }

  fetchFlowGraph(
    fetchParams: FetchFlowGraph = {
      params: { start_date: null, end_date: null },
      successfulCallback: () => {},
    }
  ) {
    const { params, successfulCallback } = fetchParams;
    this.state.setLoading(true);
    this.flowGraphApi
      .downloadFlowGraph()
      .pipe(first())
      .subscribe({
        next: (data) => {
          this.state.setGraphSource(data);
          this.state.setGraphGenerationParams(params);
          successfulCallback();
        },
        complete: () => this.state.setLoading(false),
        error: (error: Error) => {
          this.state.setErrorMessage(error.message);
          this.state.setLoading(false);
        },
      });
  }
}
