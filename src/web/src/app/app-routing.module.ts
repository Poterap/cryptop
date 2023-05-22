import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FileListComponent } from './file-list/file-list.component';
import { LogViewerComponent } from './log-viewer/log-viewer.component';

const routes: Routes = [
  {path: 'EdaRaports', component: FileListComponent},
  {path: 'Logs', component: LogViewerComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
