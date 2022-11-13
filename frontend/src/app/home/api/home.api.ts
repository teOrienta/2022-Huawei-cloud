import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FlowGraphParams } from 'src/app/shared/types/flow-graph-params';

@Injectable()
export class HomeApi {
  constructor(private readonly http: HttpClient) {}

  public getFlowGraph(params: FlowGraphParams) {
    return this.http.get('/api/image/', {
      responseType: 'text',
    });
  }

  public downloadFlowGraph() {
    return this.http.get('/api/image/download', {
      responseType: 'text',
    });
  }
}
