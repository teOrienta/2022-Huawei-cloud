import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import {
  FetchFlowGraph,
  FlowGraphParams,
} from '../shared/types/flow-graph-params';
import { HomeState } from './state/home.state';
import { HomeApi } from './api/home.api';
import { HomeService } from './services/home.service';

@Injectable()
export class HomeFacade {
  constructor(
    private homeService: HomeService,
    private readonly state: HomeState,
    private readonly homeApi: HomeApi
  ) {}

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
    fetchParams: FetchFlowGraph = {
      params: {} as FlowGraphParams,
      successfulCallback: () => {},
    }
  ) {
    const { successfulCallback } = fetchParams;
    this.state.setLoading(true);
    this.homeApi
      .downloadFlowGraph()
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

  fetchCounties() {
    this.homeApi.getCounties().subscribe((data) => {
      console.log(data)
      //this.state.setCountiesState(data);
    })
  }

  getCountiesState() {
    return this.state.getCountiesState();
  }

  fetchAcquisitionTypes() {
    this.homeApi.getAcquisitionTypes().subscribe((data) => {
      console.log(data);
      //this.state.setAcquisitionsState(data);
    })
  }

  getAcquisitionTypesState() {
    return this.state.getAcquisitionsState();
  }

}
