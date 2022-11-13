import {
  Component,
  ElementRef,
  OnInit,
  ViewChild,
  AfterContentChecked,
  Input,
} from '@angular/core';
import { SafeHtml } from '@angular/platform-browser';
import { HomeFacade } from '../../home.facade';
import * as svgPanZoom from 'svg-pan-zoom';

@Component({
  selector: 'app-flow',
  templateUrl: './flow.component.html',
  styleUrls: ['./flow.component.scss'],
})
export class FlowComponent implements OnInit, AfterContentChecked {
  @ViewChild('graph', { static: false }) graph!: ElementRef;
  @Input() graphSource!: SafeHtml | null;
  changeCount: number = 0;

  constructor(private homeFacade: HomeFacade) {}

  ngOnInit(): void {}

  ngAfterContentChecked(): void {
    this.changeCount += 1;
    if (this.changeCount > 2 && this.graphSource != null) {
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
}
