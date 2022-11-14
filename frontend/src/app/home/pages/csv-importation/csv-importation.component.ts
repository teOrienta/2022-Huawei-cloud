import { Component, OnDestroy, OnInit } from '@angular/core';
import { HomeFacade } from '../../home.facade';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { SelectItem } from 'primeng/api';
import { UploadParams } from 'src/app/shared/types/upload-params';
import { UploadFileService } from '../../services/upload-file.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-csv-importation',
  templateUrl: './csv-importation.component.html',
  styleUrls: ['./csv-importation.component.scss'],
})
export class CsvImportationComponent implements OnInit, OnDestroy {
  form: FormGroup;
  tableData: string[][] = [];
  lazyItems: SelectItem[] = [];

  fileToUpload: File | null = null;
  fileParams: UploadParams = {} as UploadParams;

  subscriptionC!: Subscription;
  subscriptionU!: Subscription;

  constructor(
    private homeFacade: HomeFacade,
    private formbuilder: FormBuilder,
    private uploadFileService: UploadFileService
  ) {
    this.form = formbuilder.group({
      analysisName: [null, Validators.required],
      startTimestamp: [null],
      timestamp: [null, Validators.required],
      case: ['', Validators.required],
      activity: ['', Validators.required],
      orgResource: ['', Validators.required],
    });
  }

  ngOnInit() {
    this.subscriptionC = this.uploadFileService.currentFile.subscribe(
      (file) => {
        this.fileToUpload = file;

        if (file !== null) {
          this.generateColumns();
        }
      }
    );
  }

  generateColumns() {
    const pushColumns = (columns: string[]) => {
      this.tableData = [];
      columns.forEach((column) =>
        this.tableData.push(
          column.split(/[,|	;]/).map((row) => row.split('"').join(''))
        )
      );
    };
    if (this.fileToUpload?.name.indexOf('.csv') !== -1) {
      var reader = new FileReader();
      reader.onload = function () {
        let textFile = reader.result as string;
        if (textFile) {
          let columnsFile = textFile.split('\n').slice(0, 2);
          pushColumns(columnsFile);
        }
      };
      reader.readAsText(this.fileToUpload as File);
    }
  }

  uploadFile() {
    if (this.fileToUpload === null || !this.form.valid) {
      return;
    }

    let values = this.form.value;
    this.fileParams.name = values.analysisName;
    this.fileParams.startTimestamp = values.startTimestamp;
    this.fileParams.timestamp = values.timestamp;
    this.fileParams.case = values.case;
    this.fileParams.activity = values.activity;
    this.fileParams.orgResource = values.orgResource;

    let loading = document.querySelector('.loadingSpace') as HTMLElement;
    loading.style.display = 'flex';

    const tableName = String(this.fileParams.name)
      .toLocaleLowerCase()
      .replace(/ /g, '_')
      .replace(/\W/g, '');
    localStorage.setItem('HashID', tableName);

    if (this.fileToUpload.name.indexOf('.csv') !== -1) {
      this.subscriptionU = this.uploadFileService
        .postFile(this.fileToUpload as File, this.fileParams)
        .subscribe({
          next: (e) => console.log('upload with successful', e),
          error: (error) => this.handleUploadError(loading, error),
        });
    }
  }

  handleUploadError(loading: HTMLElement, error: any) {
    console.error(error);
    let loadingImg = loading.querySelector('img') as HTMLImageElement;
    let paragraph = loading.querySelector('p') as HTMLParagraphElement;
    let background = loading.querySelector('div') as HTMLDivElement;
    loadingImg.src = 'assets/close.png';
    paragraph.innerHTML = 'Não conseguimos processar <br> o seu arquivo!';
    background.style.cursor = 'pointer';
    background.onclick = () => {
      this.closeMessageError(loading, loadingImg, paragraph, background);
    };
  }

  closeMessageError(
    loading: HTMLElement,
    loadingImg: HTMLImageElement,
    paragraph: HTMLParagraphElement,
    background: HTMLDivElement
  ) {
    loadingImg.src = 'assets/loading.svg';
    paragraph.innerHTML = '';
    loading.style.display = 'none';
    background.onclick = () => {};
    background.style.cursor = '';
  }

  ngOnDestroy(): void {
    if (this.subscriptionC) this.subscriptionC.unsubscribe();
    if (this.subscriptionU) this.subscriptionU.unsubscribe();
  }
}
