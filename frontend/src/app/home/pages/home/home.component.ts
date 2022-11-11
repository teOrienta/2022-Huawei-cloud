import { Component, OnInit } from '@angular/core';
import { HomeFacade } from '../../home.facade';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  dataName = 'UFPE';
  dataDate = Date.now();
  intervalId: NodeJS.Timer;
  isPaused: boolean = true;

  constructor(private readonly homeFacade: HomeFacade) {
    this.intervalId = this.updateData();
  }

  updateData() {
    this.isPaused = !this.isPaused;
    if (!this.isPaused) {
      return setInterval(() => {
        this.homeFacade.fetchFlowGraph();
        this.dataDate = Date.now();
      }, 30000);
    } else {
      console.log(this.intervalId);
      clearInterval(this.intervalId);
      return {} as NodeJS.Timer;
    }
  }

  ngOnInit(): void {}

  download() {
    this.homeFacade.downloadFlow();
  }
}
