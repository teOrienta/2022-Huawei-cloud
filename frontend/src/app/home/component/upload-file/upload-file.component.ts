import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { UploadFileService } from '../../services/upload-file.service';

@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.scss'],
})
export class UploadFileComponent implements OnInit {
  fileToUpload: File | null = null;

  @ViewChild('arquivo') fileInput!: ElementRef;

  constructor(private fileUploadService: UploadFileService) {}

  ngOnInit(): void {}

  handleFileInput(event: any) {
    let files = event.target.files;
    this.fileToUpload = files.item(0);
    this.fileUploadService.changeFile(this.fileToUpload);
  }

  upload() {
    this.fileInput.nativeElement.click();
  }
}
