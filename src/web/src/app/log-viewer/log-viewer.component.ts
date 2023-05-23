import { Component } from '@angular/core';
import { FastApiService } from '../fast-api.service';

@Component({
  selector: 'app-log-viewer',
  templateUrl: './log-viewer.component.html',
  styleUrls: ['./log-viewer.component.css']
})
export class LogViewerComponent {
  logs: string | undefined;
  defaultSource = 'scheduler';
  errorMsg = '';

  constructor(private fastApiService: FastApiService) { }

  viewLogs(source: string = this.defaultSource): void {
    this.fastApiService.getLogs(source)
    .subscribe(
      (data: string) => {
        this.errorMsg = '';
        this.logs = data;
      },
      (error: any) => {
        this.errorMsg = 'nie udało się pobrać pliku z logami';
      }
    );
}
}
