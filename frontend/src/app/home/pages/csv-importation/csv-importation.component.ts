import { Component, OnDestroy, OnInit } from '@angular/core';
import { HomeFacade } from '../../home.facade';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UploadParams } from 'src/app/shared/types/upload-params';
import { UploadFileService } from '../../services/upload-file.service';
import { first, Subscription } from 'rxjs';

@Component({
  selector: 'app-csv-importation',
  templateUrl: './csv-importation.component.html',
  styleUrls: ['./csv-importation.component.scss'],
})
export class CsvImportationComponent implements OnInit, OnDestroy {
  form: FormGroup;
  exampleSource: string[] = [];
  exampleColumns: string[] = ['', '', '', '', ''];
  columns: { label: string; value: string }[] = [];

  fileToUpload: File | null = null;
  fileParams: UploadParams = {} as UploadParams;

  subscription!: Subscription;

  constructor(
    private homeFacade: HomeFacade,
    private formbuilder: FormBuilder,
    private uploadFileService: UploadFileService
  ) {
    this.form = formbuilder.group({
      analysisName: [null, Validators.required],
      timestamp: [null, Validators.required],
      activity: [null, Validators.required],
      case: [null, Validators.required],
      startTimestamp: [null],
      orgResource: [null],
    });
  }

  ngOnInit() {
    this.subscription = this.uploadFileService.currentFile.subscribe((file) => {
      this.fileToUpload = file;
      if (file !== null) {
        this.generateColumns();
      }
    });
  }

  generateColumns() {
    const getColumns = (text: string) => {
      return text.split(/[,|	;]/).map((value) => value.split(/["\r]/).join(''));
    };

    const setHeaderColumns = (row: string) => {
      this.columns = [{ label: 'empty', value: '' }];
      getColumns(row).map((value) => {
        this.columns.push({ label: value, value: value });
      });
    };
    const setExampleColumns = (row: string) => {
      this.exampleSource = [''];
      getColumns(row).map((value) => {
        this.exampleSource.push(value);
      });
    };

    if (this.fileToUpload?.name.indexOf('.csv') !== -1) {
      var reader = new FileReader();
      reader.onload = function () {
        let textFile = reader.result as string;
        if (textFile) {
          let columnsFile = textFile.split('\n').slice(0, 2);
          setHeaderColumns(columnsFile[0]);
          setExampleColumns(columnsFile[1]);
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
    this.fileParams.analysisName = values.analysisName;
    this.fileParams.startTimestamp = values.startTimestamp;
    this.fileParams.timestamp = values.timestamp;
    this.fileParams.caseID = values.case;
    this.fileParams.activity = values.activity;
    this.fileParams.orgResource = values.orgResource;

    if (this.fileToUpload.name.indexOf('.csv') !== -1) {
      this.uploadFileService
        .postFile(this.fileToUpload as File, this.fileParams)
        .pipe(first())
        .subscribe({
          next: (e) => {}, // Close loading
        });
    }
  }

  onChangeColumn(event: any, index: number) {
    let valueIndex = 0;
    this.columns.map((value, index) => {
      if (value.value === event.value) {
        valueIndex = index;
      }
    });
    this.exampleColumns[index] = this.exampleSource[valueIndex];
  }

  ngOnDestroy(): void {
    if (this.subscription) this.subscription.unsubscribe();
  }
}
