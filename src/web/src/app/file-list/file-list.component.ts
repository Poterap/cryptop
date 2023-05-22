import { Component, OnInit } from '@angular/core';
import { FastApiService } from '../fast-api.service';

@Component({
  selector: 'file-list',
  templateUrl: './file-list.component.html',
  styleUrls: ['./file-list.component.css']
})
export class FileListComponent implements OnInit {
  title = 'Lista dostępnych raportów EDA';
  raports: any[] = [];

  constructor(private fastApiService: FastApiService) {}

  ngOnInit(): void {
    this.getStooqSymbols();
  }

  getStooqSymbols(): void {
    this.fastApiService.getStooqSymbols().subscribe(
      (response: any) => {
        this.raports = response.symbols;
      },
      (error: any) => {
        console.error(error);
      }
    );
  }
}
