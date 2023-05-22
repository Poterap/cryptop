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

  constructor(private fastApiService: FastApiService) { }

  viewLogs(source: string = this.defaultSource): void {
    this.fastApiService.getLogs(source)
      .subscribe((data: string) => {
        this.logs = data;
      });
  }
}
