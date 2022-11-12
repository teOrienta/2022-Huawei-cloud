import { BehaviorSubject } from 'rxjs';
import { Injectable } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { FlowGraphParams } from 'src/app/shared/types/flow-graph-params';
import Statistics from '../../shared/types/statistics';

@Injectable({ providedIn: 'root' })
export class HomeState {
  private readonly graphSource = new BehaviorSubject<SafeHtml>(
    this.sanitizer.bypassSecurityTrustHtml(`<svg><\svg>`)
  );
  private readonly frequencyGraph = new BehaviorSubject<SafeHtml>(
    this.sanitizer.bypassSecurityTrustHtml(`<svg><\svg>`)
  );
  private readonly performanceGraph = new BehaviorSubject<SafeHtml>(
    this.sanitizer.bypassSecurityTrustHtml(`<svg><\svg>`)
  );
  private readonly statistics = new BehaviorSubject<Statistics>({
    cases: 0, activities: 0, averageCaseDuration: 0, averageActivityDuration: 0
  });
  private readonly graphGenerationParams = new BehaviorSubject<FlowGraphParams>(
    {} as FlowGraphParams
  );
  private readonly errorMessage = new BehaviorSubject<string>('');
  private readonly loading = new BehaviorSubject<boolean>(false);

  constructor(private readonly sanitizer: DomSanitizer) {}

  getGraphSource() {
    return this.graphSource.asObservable();
  }

  setFrequencyGraph(graphSource: string) {
    this.frequencyGraph.next(this.sanitizer.bypassSecurityTrustHtml(graphSource));
  }

  setPerformanceGraph(graphSource: string) {
    this.performanceGraph.next(this.sanitizer.bypassSecurityTrustHtml(graphSource));
  }

  setStatistics(newStatistics: Statistics) {
    this.statistics.next(newStatistics);
  }

  setGraphSource(graphSource: string) {
    this.graphSource.next(this.sanitizer.bypassSecurityTrustHtml(graphSource));
  }

  getGraphGenerationParams() {
    return this.graphGenerationParams.asObservable();
  }

  getFrequencyGraph() {
    return this.frequencyGraph.asObservable();
  }

  getPerformanceGraph() {
    return this.performanceGraph.asObservable();
  }

  getStatistics() {
    return this.statistics.asObservable();
  }

  setGraphGenerationParams(value: FlowGraphParams) {
    this.graphGenerationParams.next(value);
  }

  setCountiesState(counties: County) {
    this.countiesState.next(counties);
  }

  getCountiesState() {
    return this.countiesState.asObservable();
  }

  setAcquisitionsState(acquisitions: Acquisition) {
    this.acquisitionsState.next(acquisitions);
  }

  getAcquisitionsState() {
    return this.acquisitionsState.asObservable();
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
