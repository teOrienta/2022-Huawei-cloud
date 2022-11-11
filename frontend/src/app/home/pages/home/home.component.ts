import {
  Component,
  OnInit,
  ViewChild,
  ElementRef,
  OnDestroy,
  AfterContentChecked,
} from '@angular/core';
import { SafeHtml } from '@angular/platform-browser';
import { Subscription } from 'rxjs';
import * as svgPanZoom from 'svg-pan-zoom';
import { HomeFacade } from '../../home.facade';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit, OnDestroy, AfterContentChecked {
  graphSource!: SafeHtml | null;
  dataName = 'UFPE';
  dataDate = Date.now();

  subscription!: Subscription;
  changeCount: number = 0;

  @ViewChild('graph', { static: false }) graph!: ElementRef;

  constructor(private readonly homeFacade: HomeFacade) {
    setInterval(() => {
      this.homeFacade.fetchFlowGraph();
      this.dataDate = Date.now();
    }, 30000);
  }

  ngOnInit(): void {
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

  ngAfterContentChecked(): void {
    this.changeCount += 1;
    if (this.changeCount > 2) {
      this.renderSvgPanZoom();
    }
  }

  renderSvgPanZoom() {
    const svgElement = this.graph.nativeElement.querySelector('svg');
    if (svgElement === null) return;

    svgPanZoom(svgElement as SVGElement, {
      zoomEnabled: true,
      controlIconsEnabled: true,
      fit: true,
      center: true,
      dblClickZoomEnabled: false,
    });
    svgElement.style.width = '100%';
    svgElement.style.height = '100%';

    const controls = svgElement.querySelector(
      '#svg-pan-zoom-controls'
    ) as HTMLElement;
    controls.style.transform = 'translate(5px, 10px) scale(0.6)';
  }

  download() {
    this.homeFacade.downloadFlow();
  }
}
