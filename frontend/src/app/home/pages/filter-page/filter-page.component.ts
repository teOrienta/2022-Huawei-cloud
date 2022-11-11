import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { SafeHtml } from '@angular/platform-browser';
import { Subscription } from 'rxjs';
import { HomeFacade } from '../../home.facade';
import * as svgPanZoom from 'svg-pan-zoom';

@Component({
  selector: 'app-filter-page',
  templateUrl: './filter-page.component.html',
  styleUrls: ['./filter-page.component.scss'],
})
export class FilterPageComponent implements OnInit {
  form: FormGroup;
  subscription!: Subscription;
  dataName = 'UFPE';
  dataDate = Date.now();
  changeCount: number = 0;
  detailLevel: number = 0;

  @ViewChild('graph', { static: false }) graph!: ElementRef;

  constructor(
    private formbuilder: FormBuilder,
    private homeFacade: HomeFacade
  ) {
    this.form = formbuilder.group({
      startDate: [null],
      endDate: [null],
      detailLevel: [null],
      mode: ['frequency'],
    });
  }

  graphSource!: SafeHtml | null;

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
}
