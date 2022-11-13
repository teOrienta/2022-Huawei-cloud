import { Injectable, SecurityContext } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { FileSaverService } from 'ngx-filesaver';
import { take } from 'rxjs';
import { HomeApi } from '../api/home.api';

@Injectable()
export class HomeService {
  constructor(
    private readonly state: HomeApi,
    private fileSaverService: FileSaverService,
    private sanitizer: DomSanitizer,
    private flowGraphApi: HomeApi
  ) {}

  public downloadFlow() {
    this.state
      .getLiveFlowGraph()
      .pipe(take(1))
      .subscribe((value) => {
        return this.fileSaverService.saveText(value, 'fluxo.svg');
      });
  }
}
