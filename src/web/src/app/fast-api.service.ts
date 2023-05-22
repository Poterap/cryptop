import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FastApiService {
  private apiBaseUrl = 'http://127.0.0.1:8080';

  constructor(private http: HttpClient) {}

  public getStooqSymbols(): Observable<any> {
    const url = `${this.apiBaseUrl}/symbols_stooq`;
    return this.http.get(url);
  }

  public getLogs(source: string): Observable<string> {
    const url = `${this.apiBaseUrl}/logs/${source}`;
    return this.http.get(url, { responseType: 'text' });
  }
}
