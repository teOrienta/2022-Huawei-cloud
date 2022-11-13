import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FlowGraphParams } from '../../shared/types/flow-graph-params';
import Statistics from '../../shared/types/statistics';

@Injectable()
export class HomeApi {
  constructor(private readonly http: HttpClient) {}

  public filterFlowGraph(params: FlowGraphParams) {
    return this.http.post<{
      freq_svg: string;
      perf_svg: string;
      statistics: Statistics
    }>('/api/filter', params);
  }

  public getLiveFlowGraph() {
    return this.http.get('/api/image/download', {
      responseType: 'text',
    });
  }
}
