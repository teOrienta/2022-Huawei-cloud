import { Component, OnInit, OnDestroy, Output } from '@angular/core';
import { HomeFacade } from '../../home.facade';
import { SafeHtml } from '@angular/platform-browser';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit, OnDestroy {
  dataDate = Date.now();
  intervalId: NodeJS.Timer;
  isPaused: boolean = true;
  subscription!: Subscription;
  graphSource!: SafeHtml | null;

  constructor(private readonly homeFacade: HomeFacade) {
    this.intervalId = this.updateData();
    this.setGraph();
  }

  updateData() {
    this.isPaused = !this.isPaused;
    if (!this.isPaused) {
      return setInterval(() => {
        this.homeFacade.fetchFlowGraph();
        this.dataDate = Date.now();
      }, 30000);
    } else {
      clearInterval(this.intervalId);
      return {} as NodeJS.Timer;
    }
  }

  setGraph() {
    this.subscription = this.homeFacade.getGraphSource().subscribe({
      next: (flow) => {
        this.graphSource = flow;
      },
    });
  }

  ngOnDestroy(): void {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }

  ngOnInit(): void {}

  download() {
    this.homeFacade.downloadFlow();
  }
}
