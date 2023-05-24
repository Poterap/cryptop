import { Component } from '@angular/core';
import { FastApiService } from '../fast-api.service';

@Component({
  selector: 'file-list',
  templateUrl: './file-list.component.html',
  styleUrls: ['./file-list.component.css']
})
export class FileListComponent {
  datas: { [key: string]: string[] } = {};
  Object = Object;
  info: string = '';
  source: string = '';

  constructor(private fastApiService: FastApiService) {}

  getFolders(source: string) {
    this.fastApiService.getFolders(source).subscribe(
      response => {
        this.info = source;
        this.source = source;
        this.datas = response.datas;
      },
      error => {
        console.error(error);
      }
    );
  }

  getEdaRaports(file: string) {
    const parts = file.split('_');
  
    const symbol = parts[0];
    const date = parts[1];

    this.fastApiService.getEDAReport(symbol, date, this.source).subscribe(
      (html: string) => {
        const blob = new Blob([html], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        window.open(url, '_blank');
      },
      (error) => {
        console.error(error);
      }
    );
  }
}
