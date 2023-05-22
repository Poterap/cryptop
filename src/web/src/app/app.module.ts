import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FileListComponent } from './file-list/file-list.component';
import { EdaRaportService } from './eda-raports.service';
import { HttpClientModule } from '@angular/common/http';
import { LogViewerComponent } from './log-viewer/log-viewer.component';

@NgModule({
  declarations: [
    AppComponent,
    FileListComponent,
    LogViewerComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
