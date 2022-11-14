import {
  HttpClient,
  HttpErrorResponse,
  HttpHeaders,
} from '@angular/common/http';
import {
  throwError as observableThrowError,
  Observable,
  BehaviorSubject,
} from 'rxjs';
import { Injectable } from '@angular/core';
import { catchError, map } from 'rxjs/operators';
import { UploadParams } from 'src/app/shared/types/upload-params';

@Injectable({
  providedIn: 'root',
})
export class UploadFileService {
  constructor(private http: HttpClient) {}
  private fileSource = new BehaviorSubject<File | null>(null);
  currentFile = this.fileSource.asObservable();

  createFormData(params: UploadParams) {
    const formData: FormData = new FormData();
    formData.append('analysis_name', params.analysisName);
    formData.append('case_id_key', params.caseID);
    formData.append('activity_key', params.activity);
    formData.append('resource_key', params.orgResource);
    formData.append('timestamp_key', params.timestamp);
    formData.append('start_timestamp_key', params.startTimestamp);

    return formData;
  }

  postFile(fileToUpload: File, params: UploadParams): Observable<boolean> {
    const formData: FormData = this.createFormData(params);
    formData.append('file', fileToUpload, fileToUpload.name);

    return this.http
      .post('/api/upload/', formData, {
        headers: new HttpHeaders({
          timeout: `${5 * 60 * 1000}`,
        }),
      })
      .pipe(
        map(() => {
          return true;
        }),
        catchError((e: HttpErrorResponse) => this.handleError(e))
      );
  }

  changeFile(file: File | null) {
    this.fileSource.next(file);
  }

  protected handleError(httpError: HttpErrorResponse) {
    console.error('Ocorreu erro na requisição:', httpError);
    if (httpError.status >= 401 && httpError.status <= 403) {
      window.location.href = '/';
    }
    return observableThrowError(httpError);
  }
}
