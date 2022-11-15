import { BehaviorSubject } from 'rxjs';
import { Injectable } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { FlowGraphParams } from 'src/app/shared/types/flow-graph-params';
import Statistics from '../../shared/types/statistics';

@Injectable({ providedIn: 'root' })
export class HomeState {
  private readonly graphSource = new BehaviorSubject<SafeHtml | null>(null);
  private readonly frequencyGraph = new BehaviorSubject<SafeHtml | null>(null);
  private readonly performanceGraph = new BehaviorSubject<SafeHtml | null>(
    null
  );
  private readonly statistics = new BehaviorSubject<Statistics>({
    cases: 0,
    activities: 0,
    averageCaseDuration: "",
    averageActivityDuration: "",
  });
  private readonly graphGenerationParams = new BehaviorSubject<FlowGraphParams>(
    {} as FlowGraphParams
  );
  private readonly analysis = new BehaviorSubject<string[]>([]);
  private readonly errorMessage = new BehaviorSubject<string>('');
  private readonly loading = new BehaviorSubject<boolean>(false);

  constructor(private readonly sanitizer: DomSanitizer) {}

  getAnalysis() {
    return this.analysis.asObservable();
  }

  setAnalysis(analysis: string[]) {
    this.analysis.next(analysis);
  }

  getGraphSource() {
    return this.graphSource.asObservable();
  }

  setFrequencyGraph(graphSource: string) {
    this.frequencyGraph.next(
      this.sanitizer.bypassSecurityTrustHtml(graphSource)
    );
  }

  setPerformanceGraph(graphSource: string) {
    this.performanceGraph.next(
      this.sanitizer.bypassSecurityTrustHtml(graphSource)
    );
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
