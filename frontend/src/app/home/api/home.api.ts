import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable()
export class HomeApi {
  constructor(private readonly http: HttpClient) {}

  public downloadFlowGraph() {
    return this.http.get('/api/image/download', {
      responseType: 'text',
    });
  }
}
