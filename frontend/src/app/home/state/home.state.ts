import { BehaviorSubject } from 'rxjs';
import { Injectable } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { FlowGraphParams } from 'src/app/shared/types/flow-graph-params';

@Injectable({ providedIn: 'root' })
export class HomeState {
  private readonly graphSource = new BehaviorSubject<SafeHtml>(
    this.sanitizer.bypassSecurityTrustHtml(`<svg><\svg>`)
  );
  private readonly graphGenerationParams = new BehaviorSubject<FlowGraphParams>(
    { start_date: null, end_date: null }
  );
  private readonly errorMessage = new BehaviorSubject<string>('');
  private readonly loading = new BehaviorSubject<boolean>(false);

  constructor(private readonly sanitizer: DomSanitizer) {}

  getGraphSource() {
    return this.graphSource.asObservable();
  }

  setGraphSource(graphSource: string) {
    this.graphSource.next(this.sanitizer.bypassSecurityTrustHtml(graphSource));
  }

  getGraphGenerationParams() {
    return this.graphGenerationParams.asObservable();
  }

  setGraphGenerationParams(value: FlowGraphParams) {
    this.graphGenerationParams.next(value);
  }

  getErrorMessage() {
    return this.errorMessage.asObservable();
  }

  setErrorMessage(message: string) {
    this.errorMessage.next(message);
  }

  getLoading() {
    return this.loading.asObservable();
  }

  setLoading(isLoading: boolean) {
    this.loading.next(isLoading);
  }
}
